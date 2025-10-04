import re
import pandas as pd


## Functions for extracting item sections from SEC filings
def extract_items(part_header, part_text, form_type):
    """Extracts the item header and its corresponding text for every item within the plain text of a "part" of a form.
    
    :type part_header: str
    :param part_header: The header of a "part" of a form (e.g. Part III)
    
    :type part_text: str
    :param part_text: The plain text of a "part" of a form (e.g. Part III). In the case of 10-K and 8-K forms, the "part" is the whole form.
    
    :type form_type: str
    :param form_type: The form type (e.g. 10-K, 10-Q, 8-K)

    :rtype: Iterator[(str, str, str)]
    :returns: An iterator over tuples of the form (part_header, item_header, text) 
        where "item_header" is the item header and "text" is the corresponding text
        for each item in the "part". part_header is included to differentiate 
        between portions of a filing that have the same item number but are in different parts.
    """
    if form_type == "10-K" or form_type == "10-Q":
        pattern = '(?P<header>(\n\n(ITEM|Item) \d+[A-Z]*.*?)\n\n)(?P<text>.*?)(?=(\n\n(ITEM|Item) \d+[A-Z]*.*?)\n\n|$)'
    elif form_type == "8-K":
        pattern = '(?P<header>\n\n(ITEM|Item) \d+\.\d+\.*)(?P<text>.*?)(?=((\n\n(ITEM|Item) \d+\.\d+.*?)\n\n|$))'
    return ((part_header, _.group('header').strip(), _.group('text').strip()) for _ in re.finditer(pattern, part_text, re.DOTALL))

## Functions for processing filings dataframe
def extract_parts(form_text, form_type):
    """Extracts every part from form plain text, where a "part" is defined
    specifically as a portion in the form starting with "PART (some roman numeral)".
    
    :type form_text: str
    :param form_text: The form plain text.
    
    :type form_type: str
    :param form_type: The form type (e.g. 10-K, 10-Q, 8-K)
    
    :rtype: Iterator[(str, str)]
    :returns: An iterator over the header and text for each part extracted from the form plain text.
        (e.g. for 10-K forms, we iterate through Part I through Part IV)
    """
    pattern = '((^PART|^Part|\n\nPART|\n\nPart) [IVXLCDM]+).*?(\n\n.*?)(?=\n\n(PART|Part) [IVXLCDM]+.*?\n\n|$)'
    return ((_.group(1).strip(), _.group(3)) for _ in re.finditer(pattern, form_text, re.DOTALL))


def get_form_items(form_text, form_type):
    """Extracts the item header and its corresponding text for every item within a form's plaintext.
    
    :type form_text: str
    :param form_text: The form plain text.
    
    :type form_type: str
    :param form_type: The form type (e.g. 10-K, 10-Q, 8-K)
    
    :rtype: Iterator[(str, str)]
    :returns: An iterator over tuples of the form (header, text) where "header" is the item header and "text" is the corresponding text.
    """
    if form_type == "10-Q":
        for part_header, part_text in extract_parts(form_text, form_type):
            items = extract_items(part_header, part_text, form_type)
            yield from items
    elif form_type == "8-K"  or form_type == "10-K":
        items = extract_items("", form_text, form_type)
        yield from items

## Code for building a dataframe whose columns are the different "Item" sections
def items_to_df_row(item_iter, columns, form_type):
    """Takes an iterator over tuples of the form (header, text) that is created from calling extract_items
    and generates a row for a dataframe that has a column for each of the item types.
    
    :type item_iter: Iterator[(str, str, str)]
    :param item_iter: An iterator over tuples of the form (part_header, item_header, item_text).
    
    :type columns: List[str]
    :param columns: A list of column names for the dataframe we wish to generate a row for.
    
    :type form_type: str
    :param form_type: The form type. Currently supported types include 10-K, 10-Q, 8-K.
    
    :rtype: List[str]
    :returns: A row for the dataframe.
    """
    mapping = {} # mapping between processed column names and their corresponding row index
    for idx, col_name in enumerate(columns):
        processed_col_name = col_name.lower()
        mapping[processed_col_name] = idx
        
    returned_row = ["" for i in range(len(columns))]
    for part_header, item_header, text in item_iter:
        processed_header = (part_header.lower() + " " + item_header.lower()).strip()
        if form_type == "10-Q":
            processed_header = re.search("part [ivxlcdm]+ item \d+[a-z]*", processed_header).group(0)
        elif form_type == "10-K":
            processed_header = re.search("item \d+[a-z]*", processed_header).group(0)
        elif form_type == "8-K":
            if processed_header[-1] == ".":
                processed_header = processed_header[:-1] # Some companies will include a period at the end of the header while others don't        
        if processed_header in mapping.keys():
            row_index = mapping[processed_header]
            returned_row[row_index] = text
            
    return returned_row

## Required hard-coded values for the different Item section header names
columns_10K = ["Item 1", "Item 1A", "Item 1B", "Item 2", "Item 3", "Item 4",
           "Item 5", "Item 6", "Item 7", "Item 7A", "Item 8", "Item 9",
           "Item 9A", "Item 9B", "Item 10", "Item 11", "Item 12", "Item 13",
           "Item 14", "Item 15"]

