#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 17:29:31 2023


"""


def loadS2Q(questionairef):
    
    s2q={}
    q2s={}
    lines = open (questionairef, "r").readlines()
    ql=[]
    sname=""
    for line in lines:
        line = line.strip()
        if line.strip().isupper(): #startswith("*"):
            if sname!="" and len(ql)>0:
                s2q[sname] = ql
                for q in ql:
                    q2s[q]=sname
            
            sname=line.strip() #[1:]
            ql=[]
        else:
            ql.append(line.strip())
            
    if sname!="" and len(ql)>0:
        s2q[sname] = ql
        for q in ql:
            q2s[q]=sname
    
    return s2q, q2s

def loadSchemaDefinitionsFile(inpf):

    defs={}

    lines = open (inpf, "r").readlines()
    stype=""
    for line in lines:
        l = line.strip()
        if l=="":
            continue
        if l.strip().isupper():
            stype = l.strip()
            defs[stype]=""
        elif stype!="":
            defs[stype] +=" "+l.strip()

    return defs

def loadTexts(tsvfile, idcol, txtcol):
    
    lines = open (tsvfile, "r").readlines()
    id2text={}
    
    
    for lx in range(0, len(lines)):
        
        if lines[lx].startswith("#"):
            print ("Ignoring line, looks like a comment: "+lines[lx])
            continue
        
        
        
        lp = lines[lx].strip().split("\t")
        
        if len(lp) < idcol or len(lp) < txtcol:
            print ("Ignoring line, not enough parts: "+lines[lx])
            continue
        
        id2text [lp[idcol]] = lp[txtcol].strip()
        
    
    return id2text