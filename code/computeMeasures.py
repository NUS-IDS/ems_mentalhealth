#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import sys
import csv
from EvaluationMeasures import normalize, evaluation
    


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

def loadGoldFile(goldfile, idcol, lstartcol):
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


    
def evaluateCSVPreds(predsfile, goldfile, mapfile, \
                  colstart=1, skip=2):
    
    lkmap = loadLabelMap(mapfile, 0)
    id2labels = loadGoldFile(goldfile, 0, 2)     
    
    
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
        
        npreds=[]
        
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
    
    if len(sys.argv)!=3:
        print ("args1: gold-dir-path, args2: labels.csv(output from processEMNLP)")
        sys.exit(1)
        
    gold_dir=sys.argv[1]
    gold_file=gold_dir+"/gold.tsv"
    lmap_file=gold_dir+"/labels.list"
    
    preds_file=sys.argv[2] 
    colstart=3
    skip=2
    print ("Using preds file "+preds_file)
    evaluateCSVPreds(preds_file, gold_file, lmap_file, colstart, skip)
    
        
