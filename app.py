from flask import Flask, request, jsonify
import pandas as pd
import os
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

filePath = "data_new.csv"

llm = OpenAI(temperature=0, model="gpt-3.5-turbo-instruct-0914")

df = pd.read_csv(filePath).fillna(0)
df.rename(columns={'category':'ownership_type','registered_address':'address','upper':'turnover_range_upper_boundary','lower':'turnover_range_lower_boundary'}, inplace=True)

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        data = request.get_json()
        reqPrompt = data.get('prompt', '').lower()

        finalPrompt = {
            "input": reqPrompt + ". 1) ignoring case. 2) use includes and not equal for string type datas.",
            "tool_names":["pandas"],
            "tools":{
                "pandas":{
                    "df": df.to_dict()
                }
            }
        }
        
        # Create agent with pandas dataframe
        agent = create_pandas_dataframe_agent(llm, df, verbose=True)
        
        # Invoke the agent with the provided prompt
        answer = agent.invoke(finalPrompt)
        
        return jsonify({"answer": answer.get("output")})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
