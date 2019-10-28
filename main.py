
from concrete import *

import random
import os
import datetime
from multiprocessing import Process

candidates = []

def fitness(specimen:Specimen):
    ideal = 128
    value = 0
    for val in specimen.value:
        value+=val
    return value/ideal

def beginTests():
    print("Beginning Tests")
    initCandidates()
    maxFit = 0
    sameCount = 0
    genCount = 0
    while sameCount<1000:
        genCount+=1
        newFit = createCandidates()
        if newFit>maxFit:
            maxFit = newFit
            sameCount=0
            print("Generation: ",genCount," \tMax Fit: ", round(maxFit,6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))
        elif newFit == maxFit:
            sameCount+=1
        # printCandidates()
    print("---\nGeneration: ",genCount," \tMax Fit: ", round(maxFit,6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))        
    print("Best Candidates:")
    for i in range(0,3):
        print("Rank",i+1,"\t",candidates[i])
        

def printCandidates():
    f = []
    for c in candidates:
        f.append((c,c.fit))
    
    print(f)

def initCandidates(values:list = [], count = 24):
    if len(values)==0:
        for i in range(0,count):
            value = []
            for i in range(0,128):
                value.append(random.getrandbits(1))
            candidates.append(createCandidate(value))
    else:
        for value in values:
            candidates.append(createCandidate(value))

def createCandidates():
    global candidates
    keepCount = len(candidates)
    cand = []
    for i in range(0,len(candidates)-1):
        values = combine(candidates[i],candidates[i+1])
        # p = Process(target = combine, args = (candidates[i],candidates[i+1],))
        # p.start()
        # values = p.join()
        cand.extend(values)

    candidates.extend(cand)
    candidates.sort(key=lambda x:x.fit,reverse=True)
    candidates = candidates[:keepCount]
    return candidates[0].fit


def combine(s1:Specimen, s2:Specimen):
    values = []
    values.append(s1.combine(s2))
    values.append(s2.combine(s1))
    for v in values:
        v.fit = fitness(v)

    return values

def createCandidate(value):
    specimen = Specimen(value)
    specimen.fit = fitness(specimen)
    return specimen

if __name__ == "__main__":
    
    beginTests()