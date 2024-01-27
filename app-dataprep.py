import streamlit as st
import pandas as pd
from dataprep.eda import create_report
import streamlit.components.v1 as components
import os


def app(title=None):
    st.set_page_config(layout="wide")
    st.title(title)

    # use OS library to get the current directory
    current_dir = os.getcwd()

    # use OS library to list all files CSV in the current directory
    current_dir = os.listdir(current_dir)
    current_dir = [f for f in current_dir if f.endswith('.csv')]

    # upload file local
    uploaded_file = st.selectbox("Choose a CSV file", current_dir)

    # Add a select box for choosing the separator
    sep = st.selectbox("Select the separator", ("Comma", "Tab", ";", ":"))
    sep = "," if sep == "Comma" else "\t" if sep == "Tab" else ";" if sep == ";" else ":"

    if uploaded_file is not None:
        # Read the CSV data from the uploaded file
        df = pd.read_csv(uploaded_file, sep=sep)
        st.title("Dataframe:")
        st.write(df)

        # Use the analysis function from dataprep module to create a 'DataframeReport' object.
        @st.cache_data
        def generate_report(df):
            report = create_report(df)
            report.save('output.html')
            HtmlFile = open("output.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            return source_code

        # Render the output on a web page.
        if 'source_code' in st.session_state:
            # Se o estado da sessão já existir, recuperamos o valor
            source_code = st.session_state['source_code']
        else:
            # Senão, geramos o relatório e o armazenamos no estado da sessão
            source_code = generate_report(df)
            st.session_state['source_code'] = source_code

        components.html(source_code, height=1200, width=1500, scrolling=True)

app(title='Dataprep Visualization Viz')
