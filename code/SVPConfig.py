#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

device="cuda:0"
questionairef="../resources/YSQuestionnaire.txt"
topk=5
threshold = 0.4
modeltopk=2

st_model1='sentence-transformers/all-mpnet-base-v2'
st_model2='sentence-transformers/all-distilroberta-v1'
st_model3='sentence-transformers/all-MiniLM-L12-v2'

idcol = 0
txtcol = 1    
