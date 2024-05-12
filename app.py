import streamlit as st
import time
from edgar_functions import *
from graphs import *
from utils import run_summarization

def nextpage():
    st.session_state.page += 1

def restart():
    st.session_state.clear()
    st.session_state.page = 0

st.title("SEC Filing Summarizer")
st.write('\n\n')

if "page" not in st.session_state:
    st.session_state.page = 0

if st.session_state.page == 0:  # Page 0: Ticker selection
    print("Page 0: Ticker selection")
    ticker = st.selectbox("Please choose a ticker", ['AAPL', 'GOOG', 'NVDA', 'TSLA'], index=None)
    st.write("Select the Degree of summarization: \n\n  0: Large summary \n\n  1: Medium summary \n\n  2: Small summary\n")
    n = st.slider("",0.1, 2.0, 1.0, 0.1, label_visibility='hidden') 
    if st.button("Select"):
        st.session_state.ticker = ticker
        st.session_state.n = n
        print(f"Current page: {st.session_state.page}")
        nextpage()
        print(f"New page: {st.session_state.page + 1}")


elif st.session_state.page == 1:  # Page 1: Summary generation
    print("Page 1.1: Summary generation")
    if "results" not in st.session_state:
        st.session_state.results = {}

        parts = ['partI', 'item7A', 'item9A']
        
        for part in parts:
            file_path = f"./Dataset_Converted/{st.session_state.ticker}/{part}.txt"
            with open(file_path, "r") as file:
                text_str = file.read()

            with st.spinner(f"Summarizing {part} with degree of summarization {st.session_state.n}..."):
                time.sleep(3)  # Placeholder for actual summarization function
                result = run_summarization(text_str, st.session_state.n)

            st.session_state.results[part] = result

    for part, result in st.session_state.results.items():
        st.write(f"Summary for {part}:")
        st.write(result)
    
    if st.button("Next"):
        print(f"Current page: {st.session_state.page}")
        nextpage()
        print(f"New page: {st.session_state.page + 1}")

elif st.session_state.page == 2:  # Page 4: Display graphs
    print("Page 4: Display graphs")
    if "graphs_generated" not in st.session_state:
        with st.spinner("Plotting!"):
            time.sleep(3)
            st.session_state.graphs_generated = True
    if st.session_state.ticker == "AAPL":
        applGraphs()
    elif st.session_state.ticker == "NVDA":
        nvdaGraphs()
    elif st.session_state.ticker == "GOOG":
        googGraphs()
    if st.button("Next"):
        print(f"Current page: {st.session_state.page}")
        nextpage()
        print(f"New page: {st.session_state.page + 1}")

else:  # End of pages
    print("End of pages")
    st.write("Go back to home page:")
    if st.button("Restart"):
        print(f"Current page: {st.session_state.page}")
        restart()
        print(f"New page: {st.session_state.page}")