from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer


import os
from bs4 import BeautifulSoup
import glob

for filename in glob.glob("*.txt"):
    parser = PlaintextParser.from_file(filename, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 6)
    summary_str = ""
    for sentence in summary:
        summary_str += str(sentence)

    print summary_str
    fop = open("summaries/"+filename, "w")

    fop.write(summary_str)


