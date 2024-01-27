import streamlit as st
import pandas as pd
from dataprep.eda import create_report
import streamlit.components.v1 as components
import os

def app(title=None):
    st.set_page_config(layout="wide")
    st.title(title)

    # Use a função st.file_uploader para permitir ao usuário fazer upload de um arquivo CSV
    uploaded_file = st.file_uploader("Choose a CSV file")

    if uploaded_file is not None:
        # Ler os dados CSV do arquivo carregado
        df = pd.read_csv(uploaded_file)
        st.title("Dataframe:")
        st.write(df)

        # Use a função de análise do módulo dataprep para criar um objeto 'DataframeReport'.
        @st.cache_data
        def generate_report(df):
            report = create_report(df)
            report.save('output.html')
            HtmlFile = open("output.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            return source_code

        # Renderizar a saída em uma página web.
        if 'source_code' in st.session_state:
            # Se o estado da sessão já existir, recuperamos o valor
            source_code = st.session_state['source_code']
        else:
            # Senão, geramos o relatório e o armazenamos no estado da sessão
            source_code = generate_report(df)
            st.session_state['source_code'] = source_code

        components.html(source_code, height=1200, width=1500, scrolling=True)

app(title='Dataprep Visualization Viz')
