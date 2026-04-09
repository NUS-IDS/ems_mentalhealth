#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import sys
import csv
from EvaluationMeasures import normalize, evaluation
    
consider_list="train/151.txt \
train/153.txt \
train/142.txt \
train/120.txt \
train/91.txt \
train/114.txt \
train/123.txt \
train/408.txt \
train/289.txt \
train/296.txt \
train/302.txt \
train/382.txt \
val/248.txt \
train/718.txt \
train/717.txt \
train/210.txt \
train/208.txt \
train/422.txt \
train/424.txt \
train/282.txt \
train/286.txt \
train/375.txt \
train/678.txt \
train/46.txt train/365.txt  train/373.txt train/368.txt".split()

def label_lookup(lkmap, pred):
    
    if pred in lkmap:
        return pred
    
    p = normalize(pred)
    for key in lkmap.keys(): #if p not in lkmap:
        if p in key:
            #print ("Warning: "+pred +" not found in lkmap, using near label "+key)
            return lkmap[key]
    
    return ""

def loadLabelMap(mapfile, canon_col):
    lines = open (mapfile, "r").readlines()
    lkmap={}
    for line in lines:
        lp = line.strip().split("\t")
        k = normalize(lp[canon_col])
        v = lp[canon_col].strip()
        lkmap[k] = v
            
    return lkmap

def loadGoldFile2(goldfile, idcol, lstartcol):
    id2labels = {}
    
    lines = open (goldfile, "r").readlines()
    for lx in range(0, len(lines)):
        if lines[lx].strip().startswith("#"):
            print ("Ignoring line, looks like a comment "+lines[lx])
            continue

        lp = lines[lx].strip().split("\t")
        gold=[]
        fid = lp[idcol]
        for px in range(lstartcol, len(lp)):
            gold.append(lp[px].strip())
        id2labels[fid]=gold

    return id2labels

def evaluateTSVPreds(predsfile, goldfile, mapfile):
    lkmap = loadLabelMap(mapfile, 0)
    id2labels = loadGoldFile2(goldfile, 0, 2)     
    
    
    print ("len map="+str(len(lkmap)))
    print ("len id2l="+str(len(id2labels)))
    
    aggg=[]
    aggp=[]
    
    fin  = open(predsfile, "r")
    lines = fin.readlines()
    fids=[]
    
    for line in lines:
        if line.strip().startswith("#"):
            print ("Ignoring header "+line.strip())
            continue
        
        row = line.strip().split("\t")
        
        fid = row[0]
        if fid not in consider_list:
            print ("Ignorning fid not in list "+fid)
            continue
        
        npreds=[]
        # print (colstart)
        # print (row[colstart])
        for px in range(1, len(row)):
            
            pred = row[px]
        
            if pred.strip()=="" or "none" in pred.lower(): #NONE_LABEL.lower():
                continue
    
            
            canon_pred = label_lookup(lkmap, pred)
            
            if canon_pred=="":
                print ("ERROR in label lookup for "+pred)
                print ("Cannot find approx")
                sys.exit(1)
            
            ncp = normalize(canon_pred)
            if ncp not in npreds:
                npreds.append(ncp)
        
        ngold = []
        if fid not in id2labels:
            print ("ERROR in label lookup, fid missing "+fid)
            continue
            
        for g in id2labels[fid]:
            ngold.append(normalize(g))
    
        aggg.append(ngold)
        aggp.append(npreds)        
        
        fids.append (fid)

    print ("Computing measures for "+str(len(fids))+" files")
    m = str(evaluation(fids, aggg, aggp))
    print ("measures = "+m)
 
    return m
    
def evaluateCSVPreds(predsfile, goldfile, mapfile, \
                  colstart=1, skip=2):
    
    lkmap = loadLabelMap(mapfile, 0)
    id2labels = loadGoldFile2(goldfile, 0, 2)     
    
    
    print ("len map="+str(len(lkmap)))
    print ("len id2l="+str(len(id2labels)))
    
    aggg=[]
    aggp=[]
    
    fin  = open(predsfile, "r")
    header=[]
    csvr = csv.reader(fin, delimiter=",",quoting=csv.QUOTE_ALL)
    fids=[]
    
    for row in csvr:
        if len(header)==0:
            header=row
            continue
        
        
        
        fid = row[0]
        if fid not in consider_list:
            print ("Ignorning fid not in list "+fid)
            continue
        
        npreds=[]
        # print (colstart)
        # print (row[colstart])
        for px in range(colstart, len(row), skip):
            
            pred = row[px]
        
            if pred.strip()=="" or "none" in pred.lower(): #NONE_LABEL.lower():
                continue
    
            
            canon_pred = label_lookup(lkmap, pred)
            
            if canon_pred=="":
                print ("ERROR in label lookup for "+pred)
                print ("Cannot find approx")
                sys.exit(1)
            
            ncp = normalize(canon_pred)
            if ncp not in npreds:
                npreds.append(ncp)
        
        ngold = []
        if fid not in id2labels:
            print ("ERROR in label lookup, fid missing "+fid)
            continue
            
        for g in id2labels[fid]:
            ngold.append(normalize(g))
    
        aggg.append(ngold)
        aggp.append(npreds)        
        
        fids.append (fid)

    print ("Computing measures for "+str(len(fids))+" files")
    m = str(evaluation(fids, aggg, aggp))
    print ("measures = "+m)
 
    return m


    
    
if __name__=="__main__":
    
    
        
    gold_dir="/home/sdas/emnlp_final_share/gold"
    gold_file=gold_dir+"/gold.tsv"
    lmap_file=gold_dir+"/labels.list"
    print ("Using gold file "+gold_file)
    print ("Using map file "+lmap_file)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/svp.preds.tsv"
    # print ("Using preds file "+preds_file)
    # evaluateTSVPreds(preds_file, gold_file, lmap_file)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/epm.preds.tsv"
    # print ("Using preds file "+preds_file)
    # evaluateTSVPreds(preds_file, gold_file, lmap_file)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/emnlp_negotiated_dir2.csv"
    # colstart=1
    # skip=2
    # print ("Using preds file "+preds_file)
    # evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/emnlp_negotiated_dir1.csv"
    # colstart=1
    # skip=2
    # print ("Using preds file "+preds_file)
    # evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
    
    print ("===========")
    preds_file="/home/sdas/npj_calba/github_npj/code/gemini_labels.csv"
    preds_file="/home/sdas/npj_calba/github_npj/code/gpt_labels.csv"
    #"home/sdas/npj_calba/stlabels/emnlp/gpt_3labels.csv"
    colstart=3
    skip=2
    print ("Using preds file "+preds_file)
    evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/emnlp_or.csv"
    # colstart=2
    # skip=1
    # print ("Using preds file "+preds_file)
    # evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/gemini_3labels.csv"
    # colstart=3
    # skip=2
    # print ("Using preds file "+preds_file)
    # evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
    # print ("===========")
    # preds_file="/home/sdas/npj_calba/stlabels/emnlp/emnlp_and.csv"
    # colstart=2
    # skip=1
    # print ("Using preds file "+preds_file)
    # evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
