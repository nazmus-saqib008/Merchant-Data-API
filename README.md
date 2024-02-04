# Merchent Data API
This repository contains an experimental API for LangChain, integrating OpenAI's language model for advanced linguistic applications. The API is built using Flask and leverages the capabilities of both LangChain and OpenAI.

### Installation
To set up the project, follow these steps:

Install required Python packages using pip:

```bash
pip install langchain_experimental langchain_openai pandas flask tabulate python-dotenv
```
Create a .env file in the project root directory and set your OpenAI API key:

``` bash
OPENAI_API_KEY=sk-...
```
Set up a virtual environment named api-venv:

```bash
python -m venv api-venv
```
Disable certain lines in 
```bash 
api-venv\Lib\site-packages\langchain\agents\react\agent.py
```
 for experimentation by commenting out lines 93 to 97.


### Run the API using the following command:

``` bash
python app.py
```
This will start the Flask server, and the API will be accessible at http://localhost:5000.
