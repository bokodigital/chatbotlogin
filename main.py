import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import streamlit.components.v1 as components
import streamlit.components.v1 as components1
st.write('''<style>
.stSidebar{
    background:#000;
}
.mainmen{
    color:#fff;
}
</style>''', unsafe_allow_html=True)
with st.sidebar:
    with st.container():
        st.html(
            "<p><img src='https://boko.com.au/wp-content/uploads/2023/01/Boko-digital-logo-V5-2022.svg' width='160'></p><ul class='mainmen'><li>Login</li><li>About</li></ul>")

st.title("My first web scrapper")
url = st.text_input("Enter website url")


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
        
