import streamlit as st
from agents import student_staregraph
from langchain_core.messages import HumanMessage
from tools import data_generation
from utils import get_chat_messages
from PIL import Image

GRAPH_SETTINGS={"configurable":{"thread_id":"5"},"recursion_limit":50,"stream_mode":True}

st.title('Welcome to Student Report Card')
# st.write('You have to choose ID number of student and get information of student')
st.write("Please select an ID and choose an action.")


student_id=st.selectbox("Choose ID number",list(range(1,201)))
student_json=data_generation.invoke({"user_id":student_id})
student_data=student_json[0]

#user_query
user_query=f"Give me details of student whos id is {student_id}"

#create object of state graph
app=student_staregraph(student_data,user_query)

#calling 
messages=get_chat_messages(
    user_query=user_query,state_graph=app,config=GRAPH_SETTINGS
)
img_path=messages['graph']['image_location']
name=messages['graph']['info']['Name']
col1,col2,col3=st.columns(3)


with col1:
    if st.button("Analysis"):
        st.subheader("Analysis Result")
        st.write(f"Displaying analysis for Student ID : {student_id}",messages['analysis_output'])

with col2:
    if st.button("Summary"):
        st.subheader("Summary Result")
        st.write(f"Displaying summary for Student ID : {student_id}",messages['summary'])

with col3:
    if st.button("Graph"):
        st.subheader("Graph Result")
        st.write(f"Displaying graph for Student ID : {student_id}")
        image=Image.open(img_path)
        st.image(image, caption=f"{name} Report", width=None, use_container_width=True, clamp=False, channels="RGB", output_format="auto")
            




