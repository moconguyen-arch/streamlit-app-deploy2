import os
import openai
import streamlit as st
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

# APIキー取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# ==========================
# Streamlit UI
# ==========================
st.set_page_config(page_title="AI専門家アシスタント", page_icon="🤖")
st.title("🤖 AI専門家アシスタント")
st.write("専門家の視点であなたの質問に回答します。")

expert_type = st.radio(
    "相談したい専門家を選んでください：",
    ("心理カウンセラー", "料理専門家", "子育てアドバイザー")
)

user_input = st.text_area("あなたの質問:")

def generate_answer(expert, question):
    if expert == "心理カウンセラー":
        system_prompt = "あなたは優しい心理カウンセラーです。相談者の気持ちに寄り添って回答してください。"
    elif expert == "料理専門家":
        system_prompt = "あなたはプロの料理研究家です。料理の技術やレシピについて具体的に説明してください。"
    elif expert == "子育てアドバイザー":
        system_prompt = "あなたは経験豊富な子育てアドバイザーです。親しみやすく具体的なアドバイスをしてください。"
    else:
        system_prompt = "あなたは知識豊富な専門家です。"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# ==========================
# ボタン処理
# ==========================
if st.button("回答を生成"):
    if user_input.strip():
        with st.spinner("AIが考えています..."):
            try:
                answer = generate_answer(expert_type, user_input)
                st.success("✅ 回答：")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("質問を入力してください。")

st.caption("開発者: 岡本真代 | OpenAI API + Streamlit (ver.1対応)")