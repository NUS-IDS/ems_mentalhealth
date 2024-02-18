#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 22:20:46 2023

@author: sdas
"""

import gradio as gr
import random
import time

import CommonUtils as myutils
import EPMFast as epmf

from RunChatGPTForMHQWithST import runForExample



labels = []
labels2={}
for line in open (epmf.config.labelsf, "r").readlines():
    labels.append(line.strip())
    labels2[line.strip().replace(" ","").strip()]=len(labels2)

##initialization

s2q, q2s, s2qem = myutils.loadS2QWithEmbeddings(epmf.config.questionairef, epmf.sim_model, epmf.config.device)


##end initialization   

def respondToVisitor(vmessage, emslabels):
    
    if len(emslabels)==0:
        emslabels, evidence = epmf.getEMSPredictions(vmessage, s2q, q2s, s2qem)
            #if len(emslabels)>0:
        print ("======================")
        print ("DEBUG EMS Labels inferred: "+str(emslabels))
        temp=[]
        for ems in emslabels:
            if ems.replace(" ","").strip() in labels2:
                temp.append(labels[labels2[ems.replace(" ","").strip()]])
        
        print ("DEBUG Evidence for EMS Labels: "+str(evidence))
        print ("======================")
    else:
        print ("======================")
        print ("DEBUG EMS Labels Specified: "+str(emslabels))
        temp = emslabels
        
        
    _, therapy_suggestions = runForExample(vmessage, emslabels)
    
    
    print ("======================")    
    print ("DEBUG Suggested Response:\n" + therapy_suggestions)
    print ("======================")
        
    return temp, therapy_suggestions



start_msg="Hello, how may I help you today? "
prev_amessage=""
 





with gr.Blocks() as demo:
    
    def respond(message, cbg, chat_history):
        
        print (message)
        print (cbg)
        #prevconv = "STCounselor: "+prev_amessage+" Visitor: "+message
        temp_ems, bot_message = respondToVisitor(message, cbg)
        
        
        chat_history.append((message, bot_message))
        time.sleep(1)
        
        return "", temp_ems, chat_history
    
    with gr.Row():
        with gr.Column(scale=3):
            gr.Image("therapist.png", label="STC")#, scale=2)
            
            
                    
            
            cbg = gr.CheckboxGroup(labels, label="EMS Labels (if available)")
        with gr.Column(scale=15):
            
            amsg = start_msg
            prev_amessage=amsg
            
            
            chatbot = gr.Chatbot(label="STCounselor", value=[[None, amsg]])
            msg = gr.Textbox(lines=4, value="Enter your question here")
            with gr.Row():
                # with gr.Column(scale=1):
                #     cb = gr.Checkbox(label="EMS Labels Included", interactive=True, value=False)
                with gr.Column(scale=1):
                    #clear = gr.ClearButton([msg, chatbot])
                    clear = gr.ClearButton([msg, cbg])
                with gr.Column(scale=1):
                    submitbutton = gr.Button(value="Submit")
                
            submitbutton.click(respond, [msg, cbg, chatbot], [msg, cbg, chatbot])
            
            
demo.launch()


