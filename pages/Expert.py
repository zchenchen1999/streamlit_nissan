# %%
import openai
import streamlit as st
import os
import sys 
# sys.path.append("..")
from Code import expert
# %%
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

## ============================load key================================##
import configparser
from streamlit_modal import Modal
import streamlit.components.v1 as components
# # 設置 API KEY
# config = configparser.ConfigParser()
# config.read('config.ini')
# os.environ["OPENAI_API_KEY"] = config['OPEN_AI']['API_KEY']

st.title("💬 Expert")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "我可以幫您什麼？"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # response = expert.Inference(st.session_state.messages)
    response, retrieval_articles = expert.Inference(prompt)
    # msg = response.choices[0].message
    msg = {
        "content": response['result'],
        "role": "assistant",
        "article":retrieval_articles
      }
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])

modal = Modal(key="Demo Modal", title='相關評論')
open_modal = st.button("Open", key="custom_button")
if open_modal:
    modal.open()
if modal.is_open():
    with modal.container():
        if(len(st.session_state.messages[-1]['article']) > 0 ):
            html_string = ""
            for article in st.session_state.messages[-1]['article']:
                html_string+= f'''
                    <h3>參考文章</h3>
                    {article}
                    <br>
                '''
            components.html(html_string, height=300, scrolling=True)
                # st.markdown(f"參考文章:{article}")
        else:
            # st.markdown('尚無相關評論內容')
            components.html('尚無參考文章', height=100, scrolling=True)
st.markdown(
    """
    <style>
    .streamlit-modal-content {
        width: 500px;  /* 設定寬度 */
        
    }
    </style>
    """,
    unsafe_allow_html=True
)
#height: 200px; /* 設定高度 */