###### Simplified version of the app to run in terminal ######

import os
import argparse
from utils.model import run_summarization #all tf-idf functions are here

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="TF-IDF Summarizer")
    parser.add_argument('--ticker', type=str, required=True, help='Ticker symbol (e.g., GOOG)')
    parser.add_argument('--n', type=float, default=1.0, help='Degree of summarization (default: 1.0)')
    args = parser.parse_args()

    ticker = args.ticker
    partName = 'partI'
    n = args.n

    if not os.path.exists("./tf-idf-summary"):
        print("Creating directory...")
        os.mkdir("./tf-idf-summary")

    with open(f"./Dataset_Converted/{ticker}/{partName}.txt", "r") as file:
        text_str = file.read()

    result = run_summarization(text_str, n)
    path = f"tf-idf-summary/{ticker.lower()}-{partName}.txt"
    with open(path, 'w') as f1:
        f1.write(result)
    print("DONE.")
