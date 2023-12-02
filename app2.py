from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import time

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

#랭체인 강의 듣기-조코딩
#세션 스테이트(스트림릿)

#thread.id를 관리하기 위함
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# thread_id = st.session_state.thread_id
thread_id = st.session_state.thread_id
assistant_id = "asst_Tm4oToZMp4sgUxuDilVQHyVl"

thread_messages = client.beta.threads.messages.list(thread_id,order="asc")
# print(thread_messages.data)

st.header("현진건 작가님과의 대화, 그리고 CSBP팀의 별명을 물어보세요")

for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)
    # print(msg.role)
    # print(msg.content[0].text.value)

prompt = st.chat_input("물어보고 싶은 것을 입력하세요!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt #수정부
    )
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        #instructions="Please address the user as Jane Doe. The user has a premium account."
    )

    with st.spinner('Wait for it...'):
    
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
        
    )
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
    



    # print(message)
    # st.write(f"User has sent the following prompt: {prompt}")


# message = client.beta.threads.messages.create(
#    thread_id='asst_Tm4oToZMp4sgUxuDilVQHyVl',
#    role="user",
#    content="안녕하세요"
# )

# message list 호출할 때, order="asc"로 넣으면 reversed 대신 사용할 수 있을 것 같습니다. Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.