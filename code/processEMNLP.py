#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 13:51:08 2026

@author: sdas
"""

import SchemaAnnotator as stann
import csv
import sys

if __name__=="__main__":
    
    if len(sys.argv)<3:
        print ("args1: gold.tsv, args2: output.csv, [args3:llm=gpt(default)/gemini]")
        sys.exit(1)
        
    inpfile=sys.argv[1] #"../gold/gold.tsv"
    outfile=sys.argv[2]  #"../stlabels/gemini_3labels.csv"
    
    llmtype="gpt"
    if len(sys.argv)>3:
        temp = sys.argv[3].lower().strip()
        if temp not in ["gpt", "gemini"]:
            print ("LLMs supported gpt/gemini")
            temp="gpt"
        
        llmtype=temp
        print ("Setting LLM type to: "+llmtype)
        
    lines = open (inpfile, "r").readlines()
    
    
    print ("#posts+1=%d"%len(lines))
    
        
    fout = open (outfile, "w")
    csvw = csv.writer (fout, delimiter=",", quoting=csv.QUOTE_ALL)
    csvw.writerow(["pid","content","#labels","label1","expln1","label2","expln2","label3","expln3"])
    for ex in range(1, len(lines)):
        
        parts = lines[ex].strip().split("\t")
        pid = parts[0]
        content = parts[1]
      
        stlabels = stann.getSTLabels(content, llm=llmtype)
        
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
            if len(row)>3:
                print ('\n'.join(row[3:]))
        fout.flush()
        
    fout.close()
        
        
