import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np

from collections import Counter
from itertools import chain
from keywords import *

plt.rcParams['axes.labelsize'] = 36
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 30
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 30
plt.rcParams['ytick.labelsize'] = 30

data_url = 'domain_technique.csv'
domain_url = 'domains.csv'
technique_url = 'techniques.csv'
gapminder = pd.read_csv(data_url, encoding="ISO-8859-1")
df1 = gapminder[['Domains', 'Techniques']]

dtcounts = {}
for d in domain_abbrevs:
  dtcounts[d] = {}
  for t in technique_abbrevs:
    dtcounts[d][t] = 0

for i, row in df1.iterrows():
  if not isinstance(row['Domains'], float) and not isinstance(row['Techniques'], float):
    doms = row['Domains'].split('|')
    techs = row['Techniques'].split('|')
    for d in doms:
      for t in techs:
        dtcounts[d][t] += 1

dfDomain = []
dfTechnique = []
dfCount = []
for d in domain_abbrevs:
  for t in technique_abbrevs:
    dfDomain.append(d)
    dfTechnique.append(t)
    dfCount.append(dtcounts[d][t])

df2 = pd.DataFrame({'Domain': dfDomain, 'Technique': dfTechnique, 'Count': dfCount})

hmd = pd.pivot_table(df2, values='Count', index=['Technique'], columns='Domain')

fig, ax = plt.subplots(figsize=(25, 20))

sns.heatmap(hmd, cmap="GnBu", annot=False, ax=ax, fmt='g')

# get totals
dtotal = pd.read_csv(domain_url, encoding="ISO-8859-1")
dtotal = dtotal[domain_abbrevs].sum()
dtotal['Total'] = gapminder.shape[0]

ttotal = pd.read_csv(technique_url, encoding="ISO-8859-1")
ttotal = ttotal[technique_abbrevs].sum()
ttotal['Total'] = gapminder.shape[0]

kwinvert = {v: k for k, v in DOMAIN_ABBRS.items()}
hmd = hmd.rename(columns=kwinvert)
dtotal = dtotal.rename(index=kwinvert)

techinvert = {v: k for k, v in TECHNIQUE_ABBRS.items()}
ttotal = ttotal.rename(index=techinvert)
hmd = hmd.rename(index=techinvert)

# Plot totals
hmd.loc['Total']= dtotal
hmd['Total'] = ttotal
mask = np.zeros((len(hmd), len(hmd.columns)))
mask[:, len(hmd.columns)-1] = True
mask[len(hmd)-1, :] = True
sns.heatmap(hmd, alpha=0, cbar=False, annot=True, fmt='g', annot_kws={"color":"black"})
plt.yticks(rotation=0)
plt.xticks(rotation=30,horizontalalignment='right')
plt.savefig("Domain_Technique_Heatmap.png", bbox_inches='tight')
