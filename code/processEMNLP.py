#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 13:51:08 2026

@author: sdas
"""

import SchemaAnnotator as stann
import csv

inpfile="/home/sdas/npj_calba/github_npj/gold/gold.tsv"
outfile="gemini_3labels.csv"

lines = open (inpfile, "r").readlines()


print ("#posts+1=%d"%len(lines))

    
fout = open (outfile, "w")
csvw = csv.writer (fout, delimiter=",", quoting=csv.QUOTE_ALL)
csvw.writerow(["pid","content","#labels","label1","expln1","label2","expln2","label3","expln3"])
for ex in range(1, len(lines)):
    
    parts = lines[ex].strip().split("\t")
    pid = parts[0]
    content = parts[1]
  
    stlabels = stann.getSTLabels(content, llm="gemini")
    
    if stlabels is None:
        stlabels=[]
    
    row = [pid, content, len(stlabels)]
    for lpair in stlabels:
        if "label" in lpair and "explanation" in lpair:
            row.append(lpair["label"])
            row.append(lpair["explanation"])
        
    csvw.writerow(row)

    if ex%5==0:
        print ("ex is %d"%ex)
        print (row[2])
        print ('\n'.join(row[5:]))
    fout.flush()
    
fout.close()
    
    
