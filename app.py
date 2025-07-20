import streamlit as st

from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# OpenAI APIキー
import os
openai_api_key = os.getenv("OPENAI_API_KEY")  # 

# LLM 初期化（gpt-3.5-turbo）
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo", openai_api_key=openai_api_key)

# システムプロンプト定義
system_prompts = {
    "栄養アドバイザー": "あなたは経験豊富な栄養アドバイザーです。年齢・性別・生活習慣に応じて、健康的な食事や栄養バランスについて分かりやすくアドバイスしてください。専門用語は使いすぎず、日常生活に取り入れやすい具体的な提案を行ってください。",
    "睡眠コンサルタント": "あなたはプロフェッショナルな睡眠コンサルタントです。ユーザーの生活リズムや悩みに合わせて、より良い睡眠環境や習慣の整え方を優しく丁寧に提案してください。医療行為は避け、生活改善の視点でアドバイスを行ってください。",
    "パーソナルトレーナー": "あなたは信頼できるパーソナルトレーナーです。運動習慣を身につけたい人に対して、目的や体力に応じたトレーニングやストレッチを提案してください。初心者にも分かりやすく、安全を第一に考えた指導を心がけてください。",
}

# 回答生成関数
def generate_response(user_input, expert_type):
    system_message = SystemMessage(content=system_prompts[expert_type])
    human_message = HumanMessage(content=user_input)
    response = llm([system_message, human_message])
    return response.content

# 画面構成
st.set_page_config(page_title="生活改善アドバイザー", layout="centered")

st.title("🧠 生活改善アドバイザー")
st.markdown("""
このアプリでは、3つの専門家（栄養アドバイザー・睡眠コンサルタント・パーソナルトレーナー）の知識を活用して、
あなたの生活改善をサポートします。質問を入力して送信すると、専門家からのアドバイスが返ってきます。
""")

# 入力フォーム
with st.form(key="chat_form"):
    user_input = st.text_area("ご相談内容を入力してください", height=150)
    expert_type = st.radio(
        "専門家の種類を選んでください",
        options=["栄養アドバイザー", "睡眠コンサルタント", "パーソナルトレーナー"],
        index=0
    )
    submit_btn = st.form_submit_button("送信")

# 応答表示
if submit_btn and user_input:
    with st.spinner("アドバイスを生成中..."):
        response = generate_response(user_input, expert_type)
        st.success("✅ アドバイスはこちらです")
        st.markdown(response)
