import matplotlib.pyplot as plt
import pandas as pd
import os
from keywords import *

ddata = pd.read_csv("domains.csv", encoding="ISO-8859-1")
ddata = ddata.sort_values(by=['Year'])

plt.rcParams['axes.labelsize'] = 20
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams["figure.figsize"] = (15, 8)
ax = plt.gca()

markers = ["o", "^", "x", "d", "s"]
linestyles = [':', '-.', '-']

i = 0
kwinvert = {v: k for k, v in DOMAIN_ABBRS.items()}
ddata = ddata.rename(columns=kwinvert)
for kw in KEYWORDS.keys():
  mrkr = markers[i % len(markers)]
  ddata.plot(kind='line',x='Year',y=kw, ax=ax, linewidth=3, marker=mrkr, markersize=7)
  i += 1

plt.legend(loc='upper left', ncol=2, handleheight=1.5, framealpha=0.3)
plt.ylabel("Number of papers")
plt.savefig("Domains_Time_Series.png", bbox_inches='tight')
plt.cla()

tdata = pd.read_csv("techniques.csv", encoding="ISO-8859-1")
tdata = tdata.sort_values(by=['Year'])

plt.rcParams["figure.figsize"] = (15, 8)
ax = plt.gca()

i = 0
techinvert = {v: k for k, v in TECHNIQUE_ABBRS.items()}
tdata = tdata.rename(columns=techinvert)
for t in TECHNIQUES.keys():
  mrkr = markers[i % len(markers)]
  ls = linestyles[i % len(linestyles)]
  tdata.plot(kind='line',x='Year',y=t, ax=ax, linestyle=ls, linewidth=3, marker=mrkr, markersize=7)
  i += 1

plt.legend(loc='upper left', ncol=2, handleheight=1.5, framealpha=0.3)
plt.ylabel("Number of papers")
plt.savefig("Techniques_Time_Series.png", bbox_inches='tight')
