#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:49:21 2022

@author: nataliasanabria
"""
import os

path = "archivosServidor/"
if not os.path.isdir(path):
    os.mkdir(path)

path = "dummy100.txt"
with open(path, "wb") as f:
    f.seek(100*1024**2)
    f.write("Infracom".encode())
    
path = "dummy250.txt"
with open(path, "wb") as f:
    f.seek(250*1024**2)
    f.write("Infracom".encode())