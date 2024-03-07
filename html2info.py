import os
import html2text

def searchFile(filename, phrase):
    with open(filename, 'r') as fp0:
        # read all lines in a list
        lines = fp0.readlines()
        for line in lines:
            line_lc = line.lower() 
            
            # check if string present on a current line
            if line_lc.find(phrase.lower()) != -1:
                #print('Line Number:', lines.index(line))
                #print('Line:', line)
                fp0.close()
                return(lines.index(line))

            fp0.close()
            
    return -1

#Function to extract data
def extract(convertedfile, to_phrase, from_phrase, resultfile):            
    #extract first, last indices
    first = searchFile(convertedfile, to_phrase)
    last = searchFile(convertedfile, from_phrase)
    
    if(first == -1 or last == -1):
        return 0 #failed

    mylines = []     
    fp1 = open(resultfile,"w",encoding="UTF-8")

    with open (convertedfile, 'r') as fp: 
        lines = fp.readlines()[first:last]
    
    for line in lines:
        fp1.write(line)    
    fp1.close()    
    return 1 #successful


if not os.path.exists(f"./Dataset_Converted"):
    os.mkdir(f"./Dataset_Converted")

tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA", "GOOG", "BRK-B", "META", "UNH",
    "XOM", "LLY", "JPM", "JNJ", "V", "PG", "MA", "AVGO", "HD", "CVX", "MRK", "ABBV",
    "COST", "PEP", "ADBE"]

for ticker in tickers:
    inputfile = f"./Dataset_SEC_filings/{ticker}.html"
    if not os.path.exists(f"./Dataset_Converted/{ticker}"):
        os.mkdir(f"./Dataset_Converted/{ticker}")

    convertedfile = f"./Dataset_Converted/{ticker}/converted.txt"

    #Convert HTML file to text file
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    #text_maker.ignore_tables = True

    f1 = open(inputfile,"r")
    html = f1.read()
    #print(html)
    text = html2text.html2text(html)
    #print(text)
    f1.close()

    f2 = open(convertedfile,"w",encoding="UTF-8")
    f2.write(text)
    f2.close()

    #Part 1 Extraction
    if(extract(convertedfile, "Item 1. Business", "Item 5. Market", f"./Dataset_Converted/{ticker}/partI.txt")):
        print(ticker,"Part 1 done")
    else:
        if(extract(convertedfile, "Item 1.Business", "Item 5.Market", f"./Dataset_Converted/{ticker}/partI.txt")):
            print(ticker,"Part 1 done")
        else:
            print(ticker,"Part 1 failed")
    

    #Item 7A Extraction
    if(extract(convertedfile, "Item 7. Management", "Item 7A. Quantitative", f"./Dataset_Converted/{ticker}/item7A.txt")):
        print(ticker,"Item 7A done")
    else:
        if(extract(convertedfile, "Item 7.Management", "Item 7A.Quantitative", f"./Dataset_Converted/{ticker}/item7A.txt")):
            print(ticker,"Item 7A done")
        else:
            print(ticker,"Item 7A failed")

    #Item 9A Extaction
    if(extract(convertedfile, "Item 9A. Controls", "Item 9B. Other", f"./Dataset_Converted/{ticker}/item9A.txt")):
        print(ticker,"Item 9A done")
    else:
        if(extract(convertedfile, "Item 9A.Controls", "Item 9B.Other", f"./Dataset_Converted/{ticker}/item9A.txt")):
            print(ticker,"Item 9A done")
        else:
            print(ticker,"Item 9A failed")
    