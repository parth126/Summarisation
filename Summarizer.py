from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer


import os
from bs4 import BeautifulSoup
import glob
import nltk.data
runId = "lex20"
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
for filename in glob.glob("*.judgement"):
    f = ""
    with open(filename,"r") as myfile:
        f = myfile.read()
    
    parser = PlaintextParser.from_string(f, Tokenizer("english"))

    sentences = sent_detector.tokenize(f)
    n_sentences = len(sentences)
    n_summary = 0.2*n_sentences
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, n_summary)
    summary_str = ""
    for sentence in summary:
        summary_str += str(sentence)
    print summary_str
    fname = filename[0:len(filename)-10]
    
    fop = open("summaries/"+fname+"."+runId, "w")
    fop.write(summary_str)


    '''
    #Use 20% for summarisation
    parser = PlaintextParser.from_file(filename, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 6)
    summary_str = ""
    for sentence in summary:
        summary_str += str(sentence)
    fname = filename[0:len(fname)-10]
    fname += runId 
    print summary_str
    fop = open("summaries/"+filename, "w")

    fop.write(summary_str)

    '''
