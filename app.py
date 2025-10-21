import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import openai

load_dotenv()

# OpenAI APIキー取得
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# LangChain + OpenAI のLLM初期化
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

# ==========================
# Streamlit UI設定
# ==========================
st.set_page_config(page_title="AI専門家アシスタント", page_icon="🤖")
st.title("🤖 AI専門家アシスタント")
st.write("専門家の視点から相談に答えるAIアプリです。質問を入力してください。")

expert_type = st.radio(
    "どの専門家に相談しますか？",
    ("心理カウンセラー", "料理専門家", "子育てアドバイザー")
)

user_input = st.text_area("あなたの質問:")

def get_expert_answer(expert, question):
    if expert == "心理カウンセラー":
        system_prompt = "あなたは共感力の高い心理カウンセラーです。"
    elif expert == "料理専門家":
        system_prompt = "あなたは料理の専門家です。"
    elif expert == "子育てアドバイザー":
        system_prompt = "あなたは子育てアドバイザーです。"
    else:
        system_prompt = "あなたは知識豊富な専門家です。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    response = llm(messages)
    return response.content

# ==========================
# ボタン処理
# ==========================
if st.button("回答を生成"):
    if user_input.strip():
        with st.spinner("AIが考えています..."):
            answer = get_expert_answer(expert_type, user_input)
            st.success("回答:")
            st.write(answer)
    else:
        st.warning("質問を入力してください。")

st.caption("開発者: 岡本真代 | Streamlit + LangChain + OpenAI")