import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Initialize the LLaMA model outside the function to avoid reloading it every time
llm = CTransformers(
    model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
    model_type='llama',
    config={'max_new_tokens': 256, 'temperature': 0.01}
)

# Function to get response from LLaMA 2 Model
def getLLamaresponse(input_text, no_words, blog_style):
    try:
        # Ensure no_words is an integer
        no_words = int(no_words)
        if no_words <= 0:
            st.error("Number of words should be a positive integer.")
            return ""
    except ValueError:
        st.error("Number of words should be a positive integer.")
        return ""
    
    # Prompt Template
    template = f"""
    Write a blog for {blog_style} job profile for a topic {input_text}
    within {no_words} words.
    """

    prompt = PromptTemplate(
        input_variables=["blog_style", "input_text", 'no_words'],
        template=template
    )

    try:
        # Generate response from LLama 2 Model
        response = llm(prompt.format(
            style=blog_style, 
            text=input_text, 
            no_words=no_words
        ))
        return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return ""

st.set_page_config(
    page_title="Generate Blogs",
    page_icon='🤖',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the blog topic")

# Creating two more columns for additional 2 fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

with col2:
    blog_style = st.selectbox('Writing the blog for', ('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate")

# Final Response
if submit:
    if input_text and no_words:
        response = getLLamaresponse(input_text, no_words, blog_style)
        if response:
            st.write(response)
    else:
        st.error("Please fill in all the fields.")

# To run : streamlit run app.py
