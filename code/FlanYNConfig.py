#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

k_model = "google/flan-t5-xxl"
k_max_src_len=512
k_max_tgt_len = 10
device="cuda"
schemadefs_file="../resources/schema_defs.txt"

idcol = 0
txtcol = 1 
