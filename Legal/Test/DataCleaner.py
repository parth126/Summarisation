# This script extracts judgements from the legal corpus
# Stores them in the /judgements corpus
# Assumes all source files are in the present working directory
# Assumes there is a judgmenets folder present in the pwd.

import os
from bs4 import BeautifulSoup
import glob

for filename in glob.glob("*.txt"):
    #print filename
    handler = open(filename).read()
    s = BeautifulSoup(handler)
    
    fop = open("judgements/"+filename, "w")
    judgement = s.findAll("judgement")[0].string.strip()
    #print judgement
    fop.write(judgement)

'''    
f = "SupremeCourt_1989_96.txt"
handler = open(f).read()
s = BeautifulSoup(handler)
'''
#print s.findAll("judgement")[0].string.strip()