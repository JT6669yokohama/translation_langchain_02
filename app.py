# 以下を「app.py」に書き込み
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai_api_key = st.secrets["openai"]["api_key"]
chat = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

# プロンプトのテンプレート
system_template = (
    "あなたは、{source_lang} の {text_type} を {target_lang} に翻訳する優秀な翻訳アシスタントです。翻訳結果以外は出力しないでください。翻訳スタイルは {translation_style} です。"
)
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

if "response" not in st.session_state:
    st.session_state["response"] = ""

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# LLMとやりとりする関数
def communicate():
    text = st.session_state["user_input"]
    try:
        response = chat(
            chat_prompt.format_prompt(
                source_lang=source_lang, target_lang=target_lang, text=text, text_type="一般的な文章", translation_style="丁寧な言葉遣い"
            ).to_messages()
        )
        st.session_state["response"] = response.content
    except Exception as e:
        st.error(f"翻訳中にエラーが発生しました: {e}")
        st.session_state["response"] = ""

# ユーザーインターフェイスの構築
st.title("翻訳アプリ")
st.write("LangChainを使った翻訳アプリです。")

options = ["日本語", "英語", "スペイン語", "ドイツ語", "フランス語", "中国語"]
source_lang = st.selectbox(label="翻訳元", options=options)
target_lang = st.selectbox(label="翻訳先", options=options)
st.text_input("翻訳する文章を入力してください。", key="user_input")
st.button("翻訳", type="primary", on_click=communicate)

if st.session_state["user_input"] != "":
    st.markdown("### 翻訳結果:")
    st.write(st.session_state["response"])
