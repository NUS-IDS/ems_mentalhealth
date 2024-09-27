#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:29:58 2024

@author: sdas
"""

import Config as config
import subprocess as sp
import numpy as np
from nltk.tokenize import sent_tokenize

from getYSQGraph import loadYSQGraph, sim_threshold, computeSimilarity

def computeTSVector(txt, embedding_2, out_file):
                
    sents = sent_tokenize(txt)
    simvals = computeSimilarity(sents, embedding_2)
    (_, sz) = simvals.shape
    print ("embg size="+str(sz))
    representation=np.zeros(sz)
    for sx, sent in enumerate(sents):

        maxid = np.argmax(simvals[sx])
        maxval = np.max(simvals[sx])
        representation[maxid]=maxval
        for ix, ival in enumerate(simvals[sx]):
            if ival>sim_threshold and ival>representation[ix]:
                representation[ix] = ival
    
    print (len(representation))
    print (maxval)
    print (np.sum(representation))
    fout = open (out_file, "w")
    for rx, rep in enumerate(representation):
        if rep!=0:
            print (str(rx)+" "+str(rep/np.sum(representation)))
        fout.write(str(rep/np.sum(representation))+"\n")
    fout.close()
    print ("TS Vector for PPR written to "+out_file)
    
    return 
    
def runPPR(edges_file, tsvec_file, ppr_out_file):
    
    status = sp.run([config.ppr_script, \
                     edges_file, ppr_out_file, \
                     str(config.ppr_damping_factor), \
                     tsvec_file])
    
    return status.returncode    
    
def getScore(inpfiles, pprfile):

    lines = open (pprfile, "r").readlines()
    vec1=[]
    for l in lines:
        lp = l.strip().split()
        vec1.append(float(lp[-1].strip()))

    print (len(vec1))
    toreturn=[]
    for f in inpfiles:

        lines = open (f, "r").readlines()
        vec2=[]
        for l in lines:
            vec2.append(float(l.strip()))

        print (len(vec2))
        toreturn.append((f,np.dot(np.asarray(vec1), np.asarray(vec2))))

    toreturn.sort(key=lambda tup: tup[1], reverse=True) 
    
    return toreturn

def getEMSRankPredictions(qtext, ysq_embeddings, topk=5):
    
    tsvecfile = config.scratch_dir+"/tsvec.txt"
    edges_file = config.ppr_ysq_dir+"/edges.txt"
    pproutfile = config.scratch_dir+"/pprout.txt"
    computeTSVector(qtext, ysq_embeddings, tsvecfile)
    status = runPPR(edges_file, tsvecfile, pproutfile)
    
    prefix = config.ppr_ysq_dir
    emsfiles=[
            prefix +"/"+"1.txt",
            prefix +"/"+"10.txt",
            prefix +"/"+"11.txt",
            prefix +"/"+"12.txt",
            prefix +"/"+"13.txt",
            prefix +"/"+"14.txt",
            prefix +"/"+"15.txt",
            prefix +"/"+"16.txt",
            prefix +"/"+"17.txt",
            prefix +"/"+"18.txt",
            prefix +"/"+"2.txt",
            prefix +"/"+"3.txt",
            prefix +"/"+"4.txt",
            prefix +"/"+"5.txt",
            prefix +"/"+"6.txt",
            prefix +"/"+"7.txt",
            prefix +"/"+"8.txt",
            prefix +"/"+"9.txt",
    ]
    emsmap={}
    emsmapf=prefix+"/emsmap.txt"
    lines = open (emsmapf, "r").readlines()
    for line in lines:
        lp = line.strip().split("\t")
        emsmap[prefix+"/"+lp[-1]+".txt"]=lp[0].strip()

    if status==0:
        scores = getScore(emsfiles, pproutfile)
        print (scores)
        preds=[]

        _, maxs = scores[0]
        thresh = maxs/10
     
        print("max score="+str(maxs)+ " threshold= "+str(thresh))
        for ex, ele in enumerate(scores):
            (fname, score) = ele
            if score>thresh and ex<topk:
                preds.append((emsmap[fname], score))   
    
    return preds

if __name__=="__main__":
    
    ysq_embeddings=loadYSQGraph(config.ppr_ysq_dir)
    
    qtext = input("Enter the MH question text:\n")
    print (getEMSRankPredictions(qtext, ysq_embeddings))