#!/usr/bin/env python
# coding: utf-8

# In[41]:



from transformers import AutoTokenizer, T5ForConditionalGeneration
from nltk.tokenize import sent_tokenize
import Config as config



device=config.device
questionairef=config.ysq_file
t5_model = config.epm_model_id
t5_tokenizer = config.epm_model_id
t5_max_tgt_len=10
t5_max_src_len=512

t5_tokenizer = AutoTokenizer.from_pretrained(t5_tokenizer)
t5_model = T5ForConditionalGeneration.from_pretrained(t5_model, device_map="auto")


def run_model(input_strings, model, tokenizer, max_tgt_len, **generator_args):
    model_inputs = tokenizer(input_strings,
            max_length=t5_max_src_len,\
                    padding="max_length", truncation=True,
                    return_tensors="pt").to(device)
    res = model.generate(model_inputs["input_ids"], max_length=max_tgt_len, **generator_args)
    toret = tokenizer.batch_decode(res, skip_special_tokens=True)
    return toret


def loadS2Q(questionairef):
    
    s2q={}
    q2s={}
    lines = open (questionairef, "r",encoding='utf-8' ).readlines()
    ql=[]
    sname=""
    for line in lines:
        line = line.strip()
        if line.strip().isupper(): #startswith("*"):
            if sname!="" and len(ql)>0:
                s2q[sname] = ql
                for q in ql:
                    q2s[q]=sname
            
            sname=line.replace(" ","").strip() #[1:]
            ql=[]
        else:
            ql.append(line.strip())
            
    if sname!="" and len(ql)>0:
        s2q[sname] = ql
        for q in ql:
            q2s[q]=sname
    
    return s2q, q2s

def getEPMForPPRSubset(ppr_ems, qtext, s2q):

    sents = sent_tokenize(qtext)
    print ("#sents="+ str(len(sents)))
    preds={}
    for s in ppr_ems:
        ql = s2q[s]
        if s in preds:
            continue
        for sent in sents:
            premise=sent
            inputs = []
            for hypothesis in ql:
                inp_string = ("mnli hypotheis: "+hypothesis+" premise: "+premise)
                inputs.append(inp_string)

            ops = run_model(inputs, t5_model, t5_tokenizer, t5_max_tgt_len)
            if "entailment" in ops:
                if s not in preds:
                    preds[s]=[sent]
                else:
                    preds[s].append(sent)

    
    return preds
    
def getEPMPreds(qtext, s2q):

    sents = sent_tokenize(qtext)
    print ("#sents="+ str(len(sents)))
    preds={}
    for s in s2q:
        print ("Checking for EMS label "+s)
        ql = s2q[s]
        if s in preds:
            continue
        for sent in sents:
            premise=sent
            inputs = []
            for hypothesis in ql:
                inp_string = ("mnli hypotheis: "+hypothesis+" premise: "+premise)
                inputs.append(inp_string)

            ops = run_model(inputs, t5_model, t5_tokenizer, t5_max_tgt_len)
            if "entailment" in ops:
                if s not in preds:
                    preds[s]=[sent]
                else:
                    preds[s].append(sent)

    
    return preds
  
if __name__=="__main__":
    
    s2q, q2s = loadS2Q(questionairef)
    ppr_ems=['2.MISTRUST/ABUSE(MA)']
    qtext = input("Enter the MH question text:\n")
    print (getEPMForPPRSubset(ppr_ems,qtext, s2q))
    print (getEPMPreds(qtext, s2q))
    
    
