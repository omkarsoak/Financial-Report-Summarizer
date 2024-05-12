import math
import nltk
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
import os
#do ONLY once:
#nltk.download('punkt')
#nltk.download('stopwords')


def _create_frequency_table(text_string) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.

    Removing stop words and making frequency tablefi
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix


def _create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    # Initialize an empty dictionary to store the TF-IDF matrix
    tf_idf_matrix = {}

    # Iterate through each sentence and its corresponding TF and IDF tables
    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), 
                                                    idf_matrix.items()):
        tf_idf_table = {}

        # Iterate through each word and its corresponding TF and IDF values
        for (word1, value1), (word2, value2) in zip(f_table1.items(), 
                                                    f_table2.items()):  
            # Calculate the TF-IDF value for the word and store it in the TF-IDF table
            tf_idf_table[word1] = float(value1 * value2)

        # Store the TF-IDF table for the current sentence in the TF-IDF matrix
        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix



def _score_sentences(tf_idf_matrix) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue


#Find the average score from the sentence value dictionary
def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    
    # Iterate through each entry in the sentenceValue dictionary
    for entry in sentenceValue:
        # Add the value of the current entry to the sumValues
        sumValues += sentenceValue[entry]

    # Calculate the average value of a sentence
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    # Iterate through each sentence in the list of sentences
    for sentence in sentences:
        # Check if the first 15 characters of the sentence exist in the sentenceValue dictionary
        # and if the corresponding value is greater than or equal to the threshold
        if sentence[:15] in sentenceValue and sentenceValue[sentence[:15]] >= (threshold):
            # If the conditions are met, add the sentence to the summary
            summary += " " + sentence
            sentence_count += 1

    return summary



def run_summarization(text, n):

    # 1 Sentence Tokenize
    sentences = sent_tokenize(text)
    total_documents = len(sentences)

    # 2 Create the Frequency matrix of the words in each sentence.
    freq_matrix = _create_frequency_matrix(sentences)

    # 3 Calculate TermFrequency and generate a matrix
    tf_matrix = _create_tf_matrix(freq_matrix)

    # 4 creating table for documents per words
    count_doc_per_words = _create_documents_per_words(freq_matrix)

    # 5 Calculate IDF and generate a matrix
    idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, 
                                    total_documents)

    # 6 Calculate TF-IDF and generate a matrix
    tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)

    # 7 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(tf_idf_matrix)

    # 8 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 9 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, n * threshold)

    return summary
