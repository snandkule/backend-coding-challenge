# Challenge

This challenge is divided between the main task and additional stretch goals. All of those stretch goals are optional, but we would love to see them implemented. It is expected that you should be able to finish the challenge in about 1.5 hours. If you feel you are not able to implement everything on time, please, try instead describing how you would solve the points you didn't finish.

And also, please do not hesitate to ask any questions. Good luck!

## gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public GitHub Gists.
The existing code already implements most of the Flask boilerplate for you.
The main functionality is left for you to implement.
The goal is to implement an endpoint that searches a user's Gists with a regular expression.
For example, I'd like to know all Gists for user `justdionysus` that contain the pattern `import requests`.
The code in `gistapi.py` contains some comments to help you find your way.

To complete the challenge, you'll have to write some HTTP queries from `Gistapi` to the GitHub API to pull down each Gist for the target user.
Please don't use a GitHub API client (i.e. using a basic HTTP library like requests or aiohttp or urllib3 is fine but not PyGithub or similar).


## Stretch goals

* Implement a few tests (using a testing framework of your choice)
* In all places where it makes sense, implement data validation, error handling, pagination
* Migrate from `requirements.txt` to `pyproject.toml` (e.g. using [poetry](https://python-poetry.org/))
* Implement a simple Dockerfile
* Implement handling of huge gists
* Set up the necessary tools to ensure code quality (feel free to pick up a set of tools you personally prefer)
* Document how to start the application, how to build the docker image, how to run tests, and (optionally) how to run code quality checkers
* Prepare a TODO.md file describing possible further improvements to the archtiecture:
    - Can we use a database? What for? SQL or NoSQL?
    - How can we protect the api from abusing it?
    - How can we deploy the application in a cloud environment?
    - How can we be sure the application is alive and works as expected when deployed into a cloud environment?
    - Any other topics you may find interesting and/or important to cover


# Running the Application, Executing testcases, and performing Quality Checks
This documentation will guide you through the process of setting up, running, testing, and ensuring the quality of our application.

## 1. Clone the Repository
First, clone the project repository to your local machine:
```commandline
git clone https://github.com/snandkule/backend-coding-challenge.git
```
## 2. Go to the Project Folder
```commandline
cd backend-coding-challenge/
```
## Starting the Application
You can start the application either locally or within a Docker container. Steps for both methods are given below
### A. Starting the Application Locally
#### 1. Install Poetry 
If you haven't already installed Poetry, you can do so using pip:
```commandline
pip install poetry
```
#### 2. Install Dependencies
Install the project's dependencies using poetry by running below command:
```commandline
poetry install
```
#### 3. Run the Application
To start the application locally, run the following command:
```commandline
poetry run flask --app=gistapi:app run
```
The application will be accessible at http://127.0.0.1:5000.

You can specify a different port using the --port option:
```commandline
poetry run flask --app=gistapi:app run --port 8081
```
To run the application on your IP address, use the --host option:
```commandline
poetry run flask --app=gistapi:app run --host=0.0.0.0
```

### B. Starting the Application in a Docker Container
#### 1. Go to Project Directory
Navigate to the backend-coding-challenge directory:
```commandline
cd backend-coding-challenge/
```
#### 2. Build the Docker Image
To Build the Docker image, run below command:
```commandline
docker build -t gistapi .
```
#### 3. Run the Application in Docker Container
To start the application using a Docker container, run the following command:
```commandline
docker run -p 5000:5000 gistapi
```
The application will be available at http://127.0.0.1:5000.

## Running Tests
To develop and run test cases, we are using the Pytest framework. If you want to add test cases, refer to the test cases in the backend-coding-challenge/gistapi/tests folder.

Follow these steps to run the tests:

#### 1. Install pytest and other dependencies
If you haven't already installed the required dependencies, use Poetry:
```commandline
poetry install
```
#### 2. Run Test Cases
Execute the following command to run the test cases:
```commandline
poetry run pytest
```

## Quality Checkers
To maintain code quality and consistent formatting in our project, we are using Pylint and Black.

Follow below steps in order to use the quality checkers:

#### 1. Install Quality Checkers
If you haven't already installed the quality checkers, use Poetry:
```commandline
poetry install
```
#### 2. Run Pylint
If you are not in the project directory, Change the terminal directory to the backend-coding-challenge folder:
```commandline
cd <path-to-folder-containing-backend-coding-challenge-dir>/backend-coding-challenge/
```
You can run Pylint on a specific file or a folder containing multiple files. Use the following command:
```commandline
poetry run pylint <file-path or folder-path>
```
For example, to run Pylint on the gistapi folder:
```commandline
poetry run pylint gistapi/
```
#### 3. Run Black
To format Python files, navigate to the specific folder and execute the below command:
```commandline
poetry run black <file-path or folder-path>
```
For example, to format all files in the current directory:
```commandline
poetry run black .
```

