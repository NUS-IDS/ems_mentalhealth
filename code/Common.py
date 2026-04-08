#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 15:41:48 2024

"""


import time
from openai import OpenAI
import json 
import ast
##KEY needs to be set

GPT_KEY="[YOUR API KEY FROM OPENAI]"
GEMINI_API_KEY="[YOUR API KEY FROM GOOGLE]"


CHATGPT_MODEL = "gpt-5-mini" #"gpt-4o"
GEMINI_MODEL = "gemini-3-flash-preview" #"gemini-2.5-flash"


def getChatGPTResponse(userprompt, sysprompt="", \
                gptms=CHATGPT_MODEL): #, temperature=0.7):
    try:
 

        client = OpenAI(
            # This is the default and can be omitted
            api_key=GPT_KEY,
        )
        messages=[]
        if sysprompt!="":
            messages.append({"role": "system", "content": sysprompt})
        messages.append({"role": "user", "content": userprompt})
            
        completion = client.chat.completions.create(
            model=CHATGPT_MODEL,
            messages = messages) #,
            #temperature=temperature)
    
        return (completion.choices[0].message.content)
    except:
        print ("Error in GPT call")
        return None

def getGeminiResponse(userprompt, sysprompt, temperature=0.7):
    try:
        
        client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        response = client.chat.completions.create(
            model=GEMINI_MODEL,
            messages=[
                {"role": "system", "content": sysprompt},
                {
                    "role": "user",
                    "content": userprompt
                }
            ]) 
        #,
        #    temperature=temperature)
        
    
        return response.choices[0].message.content
    except:
        print ("Error in Gemini call")
        return None





def parseJSONWithKeys(opstring):
    
    try:
        opstring = opstring.replace("```json","").replace("```","")
        # print (type(opstring))
        # if opstring.startswith("["):
        #     try:
        #         temp = ast.literal_eval (opstring)
        #         return temp
        #     except:
        #         print ("ast eval did not work")
        
        pl = json.loads(opstring)
        return pl
        
    except ValueError:
        #print ("JSON appears invalid")
        return None

