"""
Copyright 2021 Janrey "CodexLink" Licas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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