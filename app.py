from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = Flask(__name__)

filePath = "data_new.csv"

# creating an instance to make a call to Large Language Model
llm = OpenAI(temperature=0.2, model="gpt-3.5-turbo-instruct-0914")
# llm = ChatGoogleGenerativeAI(model="gemini-pro")

# read the CSV file
df = pd.read_csv(filePath).fillna(0)

# preprocessed the data by renaming some columns 
df.rename(columns={'category':'ownership_type','nature_of_business':'business_sector','registered_address':'address','upper':'turnover_range_upper_boundary','lower':'turnover_range_lower_boundary'}, inplace=True)



# Flask Server endpoint to generate answer for a prompt
@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        # collected the prompt from request
        data = request.get_json()
        reqPrompt = data.get('prompt', '').lower()
        
        # Created langchain agent with pandas dataframe
        # This agent will run in loop to find satisfying result from dataframe
        agent = create_pandas_dataframe_agent(llm, df, verbose=True)
        
        # Invoked the agent with the provided prompt adding some more prompts for optimisation
        answer = agent.invoke(reqPrompt + ". 1) ignoring case. 2) use contains and not equal for string type datas.")
        
        # Response passed through JSON
        return jsonify({"answer": answer.get("output")})
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
