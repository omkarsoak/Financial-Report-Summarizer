import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
headers = {"User-Agent": "abc@example.com"}  # Need to add your email address here

pd.options.display.float_format = (
    lambda x: "{:,.0f}".format(x) if int(x) == x else "{:,.2f}".format(x)
)

def cik_matching_ticker(ticker, headers=headers):
    ticker = ticker.upper().replace(".", "-")
    ticker_json = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()

    for company in ticker_json.values():
        if company["ticker"] == ticker:
            cik = str(company["cik_str"]).zfill(10)
            return cik
    raise ValueError(f"Ticker {ticker} not found in SEC database")


def get_submission_data_for_ticker(ticker, headers=headers, only_filings_df=False):
    """
    Get the data in json form for a given ticker. For example: 'cik', 'entityType', 'sic', 'sicDescription', 'insiderTransactionForOwnerExists', 'insiderTransactionForIssuerExists', 'name', 'tickers', 'exchanges', 'ein', 'description', 'website', 'investorWebsite', 'category', 'fiscalYearEnd', 'stateOfIncorporation', 'stateOfIncorporationDescription', 'addresses', 'phone', 'flags', 'formerNames', 'filings'

    Args:
        ticker (str): The ticker symbol of the company.

    Returns:
        json: The submissions for the company.
    """
    cik = cik_matching_ticker(ticker)
    headers = headers
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    company_json = requests.get(url, headers=headers).json()
    if only_filings_df:
        return pd.DataFrame(company_json["filings"]["recent"])
    else:
        return company_json


def get_filtered_filings(
    ticker, ten_k=True, just_accession_numbers=False, headers=None
):
    """
    Retrieves either 10-K or 10-Q filings for a given ticker and optionally returns just accession numbers.

    Args:
        ticker (str): Stock ticker symbol.
        ten_k (bool): If True, fetches 10-K filings; otherwise, fetches 10-Q filings.
        just_accession_numbers (bool): If True, returns only accession numbers; otherwise, returns full data.
        headers (dict): Headers for HTTP request.

    Returns:
        DataFrame or Series: DataFrame of filings or Series of accession numbers.
    """
    # Fetch submission data for the given ticker
    company_filings_df = get_submission_data_for_ticker(
        ticker, only_filings_df=True, headers=headers
    )
    # Filter for 10-K or 10-Q forms
    df = company_filings_df[company_filings_df["form"] == ("10-K" if ten_k else "10-Q")]
    # Return accession numbers if specified
    if just_accession_numbers:
        df = df.set_index("reportDate")
        accession_df = df["accessionNumber"]
        return accession_df
    else:
        return df


def get_facts(ticker, headers=None):
    """
    Retrieves company facts for a given ticker.

    Args:
        ticker (str): Stock ticker symbol.
        headers (dict): Headers for HTTP request.

    Returns:
        dict: Company facts in JSON format.
    """
    # Get CIK number matching the ticker
    cik = cik_matching_ticker(ticker)
    # Construct URL for company facts
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    # Fetch and return company facts
    company_facts = requests.get(url, headers=headers).json()
    return company_facts


def facts_DF(ticker, headers=None):
    """
    Converts company facts into a DataFrame.

    Args:
        ticker (str): Stock ticker symbol.
        headers (dict): Headers for HTTP request.

    Returns:
        tuple: DataFrame of facts and a dictionary of labels.
    """
    # Retrieve facts data
    facts = get_facts(ticker, headers)
    us_gaap_data = facts["facts"]["us-gaap"]
    df_data = []

    # Process each fact and its details
    for fact, details in us_gaap_data.items():
        for unit in details["units"]:
            for item in details["units"][unit]:
                row = item.copy()
                row["fact"] = fact
                df_data.append(row)

    df = pd.DataFrame(df_data)
    # Convert 'end' and 'start' to datetime
    df["end"] = pd.to_datetime(df["end"])
    df["start"] = pd.to_datetime(df["start"])
    # Drop duplicates and set index
    df = df.drop_duplicates(subset=["fact", "end", "val"])
    df.set_index("end", inplace=True)
    # Create a dictionary of labels for facts
    labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
    return df, labels_dict


def annual_facts(ticker, headers=None):
    """
    Fetches and processes annual (10-K) financial facts for a given ticker.

    Args:
        ticker (str): Stock ticker symbol.
        headers (dict): Headers for HTTP request.

    Returns:
        DataFrame: Transposed pivot table of annual financial facts.
    """
    # Get accession numbers for 10-K filings
    accession_nums = get_filtered_filings(
        ticker, ten_k=True, just_accession_numbers=True, headers=headers
    )
    # Extract and process facts data
    df, label_dict = facts_DF(ticker, headers)
    # Filter data for 10-K filings
    ten_k = df[df["accn"].isin(accession_nums)]
    ten_k = ten_k[ten_k.index.isin(accession_nums.index)]
    # Pivot and format the data
    pivot = ten_k.pivot_table(values="val", columns="fact", index="end")
    pivot.rename(columns=label_dict, inplace=True)
    return pivot.T

def quarterly_facts(ticker, headers=None):
    """
    Fetches and processes quarterly (10-Q) financial facts for a given ticker.

    Args:
        ticker (str): Stock ticker symbol.
        headers (dict): Headers for HTTP request.

    Returns:
        DataFrame: Transposed pivot table of quarterly financial facts.
    """
    # Get accession numbers for 10-Q filings
    accession_nums = get_filtered_filings(
        ticker, ten_k=False, just_accession_numbers=True, headers=headers
    )
    # Extract and process facts data
    df, label_dict = facts_DF(ticker, headers)
    # Filter data for 10-Q filings
    ten_q = df[df["accn"].isin(accession_nums)]
    ten_q = ten_q[ten_q.index.isin(accession_nums.index)].reset_index(drop=False)
    # Remove duplicate entries
    ten_q = ten_q.drop_duplicates(subset=["fact", "end"], keep="last")
    # Pivot and format the data
    pivot = ten_q.pivot_table(values="val", columns="fact", index="end")
    pivot.rename(columns=label_dict, inplace=True)
    return pivot.T

