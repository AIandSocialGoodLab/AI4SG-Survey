from keywords import *
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk import FreqDist
from nltk import ngrams
import csv
import pandas as pd
import sys
import os


data = pd.read_csv("papers.csv")
domains = [k for k in KEYWORDS.keys()]
domain_abbrevs = list(map(lambda x: DOMAIN_ABBRS[x], KEYWORDS.keys()))
techniques = [k for k in TECHNIQUES.keys()]
technique_abbrevs = list(map(lambda x: TECHNIQUE_ABBRS[x], TECHNIQUES.keys()))
deployment_keywords = ["deployed", "deployment", "deploy", "in use", "been adopted"]
stemmer = SnowballStemmer("english")
dcounts = {}
tcounts = {}
num_deployed = 0

for index, abstract in data.iterrows():
    words = word_tokenize(abstract['Abstract']) + word_tokenize(abstract['Title'])
    outline = []
    row = [abstract['Title'], abstract['Year'], abstract['Abstract'], abstract['Venue']]
    all_counts = dict()
    for size in 1, 2:
        all_counts[size] = FreqDist(ngrams(words, size))
    for technique in TECHNIQUES:
        filtered_dict1 = {k[0]:v for (k,v) in all_counts[1].items() if k[0] in TECHNIQUES[technique] or stemmer.stem(k[0]) in TECHNIQUES[technique]}
        filtered_dict2 = {k[0] + " " + k[1]:v for (k,v) in all_counts[2].items() if k[0] + " " + k[1] in TECHNIQUES[technique]}
        filtered_dict1.update(filtered_dict2)
        data.loc[index, technique] = str(filtered_dict1)
    for domain in KEYWORDS:
        filtered_dict1 = {k[0]:v for (k,v) in all_counts[1].items() if k[0] in KEYWORDS[domain] or stemmer.stem(k[0]) in KEYWORDS[domain]}
        filtered_dict2 = {k[0] + " " + k[1]:v for (k,v) in all_counts[2].items() if k[0] + " " + k[1] in KEYWORDS[domain]}
        filtered_dict1.update(filtered_dict2)
        data.loc[index, domain] = str(filtered_dict1)

for index, abstract in data.iterrows():
    found = False
    for kw in deployment_keywords:
        if kw in abstract['Abstract']:
            data.loc[index, 'Deployed'] = "Y"
            found = True
            num_deployed += 1
            break
        if not found:
            data.loc[index, 'Deployed'] = "N"


    data.loc[index, 'Techniques'] = ""
    for techniqueidx, technique in enumerate(techniques):
        if abstract[technique] != "{}":
            if data.loc[index, 'Techniques'] == "":
                data.loc[index, 'Techniques'] = technique_abbrevs[techniqueidx]
            else:
                data.loc[index, 'Techniques'] = data.loc[index, 'Techniques'] + "|" + technique_abbrevs[techniqueidx]
    data.loc[index, 'Domains'] = ""
    for domainidx, domain in enumerate(domains):
        if abstract[domain] != "{}":
            if data.loc[index, 'Domains'] == "":
                data.loc[index, 'Domains'] = domain_abbrevs[domainidx]
            else:
                data.loc[index, 'Domains'] = data.loc[index, 'Domains'] + "|" + domain_abbrevs[domainidx]

data.to_csv("domain_technique.csv")

dcounts = {}
tcounts = {}
for index, abstract in data.iterrows():
    if abstract['Year'] not in dcounts:
        dcounts[abstract['Year']] = {}
        for d in domains:
            dcounts[abstract['Year']][d] = 0
    if abstract['Year'] not in tcounts:
        tcounts[abstract['Year']] = {}
        for t in techniques:
            tcounts[abstract['Year']][t] = 0

    for domainidx, domain in enumerate(domains):
        if domain_abbrevs[domainidx] in abstract['Domains']:
            dcounts[abstract['Year']][domain] += 1
    for techniqueidx, technique in enumerate(techniques):
        if technique_abbrevs[techniqueidx] in abstract['Techniques']:
            tcounts[abstract['Year']][technique] += 1
dfDictD = {"Year": list(dcounts.keys())}
for d in domains:
  dfDictD[DOMAIN_ABBRS[d]] = list(map(lambda x: dcounts[x][d], dfDictD["Year"]))

dfDictT = {"Year": list(tcounts.keys())}
for t in techniques:
  dfDictT[TECHNIQUE_ABBRS[t]] = list(map(lambda x: tcounts[x][t], dfDictT["Year"]))

df2 = pd.DataFrame(dfDictD)
df2.to_csv("domains.csv", header=True)

df3 = pd.DataFrame(dfDictT)
df3.to_csv("techniques.csv", header=True)
