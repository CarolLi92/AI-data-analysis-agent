from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import json

prompt_template = """
You are a data analysis assistant. Your response depends on the user's request.

1. For text-answer questions, answer in this format:
{"answer": "<Write your answer here>"}
For example:
{"answer": "The product ID with the highest order volume is 'MNWC3-067'"}

2. If the user needs a table, answer in this format:
{"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. If the user's request is suitable for returning a bar chart, answer in this format:
{"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. If the user's request is suitable for returning a line chart, answer in this format:
{"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. If the user's request is suitable for returning a scatter plot, answer in this format:
{"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
Note: We only support three types of charts: "bar", "line" and "scatter".

Please return all output as JSON strings. Please note that all strings in the "columns" list and the data list must be enclosed in double quotes.
For example: {"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

The user request you need to handle is as follows:
"""

def dataframe_agent(openai_api_key, df, query):
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key=openai_api_key,
                       base_url="https://api.aigc369.com/v1",
                       temperature=0)
    agent = create_pandas_dataframe_agent(llm=model,
                                          df=df,
                                          agent_executor_kwargs={"handle_parsing_errors":True},
                                          verbose=True)
    prompt = prompt_template + query
    response = agent.invoke({"input":prompt})
    response_dict = json.loads(response["output"])
    return response_dict

import os
import pandas as pd
#df = pd.read_csv("personal_data.csv")
#print(dataframe_agent(os.getenv("OPENAI_API_KEY"),df,"which profession in the csv is most popular and why is the answer"))

