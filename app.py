from dotenv import load_dotenv
import os
import streamlit as st

# .env を読み込む
load_dotenv()

# APIキー取得
api_key = os.getenv("OPENAI_API_KEY")

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # または "gpt-4o-mini"
    openai_api_key=api_key,
    temperature=0.7
)
from langchain.schema import SystemMessage, HumanMessage

# ==========================
# Streamlit App 設定
# ==========================
st.set_page_config(page_title="AI専門家アシスタント", page_icon="🤖")

st.title("🤖 AI専門家アシスタント")
st.write("""
このアプリでは、AIに「専門家」として質問に回答させることができます。  
下のラジオボタンで専門家の種類を選択し、質問を入力してみましょう！
""")

# ==========================
# LangChain LLM設定
# ==========================
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=api_key, 
    temperature=0.7
)

# ==========================
# 専門家タイプを選択
# ==========================
expert_type = st.radio(
    "どの専門家に相談しますか？",
    ("心理カウンセラー", "料理専門家", "子育てアドバイザー")
)

# ==========================
# 質問入力
# ==========================
user_input = st.text_area("あなたの質問を入力してください:")

# ==========================
# LLMインスタンス作成
# ==========================
def get_expert_answer(expert: str, question: str) -> str:
    """専門家タイプと質問を引数に取り、LLMからの回答を返す。"""
    
    if expert == "心理カウンセラー":
        system_prompt = "あなたは共感力の高い心理カウンセラーです。相談者の気持ちを理解し、前向きな気づきを与えるような助言をしてください。"
    elif expert == "料理専門家":
        system_prompt = "あなたは料理の専門家です。レシピ、調理法、食材の選び方などについて具体的かつわかりやすくアドバイスしてください。"
    elif expert == "子育てアドバイザー":
        system_prompt = "あなたは子育てアドバイザーです。育児の悩みや教育、日常生活のアドバイスを親しみやすく提供してください。"
    else:
        system_prompt = "あなたは知識豊富な専門家です。質問に誠実に答えてください。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    response = llm(messages)
    return response.content

# ==========================
# ボタン実行
# ==========================
if st.button("回答を生成"):
    if user_input.strip():
        with st.spinner("AIが考えています..."):
            answer = get_expert_answer(expert_type, user_input)
            st.success("回答:")
            st.write(answer)
    else:
        st.warning("質問を入力してください。")

st.caption("開発者: 岡本真代 | Python 3.11 / Streamlit + LangChain")