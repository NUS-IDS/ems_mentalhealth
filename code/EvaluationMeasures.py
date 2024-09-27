#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:33:55 2023

"""



def normalize(txt):
    
    return txt.replace(' ', '').strip()

def loadLabelMaps(mapfile, lkupcol, col2):
    lines = open (mapfile, "r").readlines()
    lkmap={}
    for line in lines:
        lp = line.strip().split("\t")
        if len(lp)>lkupcol and len(lp)>col2:
            k = normalize(lp[lkupcol])
            v = normalize(lp[col2])
            lkmap[k] = v
            
    return lkmap


def computeOverlap(goldlist, predlist):
  
    
    
    if len(goldlist)==0 and len(predlist)==0:
        return 1, 1, 1, 1 
    
    
    overlap=0
    for pred in predlist:
        if pred in goldlist:
            overlap += 1
    
    if len(goldlist)==0:
        recall=0
    else:
        recall=overlap/len(goldlist)
        
    if len(predlist)==0:
        precision = 0
    else:
        precision = overlap/len(predlist)
        
    f1=0
    if (precision+recall)!=0:
        f1 = 2*precision*recall/(precision+recall)
    
    
    hasone = 0
    if overlap>0:
        hasone = 1
    
    return hasone, precision, recall, f1 

def evaluation(fids, goldlists, predlists):
    
    mscores={
            "f1":0,
            "precision":0,
            "hasOne":0,
            "recall":0,
            }
    
    nnz=0 #non-zero gold list
    oz=0 #non-zero gold but overlap is zero
    pz=0 #pred is zero for non-zero gold list
    nbz=0 #both gold and pred are zero
    
    for gx, goldlist in enumerate(goldlists):
        
        predlist = predlists[gx]
        hasone, p, r, f1 = computeOverlap(goldlist, predlist)
        mscores["f1"] += f1
        
        if len(goldlist)>0:
            mscores["hasOne"] += hasone
        
        mscores["precision"] += p
        mscores["recall"] += r
        
        if len(goldlist)!=0:
            nnz += 1
            if hasone==0:
                oz += 1
                
        if len(predlist)==0:
            pz += 1
        if len(predlist)==0 and len(goldlist)==0:
            nbz += 1
        
        
    for key in mscores:
        if key!="hasOne":
            mscores[key]/=len(goldlists)
    
    mscores["hasOne"] /= nnz
    mscores["pct_oz_ngz"] = oz/nnz
    mscores["pct_pz"] = pz/len(predlists)
    mscores["pct_nbz"] = nbz/(len(goldlists)-nnz)
    mscores["pct_gz"] = (len(goldlists)-nnz)/len(goldlists)
        
    return mscores
    
