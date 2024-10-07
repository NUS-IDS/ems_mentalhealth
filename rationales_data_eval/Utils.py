

prompt_pfx="Here is the definition for the label "
prompt_mid=" Question: Is this label applicable to the context? Answer True or False. Context="

def makePrompt(ems, emsdef, text):
    prompt = prompt_pfx+" "+ems+": "+emsdef+"\". "+prompt_mid+text
    return prompt

def makePrompt1(emslist, text, evidence):
    prompt = "Question: Which of the labels in the list is most applicable to the context? Labels="+str(emslist)+" Context="+evidence+" [SEP] "+text
    return prompt

def makePrompt5(emslist, evidence):
    prompt = "Question: Which of the labels in the list is most applicable to this sentence?  Labels="+str(emslist)+" Sentence="+evidence
    return prompt

def rationalePrompt(emslist):
    prompt = "Question: What sentences in the context are indicative of the following labels? Labels="+str(emslist)+" Context="
    return prompt
def makePrompt2(ems, text):
    prompt ="Question: Is the EMS label "+ems+" applicable to the following context? Context="+text
    return prompt

def makePrompt3(ems, text):
    prompt ="Question: What sentence in the following context is indicative of the label: "+ems+" ? Context="+text
    return prompt

def makePrompt4(ems, text):
    prompt ="Question: What sentence in the following context is indicative of the label: "+ems+" ? Context="+text
    return prompt
def loadSchemaDefinitionsFile(inpf):

    defs={}

    lines = open (inpf, "r").readlines()
    stype=""
    for line in lines:
        l = line.strip()
        if l=="":
            continue
        if l.strip().isupper():
            stype = l.replace(" ","").strip()
            defs[stype]=""
        elif stype!="":
            defs[stype] +=" "+l.strip()

    return defs

def makeMCQPrompt(inpf):
    prompt="Given the following labels "# definitions: "
    lines = open (inpf, "r").readlines()
    for line in lines:
        l = line.strip()
        if l=="":
            continue
        if l.isupper():
            prompt +="\n"+l
#        else:
#            prompt  +=" "+l.strip()

    prompt +="\nQuestion: Which of the above labels is most applicable, given the following evidence and context? "
    return prompt

def makeMCQPrompt2(inpf):
    prompt="Given the following labels "# definitions: "
    lines = open (inpf, "r").readlines()
    for line in lines:
        l = line.strip()
        if l=="":
            continue
        if l.isupper():
            prompt +="\n"+l
#        else:
#            prompt  +=" "+l.strip()

    prompt +="\nQuestion: Which of the above labels are most applicable, given the following context? Select top-3. Context= "
    return prompt

def loadEMSList(inpf):

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

    return defs

if __name__=="__main__":
    sdefs = loadSchemaDefinitionsFile("schema_defs.txt")
    print (len(sdefs))


    for key in sdefs:
        print (key)
        print (sdefs[key])
