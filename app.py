import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader



st.set_page_config(page_title="LangChain: Webpage Summarizer", page_icon="📝✨")
st.title("📝✨LangChain: Summarize Text From Any Website")
st.subheader('Enter the URL to get it summarized ⬇️')




with st.sidebar.expander("Click to open Sidebar", expanded=True):
    groq_api_key = st.text_input('Give the GROQ API Key here!!!', type='password')

generic_url=st.text_input("URL",label_visibility="collapsed")


prompt_template="""
Provide a summary of the following content in 300 words along with a proper title for the content summary:
Content:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the Content from Website"):
    
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid website url")

    else:
        try:
            with st.spinner("Summarizing..."):
                loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=True,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()
                llm =ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

              
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.invoke(docs)

                st.success(output_summary['output_text'])
        except Exception as e:
            st.exception(f"Exception:{e}")
                    
