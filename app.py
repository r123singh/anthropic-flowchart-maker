import streamlit as st 
from utils import *


st.header("🤖 AI-Driven Flowchart Designer🧠", divider=True)
create_tab, see_code_tab, edit_code_tab = st.tabs(["Flowchartify 🛠️", "Mermaid🧜‍♀️", "Editor ✏️"])
st.sidebar.markdown("*Hello👋 {username}*")
api_key = st.sidebar.text_input("Anthropic API Key: ", type='password')
st.sidebar.write( "[Get Anthropic API key](https://platform.openai.com/account/keys)")

# Sidebar content
st.sidebar.markdown(
    """
    ### *Flowchartify🛠️*
    - **AI Flowchart Design from Topic**
    - **Direct Steps to Flowchart**
    ### *Mermaid🧜‍♀️*
    - **Code Mermaid.js from Topic**
    - **Direct Mermaid.js from Steps**
    ### *Editor✏️*
    - **See the live flowchart design as you edit the code**
    """
)

if api_key:
    init_client(api_key)
    

    
with create_tab:
    st.subheader("📝 Text to 📊 Flowchart")
    ttf_options = st.selectbox("Choose Option", ["Topic based Flowchart Generation", "Steps To Flowchart Conversion"])
    if ttf_options.lower() == "topic based flowchart generation":
        with st.form("topic_flow_form"):
            description = st.text_input("Topic")
            theme = st.selectbox("Theme", ["Forest", "Dark", "Default"], key="topic_flow_sln")
            submitted = st.form_submit_button("📜➡️📊 Generate",type="primary", use_container_width=True)
            if not api_key:
                st.info("Please enter Anthropic API Key to continue!")
            elif submitted and theme:
                mermaid, explanation = process_query(description)
                customCode = custom_code(theme, mermaid)
                st.components.v1.html(html_code(mermaid), height = 500, scrolling = True )
                with st.popover("Download HTML", use_container_width=True, icon="📥"):
                    st.markdown("Downloads👋")
                    filename = st.text_input("What's the HTML file name?", key="html_file_name")
                    # Display a message based on user input
                    if not filename:
                        st.info("Please enter an HTML file name.")
                    else:
                        dlink = processDownload(customCode, filename, ".html")
                        st.write(f"Your file is ready: [Link]({dlink})")
                st.markdown(explanation)                        
    elif ttf_options.lower() == "steps to flowchart conversion":
        stepsInput = st.text_area("Enter Steps", height=150, placeholder= """
                                   1. User enters name and password
                                   2. Clicks login button
                                   3. If Valid user then continue
                                    //
                                   """)
        theme = st.selectbox("Theme",["Forest", "Dark", "Default"], key="steps_flow_sln" )
        submitted = st.button("📝➡️📊 Convert", key="convert_step_btn", type="primary", use_container_width=True)
        if not api_key:
            st.info("Please enter Anthropic API Key to continue!")
        elif submitted and theme:
            mermaid = process_steps_query(stepsInput)
            customCode = custom_code(theme, mermaid)
            st.components.v1.html(html_code(mermaid), height = 500, scrolling = True)
            
with see_code_tab:
    st.subheader("Text to Mermaid")
    ttm_options = st.selectbox("Choose option", ["Topic Based Code Generation", "Steps To Code Conversion"])
    if ttm_options.lower() == "topic based code generation":
        description = st.text_input("Topic", key="only_code_tab")
        submitted = st.button("📜➡️🧜‍♀️💻 Generate",key="view_topic_code_btn", type="primary", use_container_width=True)
        if not api_key:
            st.info("Please enter Anthropic API Key to continue!")
        elif submitted:
            mermaid, explanation = process_query(description)
            st.code(mermaid)
            st.markdown(explanation)
    elif ttm_options.lower() == "steps to code conversion":
        stepsInput = st.text_area("Enter Steps", height=150, placeholder= """
                                   1. User enters name and password
                                   2. Clicks login button
                                   3. If Valid user then continue
                                    //
                                   """, key="steps_code_inputs")
        submitted = st.button("📝➡️🧜‍♀️💻 Convert",key="view_steps_code_btn", type="primary", use_container_width=True)
        if not api_key:
            st.info("Please enter Anthropic API Key to continue!")
        elif submitted:
            mermaid = process_steps_query(stepsInput)
            st.code(mermaid)        

with edit_code_tab:
    st.subheader("Mermaid to Flowchart")
    mermaid_code = st.text_area(
        "Enter your Mermaid.js code:",
        """
        flowchart TD
            A[Start] --> B{Decision?}
            B -->|Yes| C[Continue]
            B -->|No| D[Stop]
        """,
        height=150
    )
    theme = st.selectbox("Theme:", ["Forest", "Dark", "Default"], key="code_edit_sln")
    if mermaid_code and theme:
        customCode = custom_code(theme, mermaid_code)   
        html_code = html_code(customCode)
        st.components.v1.html(html_code, height=500)