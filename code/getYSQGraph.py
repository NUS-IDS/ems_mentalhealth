from sentence_transformers import SentenceTransformer, util
import numpy as np
import sys
from Config import sentence_transformer_model_id, device
model = SentenceTransformer(sentence_transformer_model_id, device)
sim_threshold = 0.5
normWeights=True



def loadYSQGraph(dprefix):
    
    nodes_file = dprefix+"/nodes.txt"
    
    lines = open (nodes_file, "r", encoding='utf-8').readlines()
    comb = []
    for l in lines:
        comb.append("")

    for lx, line in enumerate(lines):
        lp = line.strip().split("\t")
        nid = int(lp[-1])
        comb[nid] = lp[0].strip()

    print (len(comb))

    
    embedding_2= model.encode(comb, convert_to_tensor=True)
    
    return embedding_2
    
def computeSimilarity(sents, embedding_2):
    
    embedding_1= model.encode(sents, convert_to_tensor=True)
    simvals = util.cos_sim(embedding_1, embedding_2).cpu().detach().numpy()
    return simvals


if __name__=="__main__":

    if len(sys.argv)!=3:
        print("args1: ysq-file, args2: outdir")
        sys.exit(1)
        
    
    ysqfile = sys.argv[1]
    outdir=sys.argv[2]
    
    
    smap={}
    ems2ysq={}
    lines = open (ysqfile, "r").readlines()
    
    emsl=""
    for lx, line in enumerate(lines):
        key = line.replace(" ","").strip()
        if key.isupper():
            emsl=key
            print(emsl)
        else:
            line = line.strip()
            smap[line]=(emsl, len(smap))
            if emsl not in ems2ysq:
                ems2ysq[emsl]=[]

            ems2ysq[emsl].append(line.strip())

    
    print (len(smap))
    print (len(ems2ysq))


    comb = []
    for sent in smap:
        comb.append("")
    for sent in smap:
        _, sid = smap[sent]
        comb[sid]=sent

    print (len(comb))

    

    ##########BUILD THE GRAPH HERE
    nodes={}
    edges={}
    for ems in ems2ysq:

        embedding_2= model.encode(ems2ysq[ems], convert_to_tensor=True)
        for sx, sent in enumerate(ems2ysq[ems]):
            (_, s1id) = smap[sent]
            if s1id not in edges:
                edges[s1id]={}

            simvals = computeSimilarity([sent], embedding_2)

            for sx2, sent2 in enumerate(ems2ysq[ems]):

                (_, s2id) = smap[sent2]
                if simvals[0][sx2]>sim_threshold:
                    if s2id>s1id:
                        edges[s1id][s2id]=simvals[0][sx2]    
                

    ##########END BUILD 
    
    maxnodeid = len(comb)
    fout = open (outdir+"/edges.txt", "w")
    for nid1 in edges:
        total = 0
        for nid2 in edges[nid1]:
            total += edges[nid1][nid2]
        for nid2 in edges[nid1]:
            fout.write(str(nid1+1)+"\t"+str(nid2+1)+"\t"+str(edges[nid1][nid2]/total)+"\n")
            fout.flush()

    fout.write(str(maxnodeid)+"\t"+str(maxnodeid)+"\t0\n")
    fout.close()
    fout2 = open (outdir+"/emsmap.txt", "w")
    emsid=1
    for ems in ems2ysq:
        
        ysql = ems2ysq[ems]

      

        print (ems+"\t"+str(len(ysql)))

        total = len(ysql)
        weights = np.zeros(len(comb))
        for sent in ysql:
            (_, sx) = smap[sent]
            if normWeights:
                weights[sx] = 1/total
            else:
                weights[sx]=1
                
        fout2.write(ems+"\t"+str(emsid)+"\n")
        fout = open (outdir+"/"+str(emsid)+".txt","w")
        for weight in weights:
            fout.write(str(weight)+"\n")
            fout.flush()

        fout.close()
        emsid += 1

    fout2.close()
    fout = open (outdir+"/nodes.txt", "w")
    for sent in smap:
        (_, sx) = smap[sent]
        fout.write(sent+"\t"+str(sx)+"\n")
        fout.flush()

    fout.close()
        
    

    
