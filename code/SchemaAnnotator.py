#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 12:19:16 2026

@author: sdas
"""
from Common import getChatGPTResponse, getGeminiResponse, parseJSONWithKeys


def loadSchemaDefs(name2def_tsv="../resources/schema_defs.tsv"):
    
    lines =  open (name2def_tsv, "r").readlines()
    name2def={}
    for line in lines:
        lp = line.strip().split("\t")
        defn = (' '.join(lp[1:])).strip()
        name2def[lp[0].split(".")[-1].strip()]=defn
        
    return name2def


schema_defs = loadSchemaDefs()
print (len(schema_defs))
print (schema_defs.keys())

SYSPROMPT="You are an English counseling conversation analyst."+ \
        "You job is to use the following definitions listed from "+\
            "Schema Therapy to assign 0, 1, 2, or 3 Schema labels for "+\
                "the given post. Only assign labels that are most applicable "+\
            " only using the content in the post, do not speculate. "+\
                "If no labels are applicable print an empty list as your output."+\
                    "For each chosen label, "+\
        " select a sentence for grounding your prediction as explanation. Your "+\
    " output should ONLY be a JSON list of up to three elements "+\
        "formatted as [ {\"label\":<>, \"explanation\":<>} ]. Schema Definitions:\n"+\
            str(schema_defs)
            
            
def getLLMLabels(post, llm="gpt"):
    
    USRPROMPT = "\nPost: "+post
    
    if llm=="gemini":
        output = getGeminiResponse(USRPROMPT, SYSPROMPT)
    else:
        output = getChatGPTResponse(USRPROMPT, SYSPROMPT)
    
    return output


def getSTLabels(post, llm="gpt"):
    try:
        output = getLLMLabels(post, llm)
        if output is None:
            return None
        return parseJSONWithKeys(output)
    except:
        print ("Exception during LLM call/parsing, output: \n")
        print (output)
        return None

