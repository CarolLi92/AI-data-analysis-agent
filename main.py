import pandas as pd
import streamlit as st
from utils import dataframe_agent

def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
#input_data["data"] - this function can convert it to df so that streamlit can use
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("💡 CSV Data Analysis AI tool")

with st.sidebar:
    openai_api_key = st.text_input("Please enter your OpenAI API key：", type="password")
    st.markdown("[Get OpenAI API key](https://platform.openai.com/account/api-keys)")

data = st.file_uploader("Upload CSV for analysis：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("Original Data"):
        st.dataframe(st.session_state["df"])

query = st.text_area("Please enter your questions about the above table, or data extraction requests, or visualization requirements (support scatter charts, line charts, bar charts):")
button = st.button("Generate answers")

if button and not openai_api_key:
    st.info("Please enter your OpenAI API key")
if button and "df" not in st.session_state:
    st.info("Please upload your file")
if button and openai_api_key and "df" in st.session_state:
    with st.spinner("AI is thinking , please wait"):
        response_dict = dataframe_agent(openai_api_key, st.session_state["df"], query)
        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  columns=response_dict["table"]["columns"]))
        if "bar" in response_dict:
            create_chart(response_dict["bar"], "bar")
        if "line" in response_dict:
            create_chart(response_dict["line"], "line")
        if "scatter" in response_dict:
            create_chart(response_dict["scatter"], "scatter")
