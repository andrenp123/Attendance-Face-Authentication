import streamlit as st
import mysql.connector

def insertemployee(usr,name,jabatan):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbproject"
    )
    mycursor = connection.cursor()
    variable=[usr,name,jabatan]
    mycursor.callproc('spInsertPegawai',variable)
    connection.commit()
    mycursor.close()
    connection.close()

def format_labels(option):
    return listjabatan[option]

name=st.session_state['name']
authentication_status=st.session_state['authentication_status']
username=st.session_state['username']

if authentication_status==True and username=='controller':
    listjabatan = {0: "Administrator", 1: "Direktur Utama", 2: "Manager", 3: "Supervisor" ,4: "Staff"}
    st.subheader('Input New Employee Page')
    name = st.text_input("Name")
    usr= st.text_input("Username")
    jabatan = st.selectbox("Position : ", options=list(listjabatan.keys()), format_func=format_labels)
    uploaded_files = st.file_uploader("Upload Identity Image Files (5)", accept_multiple_files=True)
    submit=st.button('Submit')
    if submit:
        if len(uploaded_files)<5:
            st.warning("You only upload %s files" %(len(uploaded_files)))
        else:
            insertemployee(usr,name,jabatan)
            dir='./database/%s' %(usr)
            os.mkdir(dir)
            files=0
            for uploaded_file in uploaded_files:
                if files==5:
                    break
                with open(os.path.join(dir,uploaded_file.name),"wb") as f:
                    f.write(uploaded_file.getbuffer())
                files=files+1
            st.success('Success ! New Employee Recorded')
elif authentication_status==True:
    st.warning("You can't access Administration Page")
else:
    st.warning('Please Login from Home Menu')








hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 