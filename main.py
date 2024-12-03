import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import streamlit.components.v1 as components
import streamlit.components.v1 as components1
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import requests as rs
import pandas as pd
# placeholder = st.empty()

# actual_email = "email"
# actual_password = "password"

st.write('''<style>
.stSidebar{
    background:#000;
}
.mainmen{
    color:#fff;
}
.foot{
    position:relative;
    color:#fff;
}
.footmain{
    position:fixed;
    bottom:0;
}
</style>''', unsafe_allow_html=True)
with st.sidebar:
    with st.container():
        st.html(
            "<p style='text-align:center;'><img src='https://boko.com.au/wp-content/uploads/2024/12/signature-logo-1-1.jpg' width='160'></p><p style='color:#bffc00;font-size:26px;'>Boko's Ai<br/>Lead Assistant</p><p style='color:#fff; font-size:20px;'>Saved Searches</p><ul class='mainmen' style='color:#fff; font-size:16px;list-style:none;'><li><span>Search Result 1</span></li><li><span>Search Result 2</span></li></ul><div class='foot'><div class='footmain'><p>Settings</p><p>Login / Logout</p><p>&copy; 2024 Boko Digital<br/>Boko's AI Lead Assistant</p></div></div>")
sheet_csv = st.secrets["database_url"]
res = rs.get(url=sheet_csv)
open('database.csv', 'wb').write(res.content)
database = pd.read_csv('database.csv', header=0)

# Create user_state
if 'user_state' not in st.session_state:
    st.session_state.user_state = {
        'name_surname': '',
        'password': '',
        'logged_in': False,
        'user_type': '',
        'mail_adress': '',
        'fixed_user_message': ''
    }

if not st.session_state.user_state['logged_in']:
    # Create login form
    st.write('Login')
    mail_adress = st.text_input('E-Mail')
    password = st.text_input('Password', type='password')
    submit = st.button('Login')

    # Check if user is logged in
    if submit:
        user_ = database[database['mail_adress'] == mail_adress].copy()
        if len(user_) == 0:
            st.error('User not found')
        else:
            if user_['mail_adress'].values[0] == mail_adress and user_['password'].values[0] == password:
                st.session_state.user_state['mail_adress'] = mail_adress
                st.session_state.user_state['password'] = password
                st.session_state.user_state['logged_in'] = True
                st.session_state.user_state['user_type'] = user_['user_type'].values[0]
                st.session_state.user_state['mail_adress'] = user_['mail_adress'].values[0]
                st.session_state.user_state['fixed_user_message'] = user_['fixed_user_message'].values[0]
                st.write('You are logged in')
                st.rerun()
            else:
                st.write('Invalid username or password')
elif st.session_state.user_state['logged_in']:
    # st.write('Welcome to the app')
    # st.write('You are logged in as:', st.session_state.user_state['mail_adress'])
    # st.write('You are a:', st.session_state.user_state['user_type'])
    # st.write('Your fixed user message:', st.session_state.user_state['fixed_user_message'])
    if st.session_state.user_state['user_type'] == 'admin':
        st.title("My first web scrapper")
        url = st.text_input("Enter website url")
        # st.write('')
        # st.table(database)
# Insert a form in the container
# with placeholder.form("login"):
#     st.markdown("#### Enter your credentials")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     submit = st.form_submit_button("Login")

# if submit and email == actual_email and password == actual_password:
#     # If the form is submitted and the email and password are correct,
#     # clear the form/container and display a success message
#     placeholder.empty()
#     st.success("Login successful")

    


    if st.button("Scrape Site"):
        st.write("website scrapping is running now")
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content

        with st.expander("view more content"):
            st.text_area("Dom Content", cleaned_content, height=300)

    if "dom_content" in st.session_state:
        parse_description = st.text_area("Describe what you want to parse?")

        if st.button("Parse Content"):
            st.write("Parsing the content")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
    
# elif submit and email != actual_email or password != actual_password:
#     st.error("Login failed")
# else:
#     pass