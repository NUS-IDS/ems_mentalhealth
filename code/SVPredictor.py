from sentence_transformers import SentenceTransformer, util
import sys
import numpy as np
from nltk.tokenize import sent_tokenize
import CommonUtils as myutils
import SVPConfig as config

#####################


models = [
        SentenceTransformer(config.st_model1, device=config.device),
        SentenceTransformer(config.st_model2, device=config.device),
        SentenceTransformer(config.st_model3, device=config.device),
        ]


#Compute embedding for both lists

def loadS2Q(questionairef, amodel):
    
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
    
    s2q_a={}
    for s in s2q:
        ql = s2q[s]
        embeddings = amodel.encode(ql, convert_to_tensor=True).to(config.device)
        s2q_a[s] = (ql, embeddings)
    return s2q_a, q2s


s2q_a = []
q2s = []
for mx, model in enumerate(models):
    s2q_a_t, q2s_t = loadS2Q(config.questionairef, model)
    s2q_a.append(s2q_a_t)
    q2s.append(q2s_t)

print (len(s2q_a))
print (len(q2s))


#####################
def predictForText(text, s2q_a, amodel):
    
    sents = sent_tokenize(text)
    embedding_1= amodel.encode(sents, convert_to_tensor=True).to(config.device)
        

    qlevel = []
    for s in s2q_a:
        (ql, qlem) = s2q_a[s]
        simvals = util.cos_sim(embedding_1, qlem).cpu().detach().numpy()
        

        maxi=-1
        maxv=0
        for sentx in range(len(simvals)):
            ti = np.argmax(simvals[sentx])
            tv = np.max(simvals[sentx])
            if tv>maxv:
                maxi = ti
                maxv = tv

        
        qlevel.append((ql[maxi], maxv))

        
    
    qlevel.sort(key=lambda x: x[1], reverse=True)

    return qlevel






def getPredictions(txt):
    
    candidates={}
    
    for mx, model in enumerate(models):
        qlevel = predictForText(txt, s2q_a[mx], model)
    
        for i in list(range(config.topk)):

            (q1, v1) = qlevel[i]
            
            if q1 not in candidates:
                candidates[q1]=[]
                
                 
            if v1>=config.threshold:
                candidates[q1].append((mx, v1, q2s[mx][q1]))

    #print ()
    topschemas=[]
    #print (candidates)
    for q in candidates:
        sl = candidates[q]
        #print (q +"\t"+ str(len(sl)))
        
        if len(sl)>=config.modeltopk:
            (_, _, sname) = sl[0]
            if sname not in topschemas:
                topschemas.append(sname)
 
    
    return topschemas
        
if __name__=="__main__":
 
    if len(sys.argv)!=3:
        print ("args1: data.tsv, args2: outfile.tsv")
        sys.exit(1)
    
    data_file=sys.argv[1]
    preds_out_file=sys.argv[2]
    

    idcol = config.idcol
    txtcol = config.txtcol
    
    print ("Using data file "+data_file+" idcol="+str(idcol)+" txtcol="+str(txtcol))
    
    id2text = myutils.loadTexts(data_file, 0, 1)
    fout = open(preds_out_file, "w")
        

    for fid in id2text:
        txt = id2text[fid]       
        
        
        topschemas = getPredictions(txt)
        print ()
        #print ("\n"+txt)
        print (topschemas)
        tops = '\t'.join(topschemas)
        fout.write(fid+"\t"+tops.strip()+"\n")
        fout.flush()
        #print (candidates)
        
    
    fout.close()
    print ("Predictions written to "+preds_out_file)

