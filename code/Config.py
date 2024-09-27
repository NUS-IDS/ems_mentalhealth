#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:03:19 2024

@author: sdas
"""


sentence_transformer_model_id="sentence-transformers/all-distilroberta-v1"
device="cuda"
epm_model_id="t5-large"
ppr_script="/home/sdas/pagerank/tspagerank"
ppr_damping_factor=0.86
ppr_ysq_dir="/home/sdas/ecai24/supmat/upload/temp"

scratch_dir="/tmp"
ysq_file="resources/YSQuestionnaire.txt"

