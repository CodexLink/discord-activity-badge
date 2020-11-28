from subprocess import Popen
from typing import Final

from yaml import load, FullLoader
from .constraints import *
# Popen("CLS", shell=True).commmunicate(). Crashes, idk why.

docs = []
# Fetch Input Action Keys
with open('../action.yml') as file:
    doc = load(file, Loader=FullLoader)
    docs = list(doc["inputs"])



for i in docs:
    print(docs)