columns_10Q = ["Part I Item 1", "Part I Item 2", "Part I Item 3", "Part I Item 4",
               "Part II Item 1", "Part II Item 1A", "Part II Item 2", "Part II Item 3",
               "Part II Item 4", "Part II Item 5", "Part II Item 6"]

columns_8K = ["Item 1.01", "Item 1.02", "Item 1.03", "Item 1.04",
             "Item 2.01", "Item 2.02", "Item 2.03", "Item 2.04", "Item 2.05", "Item 2.06",
             "Item 3.01", "Item 3.02", "Item 3.03",
             "Item 4.01", "Item 4.02",
             "Item 5.01", "Item 5.02", "Item 5.03", "Item 5.04", "Item 5.05", "Item 5.06", "Item 5.07", "Item 5.08",
             "Item 6.01", "Item 6.02", "Item 6.03", "Item 6.04", "Item 6.05",
             "Item 7.01",
             "Item 8.01",
             "Item 9.01"]

header_mappings_10K = {
    "Item 1": "Business",
    "Item 1A": "Risk Factors",
    "Item 1B": "Unresolved Staff Comments",
    "Item 2": "Properties",
    "Item 3": "Legal Proceedings",
    "Item 4": "Mine Safety Disclosures",
    "Item 5": "Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
    "Item 6": "Selected Financial Data",
    "Item 7": "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
    "Item 7A": "Quantitative and Qualitative Disclosures about Market Risk",
    "Item 8": "Financial Statements and Supplementary Data",
    "Item 9": "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure",
    "Item 9A": "Controls and Procedures",
    "Item 9B": "Other Information",
    "Item 10": "Directors, Executive Officers and Corporate Governance",
    "Item 11": "Executive Compensation",
    "Item 12": "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters",
    "Item 13": "Certain Relationships and Related Transactions, and Director Independence",
    "Item 14": "Principal Accountant Fees and Services",
    "Item 15": "Exhibits, Financial Statement Schedules"
}

header_mappings_10Q = {
    "Part I Item 1": "Financial Statements",
    "Part I Item 2": "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
    "Part I Item 3": "Quantitative and Qualitative Disclosures About Market Risk",
    "Part I Item 4": "Controls and Procedures",
    "Part II Item 1": "Legal Proceedings",
    "Part II Item 1A": "Risk Factors",
    "Part II Item 2": "Unregistered Sales of Equity Securities and Use of Proceeds",
    "Part II Item 3": "Defaults Upon Senior Securities",
    "Part II Item 4": "Mine Safety Disclosures",
    "Part II Item 5": "Other Information",
    "Part II Item 6": "Exhibits"
}

header_mappings_8K = {
    "Item 1.01": "Entry into a Material Definitive Agreement",
    "Item 1.02": "Termination of a Material Definitive Agreement",
    "Item 1.03": "Bankruptcy or Receivership",
    "Item 1.04": "Mine Safety - Reporting of Shutdowns and Patterns of Violations",
    "Item 2.01": "Completion of Acquisition or Disposition of Assets",
    "Item 2.02": "Results of Operations and Financial Condition",
    "Item 2.03": "Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant",
    "Item 2.04": "Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement",
    "Item 2.05": "Costs Associated with Exit or Disposal Activities",
    "Item 2.06": "Material Impairments",
    "Item 3.01": "Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing",
    "Item 3.02": "Unregistered Sales of Equity Securities",
    "Item 3.03": "Material Modification to Rights of Security Holders",
    "Item 4.01": "Changes in Registrant's Certifying Accountant",
    "Item 4.02": "Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review",
    "Item 5.01": "Changes in Control of Registrant",
    "Item 5.02": "Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers",
    "Item 5.03": "Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year",
    "Item 5.04": "Temporary Suspension of Trading Under Registrant's Employee Benefit Plans",
    "Item 5.05": "Amendment to Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics",
    "Item 5.06": "Change in Shell Company Status",
    "Item 5.07": "Submission of Matters to a Vote of Security Holders",
    "Item 5.08": "Shareholder Director Nominations",
    "Item 6.01": "ABS Informational and Computational Material",
    "Item 6.02": "Change of Servicer or Trustee",
    "Item 6.03": "Change in Credit Enhancement or Other External Support",
    "Item 6.04": "Failure to Make a Required Distribution",
    "Item 6.05": "Securities Act Updating Disclosure",
    "Item 7.01": "Regulation FD Disclosure",
    "Item 8.01": "Other Events",
    "Item 9.01": "Financial Statements and Exhibits"
}

## main function
def process_filings(dataframe, form_type):
    if form_type=='10-K':
            columns = columns_10K
            header_mappings = header_mappings_10K
    elif form_type=='10-Q':
            columns = columns_10Q
            header_mappings = header_mappings_10Q
    elif form_type=='8-K':
            columns = columns_8K
            header_mappings = header_mappings_8K
    else:
            print('Unsupported filing type')
            return None
        
    df = dataframe[dataframe.form_type == form_type]
    items = pd.DataFrame(columns = columns, dtype=object)
    for i in df.index:
        form_text = df.text[i]
        item_iter = get_form_items(form_text, form_type)
        items.loc[i] = items_to_df_row(item_iter, columns, form_type)
    items.rename(columns=header_mappings, inplace=True)
    df = pd.merge(df, items, left_index=True, right_index=True)
    return df