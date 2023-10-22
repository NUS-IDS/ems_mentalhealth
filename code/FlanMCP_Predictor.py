#!/usr/bin/env python
# coding: utf-8

import torch
import torch.nn as nn
from transformers import AutoTokenizer, T5ForConditionalGeneration
from nltk.tokenize import sent_tokenize
import CommonUtils as myutils
import FlanMCConfig as config
import sys


tokenizer = AutoTokenizer.from_pretrained(config.k_tokenizer)
model = T5ForConditionalGeneration.from_pretrained(config.k_model, device_map="auto")


def run_model(input_string, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt").to("cuda")
    res = model.generate(input_ids, max_length=config.k_max_tgt_len, **generator_args)
    return tokenizer.batch_decode(res, skip_special_tokens=True)[0]


if __name__=="__main__":
 
    if len(sys.argv) < 3:
        print ("args1: data.tsv, args2: out-preds.tsv")
        sys.exit(1)
        
    lines=open(config.promptfile,'r').readlines()
    prompt_=(' '.join(lines)).strip()

    inpf = sys.argv[1]
    outf = sys.argv[2]
    
    id2text = myutils.loadTexts(inpf, config.idcol, config.txtcol)
    
    fout = open(outf, "w")
    fout.write("##MCPrompt from "+prompt_+"\n#\n")

    cnt=0
    
    for fid in id2text:
        txt = id2text[fid]       
        cnt+=1
        if cnt%5==0:
            print (str(cnt)+"\n"+txt)
        
        prompt = prompt_ + txt

        tops = run_model(prompt)
        
        tops = tops.replace(", ","\t")
        if tops.strip()=="":
            tops="NONE_APPLICABLE"
        if cnt%5==0:
            print (tops)

        fout.write(fid+"\t"+tops.strip()+"\n")
        fout.flush()
        
    
    fout.close()
    
