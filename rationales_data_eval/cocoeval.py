#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:23:20 2020

@author: sdas
"""
import sys
import csv
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from Utils import loadEMSList

scorers = {
        "Bleu": Bleu(4),
        "Meteor": Meteor(),
        "Rouge": Rouge()
    }


    

def getScoresForPairs(corrlines, predlines):
    
    gts={}
    res={}
    
    
    
    for lx, corr in enumerate(corrlines):
    #    if lx!=6:
    #        continue
        
        gts[lx] = [corrlines[lx].lower().strip()]
        res[lx]= [predlines[lx].lower().strip()]
        
        
        
    scores = {}
    for name, scorer in scorers.items():
    #    print (gts)
    #    print (res)
        score, all_scores = scorer.compute_score(gts, res)
        if isinstance(score, list):
            for i, sc in enumerate(score, 1):
                scores[name + str(i)] = sc
        else:
            scores[name] = score
    
    return scores

def getScoresForPair(gold_question, prediction):

    
    gts={}
    gts[0]=[gold_question]
    res={}
    res[0]=[prediction]
    
    scores = {}
    for name, scorer in scorers.items():
    #    print (gts)
    #    print (res)
        score, all_scores = scorer.compute_score(gts, res)
        if isinstance(score, list):
            for i, sc in enumerate(score, 1):
                scores[name + str(i)] = sc
        else:
            scores[name] = score
    
   
    return scores
    

def getScores(goldf, predf):

    print ("GOLD "+goldf)
    print ("PRED "+predf)
    fin = open(goldf, "r")
    corrlines = fin.readlines()
    fin.close()
    
    fin = open(predf, "r")
    predlines = fin.readlines()
    fin.close()
    
    print ("Total questions "+str(len(corrlines)))


    return getScoresForPairs(corrlines, predlines)


if __name__ == "__main__":

 #   gold_question = "who was the mvp of super bowl i and ii ?"
 #   prediction="who was the mvp ?"
 #   scores = getScoresForPair(gold_question, prediction)

 #   print (scores)
 

    sdefs = loadEMSList("./schema_defs.txt")
    map2={}
    for key in sdefs:
        map2[key.replace(" ","").strip()]=key.strip()


    goldf= "./emnlp_gold_rationales.tsv"
#    predsf=["data_new/emnlp_predicted_rationales_goldems.csv",
    predsf=["./emnlp_epm_rationales.csv"]

    id2goldr={}

    fin = open (goldf, "r")
    for line in fin.readlines():
        lp = line.strip().split("\t")
        iid = lp[0]

        for px in range(2, len(lp)-1):
            if px%2!=0:
                continue

            ems = lp[px]
            ems = map2[ems.replace(" ","").strip()]
            rationale = lp[px+1]

            if iid not in id2goldr:
                id2goldr[iid]={}

            if ems not in id2goldr[iid]:
                id2goldr[iid][ems]=""

            id2goldr[iid][ems]+=" "+rationale.strip()

    
    print ("#gold="+str(len(id2goldr)))


    predrmaps=[]

    for epmf in predsf:

        id2epmr={}

        fin = open (epmf, "r")
        csvr = csv.reader(fin, delimiter=",")
        header={}
        for row in csvr:
            if len(header)==0:
                for ex, ele in enumerate(row):
                    header[ele]=ex
                print (header)
                continue

            iid = row[header["id"]]

            ems = row[header["ems"]]
            ems = map2[ems.replace(" ","").strip()]
            rationale = row[header["rationale"]]

            if iid not in id2epmr:
                id2epmr[iid]={}

            if ems not in id2epmr[iid]:
                id2epmr[iid][ems]=""

            id2epmr[iid][ems]+=" "+rationale.strip()


        print("#epm="+str(len(id2epmr)))
        predrmaps.append(id2epmr)


    for ix, id2epmr in enumerate(predrmaps):
        glines=[]
        plines=[]
        for iid in id2epmr:
            pairs = id2epmr[iid]
            if iid not in id2goldr:
                continue
            gpairs = id2goldr[iid]

            for ems in pairs:
                if ems in gpairs:
                    glines.append(gpairs[ems])
                    plines.append(pairs[ems])

        print (predsf[ix])
        print ("#glines="+str(len(glines))+" #plines="+str(len(plines)))
        scores = getScoresForPairs(glines, plines)
        print (scores)
