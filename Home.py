import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector

st.set_page_config(page_title="Home",page_icon="👋")

names=[]
usernames =[]
passwords = []

def login():
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbproject"
    )
    login = connection.cursor()
    login.execute("CALL spGetLogin()") 
    logindata = login.fetchall()
    for x,y,z in logindata:
        usernames.append(x)
        passwords.append(y)
        names.append(z)
    login.close()
    connection.close()

login()
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'cookie_name', 'signature_key',cookie_expiry_days=1)
name, authentication_status , username= authenticator.login('Login','sidebar')

if authentication_status:
    st.title('Hello ,')
    st.subheader(name)
    st.write('Welcome to Our New Dashboard')
    st.caption('Powered with Face Authentication by Andre')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 