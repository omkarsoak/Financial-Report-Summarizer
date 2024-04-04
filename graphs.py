import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from edgar_functions import *


def applGraphs():
    annual = annual_facts("AAPL",headers)
    annual = annual.T[['Assets',
    'Assets, Current',
    'Liabilities',
    'Liabilities, Current',

    'Common Stock, Shares Authorized',
    'Common Stock, Shares, Outstanding',
    'Common Stock, Dividends, Per Share, Declared',
    'Gross Profit',
    'Net Income (Loss) Attributable to Parent',
    'Earnings Per Share, Basic',
    'Earnings Per Share, Diluted',
    'Operating Income (Loss)',]]


    # Graph 1
    st.subheader("Earnings Per Share")

    basic = annual['Earnings Per Share, Basic']
    diluted = annual['Earnings Per Share, Diluted']

    plt.figure(figsize=(10, 6))
    plt.plot(annual.index, basic, marker='o', linestyle='-', color='blue', label='Earnings Per Share, Basic')
    plt.plot(annual.index, diluted, marker='o', linestyle='-', color='red', label='Earnings Per Share, Diluted')

    plt.xlabel('Date')  # Assuming your index represents dates
    plt.ylabel('Earnings Per Share')
    plt.title('EPS over time')
    plt.legend()

    st.pyplot(plt)


    #Graph 2
    st.subheader("Graph 2: Assets, Assets Current, Liabilities Current")

    assets = annual['Assets']
    current_assets = annual['Assets, Current']
    current_liabilities = annual['Liabilities, Current']
    plt.figure(figsize=(10, 6))

    # Plotting each column
    plt.plot(annual.index, assets, label='Assets')
    plt.plot(annual.index, current_assets, label='Assets, Current')
    plt.plot(annual.index, current_liabilities, label='Liabilities, Current')


    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Assets, Assets Current, Liabilities Current Over Time')
    plt.legend()

    st.pyplot(plt)


    #Graph 3
    st.subheader("Graph 3: Operating income, net income, gross profit")

    operating_income = annual['Operating Income (Loss)']
    net_income = annual['Net Income (Loss) Attributable to Parent']
    gross_profit = annual['Gross Profit']

    plt.figure(figsize=(10, 6))

    plt.plot(annual.index, operating_income, label='Operating Income (Loss)')
    plt.plot(annual.index, net_income, label='Net Income (Loss) Attributable to Parent)')
    plt.plot(annual.index, gross_profit, label='Gross Profit')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Operating Income, Net Income, Gross Profit Over Time')
    plt.legend()

    st.pyplot(plt)

def nvdaGraphs():

    # Fetching annual financial data for NVDA
    annual = annual_facts("NVDA", headers)
    annual = annual.T[['Assets',
                    'Assets, Current',
                    'Liabilities',
                    'Liabilities, Current',
                    'Common Stock, Shares Authorized',
                    'Common Stock, Shares, Outstanding',
                    'Common Stock, Dividends, Per Share, Declared',
                    'Gross Profit',
                    'Net Income (Loss) Attributable to Parent',
                    'Earnings Per Share, Basic',
                    'Earnings Per Share, Diluted',
                    'Operating Income (Loss)']]

    # Graph 1: Earnings Per Share
    st.subheader("Earnings Per Share")

    basic = annual['Earnings Per Share, Basic']
    diluted = annual['Earnings Per Share, Diluted']

    plt.figure(figsize=(10, 6))
    plt.plot(annual.index, basic, marker='o', linestyle='-', color='blue', label='Earnings Per Share, Basic')
    plt.plot(annual.index, diluted, marker='o', linestyle='-', color='red', label='Earnings Per Share, Diluted')

    plt.xlabel('Date')
    plt.ylabel('Earnings Per Share')
    plt.title('EPS over time')
    plt.legend()

    st.pyplot(plt)

    # Graph 2: Assets, Assets Current, Liabilities Current
    st.subheader("Graph 2: Assets, Assets Current, Liabilities Current")

    assets = annual['Assets']
    current_assets = annual['Assets, Current']
    current_liabilities = annual['Liabilities, Current']

    plt.figure(figsize=(10, 6))

    # Plotting each column
    plt.plot(annual.index, assets, label='Assets')
    plt.plot(annual.index, current_assets, label='Assets, Current')
    plt.plot(annual.index, current_liabilities, label='Liabilities, Current')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Assets, Assets Current, Liabilities Current Over Time')
    plt.legend()

    st.pyplot(plt)

    # Graph 3: Operating income, net income, gross profit
    st.subheader("Graph 3: Operating income, net income, gross profit")

    operating_income = annual['Operating Income (Loss)']
    net_income = annual['Net Income (Loss) Attributable to Parent']
    gross_profit = annual['Gross Profit']

    plt.figure(figsize=(10, 6))

    plt.plot(annual.index, operating_income, label='Operating Income (Loss)')
    plt.plot(annual.index, net_income, label='Net Income (Loss) Attributable to Parent)')
    plt.plot(annual.index, gross_profit, label='Gross Profit')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Operating Income, Net Income, Gross Profit Over Time')
    plt.legend()

    st.pyplot(plt)

