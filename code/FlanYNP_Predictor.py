
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from nltk.tokenize import sent_tokenize
import FlanYNConfig as config
import CommonUtils as myutils
import sys


tokenizer = AutoTokenizer.from_pretrained(config.k_model)
model = AutoModelForSeq2SeqLM.from_pretrained(config.k_model, device_map="auto") #, load_in_8bit=True)


def run_model(input_strings, **generator_args):
    model_inputs = tokenizer(input_strings, max_length=config.k_max_src_len,\
                    padding="max_length", truncation=True, return_tensors="pt").to(config.device)
    res = model.generate(model_inputs["input_ids"], max_length=config.k_max_tgt_len, **generator_args)
    toret = tokenizer.batch_decode(res, skip_special_tokens=True)
    return toret




###############


if __name__=="__main__":
    
    if len(sys.argv)!=3:
        print ("args1: data.tsv, args2: outfile.tsv")
        sys.exit(1)
        
    sdefs = myutils.loadSchemaDefinitionsFile(config.schemadefs_file)
    
    prompt_pfx="Here is the definition for the label "

  
        
    data_file=sys.argv[1]
    preds_out_file=sys.argv[2]
    fout = open(preds_out_file, "w")
    id2text = myutils.loadTexts(data_file, config.idcol, config.txtcol)
    
    
    for iid in id2text:
        
        txt = id2text[iid]
        
        tops=""
        inputs = []
        for s in sdefs:
            sdef = sdefs[s]
            
            prompt = prompt_pfx +s+" "+ sdef+" Is this label applicable to the context: "+txt+"? Answer Yes or No."
            
            inputs.append(prompt)

        op = run_model(inputs)
        for sx, s in enumerate(sdefs):
            if "yes" in op[sx].lower():
                tops +="\t"+s
    
        fout.write(iid+"\t"+tops.strip()+"\n")
        fout.flush()

        
        print (op)
        print(iid+"\t"+tops.strip()+"\n")


    fout.close()
