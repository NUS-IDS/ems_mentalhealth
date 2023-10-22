#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import sys

from EvaluationMeasures import normalize, evaluation
    

def label_lookup(lkmap, pred):
    
    if pred in lkmap:
        return pred
    
    p = normalize(pred)
    for key in lkmap.keys(): #if p not in lkmap:
        if p in key:
            print ("Warning: "+pred +" not found in lkmap, using near label "+key)
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

def evaluateTSVPreds(predsfile, goldfile, mapfile, canon_col = 0, NONE_LABEL="NONE_APPLICABLE"):
    
    
    lkmap = loadLabelMap(mapfile, canon_col)
    
    id2labels = loadGoldFile2(goldfile, 0, 2)     
    
    
    print ("len map="+str(len(lkmap)))
    print ("len id2l="+str(len(id2labels)))
    
    aggg=[]
    aggp=[]
    lines = open(predsfile, "r").readlines()
    fids=[]
    for lx, line in enumerate(lines):
        if line.startswith("#"):
            print ("Ignoring line with #")
            continue
        
        lp = line.strip().split("\t")
        fid = lp[0]
        preds = lp[1:]
        
        
        npreds=[]
        seen={} #in case the model predicted the same label multiple times due to whatever reason
        for pred in preds:
            if pred.strip()=="" or "none" in pred.lower(): #NONE_LABEL.lower():
                continue
    
            canon_pred = label_lookup(lkmap, pred)
            
            if canon_pred=="":
                print ("ERROR in label lookup for "+pred)
                print ("Cannot find approx")
                sys.exit(1)
            
            ncp = normalize(canon_pred)
            if ncp not in seen:
                seen[ncp]=""
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

    print ("Computing measures for "+str(len(aggg))+" files")
    m = str(evaluation(fids, aggg, aggp))
    print ("measures = "+m)
 
    return m


if __name__=="__main__":
    
    if len(sys.argv)!=3:
        print ("args1: gold-dir (contains gold.tsv and labels.list), args2: preds.tsv")
        sys.exit(1)
        
    gold_file=sys.argv[1]+"/gold.tsv"
    lmap_file=sys.argv[1]+"/labels.list"
    preds_file=sys.argv[2]
    
    print ("Using gold file "+gold_file)
    print ("Using map file "+lmap_file)
    print ("Using preds file "+preds_file)
    evaluateTSVPreds(preds_file, gold_file, lmap_file)
    
