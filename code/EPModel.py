#!/usr/bin/env python
# coding: utf-8

# In[41]:


import torch
import torch.nn as nn
from transformers import AutoTokenizer, T5ForConditionalGeneration
from nltk.tokenize import sent_tokenize
import CommonUtils as myutils
import EPMConfig as config
import sys

# # Global Settings

# In[42]:




tokenizer = AutoTokenizer.from_pretrained(config.k_tokenizer)
model = T5ForConditionalGeneration.from_pretrained(config.k_model)
model.to(config.device)


def run_model(input_string, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt").to(config.device)
    res = model.generate(input_ids, max_length=config.k_max_tgt_len, **generator_args)
    return tokenizer.batch_decode(res, skip_special_tokens=True)[0]







if __name__=="__main__":
 
    if len(sys.argv) < 3:
        print ("args1: data.tsv, args2: out-preds.tsv")
        sys.exit(1)
 
    
    s2q, q2s = myutils.loadS2Q(config.questionairef)

    inpf = sys.argv[1]
    outf = sys.argv[2]
    
    id2text = myutils.loadTexts(inpf, config.idcol, config.txtcol)
    fout = open(outf, "w")
        
    cnt=0
    for fid in id2text:
        txt = id2text[fid]       
        sents = sent_tokenize(txt)
        if cnt%5==0:
            print ("Processed "+str(cnt))
            print ("\n"+txt)
            print ()
        cnt+=1
        preds=[]
        for sent in sents:
            premise=sent
            for s in s2q:
                if s in preds:
                    continue
                found=False
                for q in s2q[s]:
                    hypothesis=q
                    op = run_model("mnli hypotheis: "+hypothesis+" premise: "+premise)
                    if "entailment" in op:
                        found=True
                        break
                if found:
                    preds.append(s)

        tops='\t'.join(preds)
        if tops.strip()=="":
            tops="NONE_APPLICABLE"
        if cnt%5==0:
            print (tops)

        fout.write(fid+"\t"+tops.strip()+"\n")
        fout.flush()
        #print (candidates)
        
    
    fout.close()
    
