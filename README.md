# API-Health-Checker
Checks if an API endpoint is up or down, every 15 seconds

**Code Execution Steps**
1. Ensure that python is installed in your system
2. (Optional step) Open the command prompt and create a virtual environment to isolate dependencies using `python -m venv venv` for python and `python3 -m venv venv` for python3
3. Navigate to the directory where the project files are present using `cd API-Health-Checker`
4. Install dependencies using `pip install -r requirements.txt` for python or `pip3 install -r requirements.txt` for python3
5. Run the code using the command `python main.py` for python or `python3 main.py` for python3
6. On entering this, you'll be prompted to enter the file path for your input file. Enter the path as such `/Users/username/Desktop/input.yml` and hit Enter

**How it works**
It performs a health check for all API endpoints mentioned in the input file.
Execution ends when the user terminates the program execution using CTRL+C keys.

A health check is performed every 15 seconds and the below is printed to the console.

```
    Run 1
    fetch.com has 67% availability percentage
    www.fetchrewards.com has 0% availability percentage

    Run 2
    fetch.com has 67% availability percentage
    www.fetchrewards.com has 50% availability percentage
```

In the above sample output, 
For Run 1 --> fetch.com had 2/3 successful responses
                www.fetchrewards.com had 0/1 successful responses
For Run 2 --> fetch.com had 4/6 successful responses
                www.fetchrewards.com had 1/2 successful responses

Successful response is the one where the response code is between 200 and 299 (inclusive) and response latency is <0.5s