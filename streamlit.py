import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.callbacks import get_openai_callback


def init_page():
    st.set_page_config(
        page_title="AmanoGPT",
        page_icon="🤖"
    )
    st.header("AmanoGPT")
    st.sidebar.title("各種設定")


def init_messages():
    clear_button = st.sidebar.button("会話履歴をクリア", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("モデル", ("GPT-3.5", "GPT-4", "GPT-4o"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
    elif model == "GPT-4":
        model_name = "gpt-4-turbo"
    elif model == "GPT-4o":
        model_name = "gpt-4o"

    # スライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.01とする
    temperature = st.sidebar.slider("ランダム性（Temperature）", min_value=0.0, max_value=2.0, value=0.0, step=0.01)

    return ChatOpenAI(temperature=temperature, model_name=model_name)


def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost


def main():
    api_key = os.getenv('OPENAI_API_KEY')
    print(api_key)
    if not api_key:
        st.error("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")
        return

    init_page()

    llm = select_model()
    init_messages()

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してね！"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## コスト")
    st.sidebar.markdown(f"**トータル: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

    Balloon_button = st.sidebar.button('🎉')
    if Balloon_button:
        st.balloons()
    Snow_button = st.sidebar.button('⛄️')
    if Snow_button:
        st.snow()

if __name__ == '__main__':
    main()
