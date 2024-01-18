import yaml
import requests
import time
from urllib.parse import urlparse
from decouple import config

class ConfigReader:
    @staticmethod
    def read_input():
        '''
        This method reads the input from the input file using the `file_path` entered.
        Returns - 
            FileContent : if the data was retrieved from the file without any errors
            None : if the data was not retrieved from the file due to an error
        '''
        try:
            file_path = input("Enter the file path: ")
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error when reading the input file: {e}")
            return None

class ApiRequester:
    @staticmethod
    def make_request(method, url, headers):
        '''
        This method makes an API call using the parameters passed.
        Returns - 
            ResponseCode : if the api responded within the specified time without any errors
            None : if the api did not response within the specified time or resulted in an error
        '''
        try:
            response = requests.request(method, url, headers=headers, timeout=0.5)
            return response.status_code
        except requests.RequestException as e:
            return None

class HealthCheck:
    def __init__(self, data):
        self.data = data
        self.runs = 1

    def calculate_availability(self):
        for api_data in self.data:
            headers = api_data.get('headers', {})
            method = api_data.get('method', 'GET').upper()
            if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                print(f"Warning: Invalid HTTP method '{method}' specified. Defaulting to 'GET'")
                method = 'GET'

            url = api_data.get('url', '')

            response = ApiRequester.make_request(method, url, headers)
            domain = urlparse(url).netloc

            if domain not in self.executions:
                self.executions[domain] = 0
            self.executions[domain] += 1

            if domain not in self.availability:
                self.availability[domain] = 0
            if response is not None and 200 <= response < 300:
                self.availability[domain] += 1

        # print(self.availability)
        # print(self.executions)

        for domain, ups in self.availability.items():
            divisor = self.executions[domain]
            print(f"{domain} has {round(100 * (ups / divisor))}% availability percentage")

    def health_check(self):
        '''
        This method is only called if valid data exists in the input file.
        It performs a health check for all API endpoints mentioned in the input file.
        Execution ends when the user terminates the program execution using CTRL+C keys.

        A health check is performed every 15 seconds and the below is printed to the console.
            Run 1
            fetch.com has 67% availability percentage
            www.fetchrewards.com has 0% availability percentage

            Run 2
            fetch.com has 67% availability percentage
            www.fetchrewards.com has 50% availability percentage

        In the above sample output, 
        For Run 1 --> fetch.com had 2/3 successful responses
                      www.fetchrewards.com had 0/1 successful responses
        For Run 2 --> fetch.com had 4/6 successful responses
                      www.fetchrewards.com had 1/2 successful responses

        Successful response is the one where the response code is between 200 and 299 (inclusive) and response latency is <0.5s

        '''

        interval = config('INTERVAL')
        self.availability = {}
        self.executions = {}

        while True:
            print(f"Run {self.runs}")
            self.calculate_availability()
            time.sleep(int(interval))
            self.runs += 1
            print()

class Application:
    @staticmethod
    def main():
        '''
        This method first reads the input and only if valid data is returned,
        it performs a health check on all the API endpoints
        '''
        data = ConfigReader.read_input()
        if data:
            health_check = HealthCheck(data)
            health_check.health_check()
        else:
            print("Invalid or empty input file.")

if __name__ == "__main__":
    Application.main()