def googGraphs():
    # Fetching annual financial data for TSLA
    annual = annual_facts("GOOG",headers)
    annual = annual.T[['Assets',
    'Assets, Current',
    'Liabilities',
    'Liabilities, Current',

    'Common Stock, Shares Authorized',
    'Common Stock, Shares, Outstanding',
    'Common Stocks, Including Additional Paid in Capital',
    #'Gross Profit',
    'Net Income (Loss) Attributable to Parent',
    'Earnings Per Share, Basic',
    'Earnings Per Share, Diluted',
    'Operating Income (Loss)',]]

    annual

    # Graph 1: Earnings Per Share
    st.subheader("Earnings Per Share")

    basic = annual['Earnings Per Share, Basic']
    diluted = annual['Earnings Per Share, Diluted']

    plt.figure(figsize=(10, 6))
    plt.plot(annual.index, basic, marker='o', linestyle='-', color='blue', label='Earnings Per Share, Basic')
    plt.plot(annual.index, diluted, marker='o', linestyle='-', color='red', label='Earnings Per Share, Diluted')

    plt.xlabel('Date')
    plt.ylabel('Earnings Per Share')
    plt.title('EPS over time')
    plt.legend()

    st.pyplot(plt)

    # Graph 2: Assets, Assets Current, Liabilities Current
    st.subheader("Graph 2: Assets, Assets Current, Liabilities Current")

    assets = annual['Assets']
    current_assets = annual['Assets, Current']
    current_liabilities = annual['Liabilities, Current']

    plt.figure(figsize=(10, 6))

    # Plotting each column
    plt.plot(annual.index, assets, label='Assets')
    plt.plot(annual.index, current_assets, label='Assets, Current')
    plt.plot(annual.index, current_liabilities, label='Liabilities, Current')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Assets, Assets Current, Liabilities Current Over Time')
    plt.legend()

    st.pyplot(plt)

    # Graph 3: Operating income, net income, gross profit
    st.subheader("Graph 3: Operating income, net income")#, gross profit")

    operating_income = annual['Operating Income (Loss)']
    net_income = annual['Net Income (Loss) Attributable to Parent']
    #gross_profit = annual['Gross Profit']

    plt.figure(figsize=(10, 6))

    plt.plot(annual.index, operating_income, label='Operating Income (Loss)')
    plt.plot(annual.index, net_income, label='Net Income (Loss) Attributable to Parent)')
    #plt.plot(annual.index, gross_profit, label='Gross Profit')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Operating Income, Net Income Over Time')#, Gross Profit Over Time')
    plt.legend()

    st.pyplot(plt)



def graph(ticker):
    headers = {"User-Agent": "abc@example.com"}
    if(ticker == "AAPL"):
        applGraphs()
    elif(ticker == "NVDA"): 
        nvdaGraphs()
    elif(ticker == "GOOG"):
        googGraphs()
