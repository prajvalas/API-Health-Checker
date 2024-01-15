import yaml
import requests
import time
from urllib.parse import urlparse
from decouple import config

class HealthCheck:
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
        availibility = {}
        executions = {}
        runs = 1

        while True:
            print(f"Run {runs}")
            for index,d in enumerate(self.data):
                headers = d.get('headers', {})
                method = d.get('method', 'GET')
                name = d.get('name', '')
                url = d.get('url', '')

                start = time.time()
                try:
                    response = requests.request(method, url, headers=headers).status_code
                except Exception as e:
                    print(f"Error encountered when calling the API --- {e}")
                    return
                end = time.time()
            
                # print(f"{name} - Response : {response}, Latency : {end-start}")

                domain = urlparse(url).netloc
            
                if domain not in executions:
                    executions[domain] = 0
                executions[domain] += 1

                if domain not in availibility:
                    availibility[domain] = 0
                if (200 <= response < 300) and (end-start < 0.5):
                    availibility[domain] += 1
                
            # print(availibility)
            # print(executions)

            for domain,ups in availibility.items():
                divisor = executions[domain]
                print(f"{domain} has {round(100*(ups/divisor))}% availability percentage")

            time.sleep(int(interval))
            runs = runs+1
            print()

    def read_input(self):
        '''
        This method reads the input from the input file using the `file_path` entered.
        Returns - 
            True : if the data was retrieved from the file without any errors
            False : if the data was not retrieved from the file due to an error
        '''

        try:
            file_path = input("Enter the file path : ")
            with open(file_path, 'r') as file:
                self.data = yaml.safe_load(file)
            return True
        except Exception as e:
            print("Error when reading the input_file")
            return False

    def main(self):
        '''
        This method calls first reads the input and only if valid data is returned,
        it performs a health check on all the API endpoints
        '''

        if self.read_input() and self.data:
            self.health_check()
        else:
            print("Invalid or empty input file.")

if __name__ == "__main__":
    ping = HealthCheck()
    ping.main()
    