import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Attendance Report Page",page_icon="👋")


name=st.session_state['name']
authentication_status=st.session_state['authentication_status']
username=st.session_state['username']
absensi=[]

def format_labels(option):
    return month[option]

def selectmasuk(date):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbproject"
    )
    mycursor = connection.cursor()
    mycursor.execute("CALL spChecker('%s','masuk','%s')" %(username,date)) 
    result = mycursor.fetchone()
    for x in result:
        absensi.append(x)
    mycursor.close()
    connection.close()

def selectabsen(date):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbproject"
    )
    mycursor = connection.cursor()
    mycursor.execute("CALL spChecker('%s','absen','%s')" %(username,date)) 
    result = mycursor.fetchone()
    for x in result:
        absensi.append(x)
    mycursor.close()
    connection.close()


if authentication_status==True and username=='controller':
    st.warning("Controller can't access Attendance Report Menu")

elif authentication_status:
    st.subheader('Your Attendance Report')
    month = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May" , 6: "June" , 7: "July" , 8: "August" , 9: "September" , 10: "October", 11: "November", 12:"December"}
    date = st.selectbox("Select Month", options=list(month.keys()), format_func=format_labels)
    if date:
        selectmasuk(date)
        selectabsen(date)
        if sum(absensi) !=0:
            labels=['Tepat Waktu','Terlambat']
            colors = ['#3CB371','#FF0000']
            fig1, ax1 = plt.subplots()
            ax1.pie(absensi, colors = colors, labels=labels, explode=(0.05,0.05),pctdistance=0.85, autopct='%1.1f%%', startangle=90)
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            ax1.axis('equal') 
            plt.title('Your Attendance Report in %s \n\n' %(format_labels(date))) 
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning('No Attendance Report')

    

elif authentication_status == None:
    st.warning('Please Login from Home Menu')



hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 