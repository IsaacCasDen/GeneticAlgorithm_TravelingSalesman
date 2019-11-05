
from concrete import *

import random
import os
import time
import datetime
import math
from multiprocessing import Pool, Queue

candidates = []
nodes = []
max_threads = 6
current_threads = 0

def fitness(specimen:TravelingSpecimen):
    fit = specimen.distance()
    return fit

def beginTests():
    print("Beginning Tests")
    initNodes()
    initCandidates()
    maxFit = 0
    sameCount = 0
    genCount = 0
    last_improved = 0
    while sameCount<100000:
        genCount+=1
        results = createCandidates()
        if results[0]>maxFit:
            last_improved = genCount
            display = round(results[0],6)>round(maxFit,6)
            maxFit = results[0]
            sameCount=0
            if display:
                print("Generation: ",genCount," \tMax Fit: ", round(maxFit,6), " \tMin Fit: ", round(results[1],6), " \tAverage Fit: ", round(results[2],6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))
        elif results[0] == maxFit:
            sameCount+=1
        # printCandidates()
        if genCount%100==0:
            print("Generation: ",genCount, " \tLast Improved Gen: ", last_improved," \tMax Fit: ", round(maxFit,6), " \tMin Fit: ", round(results[1],6), " \tAverage Fit: ", round(results[2],6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))

    print("---\nGeneration: ",genCount," \tMax Fit: ", round(maxFit,6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))        
    print("Best Candidates:")
    for i in range(0,3):
        print("Rank",i+1,"\t",candidates[i])
        

def printCandidates():
    f = []
    for c in candidates:
        f.append((c,c.fit))
    
    print(f)

def initNodes(_nodes = [], dimensions = 2, count = 16):
    global nodes
    
    if len(_nodes)>0:
        nodes = _nodes
        return

    mn = 0
    mx = 100

    for i in range(0,count):
        position = []
        for j in range(0,dimensions):
            position.append(random.randint(mn,mx))
        nodes.append(Node("Node " + str(i),Vector(position)))

def initCandidates(values:list = [], count = 24):
    global candidates
    global nodes

    if len(values)==0:
        for i in range(0,count):
            cand = nodes[:]
            vals = []
            start = random.choice(nodes)
            vals.append(start)
            cand.remove(start)

            while len(cand)>0:
                v = random.choice(cand)
                vals.append(v)
                cand.remove(v)
            
            vals.append(start)
                
            candidates.append(createCandidate(vals))
    else:
        for value in values:
            candidates.append(createCandidate(value))

def createCandidates():
    global candidates
    global current_threads
    global max_threads

    keepCount = len(candidates)
    cand = []
    old_fit = [value.fit for value in candidates]
    jobs = []
    values = []
    threads = []
    jobs = []
    q = Queue()
    
    for i in range(0,len(candidates)-1):
        # print("Starting Job ",i)
        job = (candidates[i],candidates[i+1])
        jobs.append(job)

    with Pool(max_threads) as p:
        values = p.map(combine,jobs)
    for v in values:
        cand.extend(v)

    # print("Values: ", str(cand))

    candidates.extend(cand)
    candidates.sort(key=lambda x:x.fit)
    fit = [value.fit for value in candidates]
    candidates = candidates[:keepCount]


    value = (fit[0],fit[len(fit)-1],(sum(fit)/len(fit))-sum(old_fit)/len(old_fit))

    return value

def thread(func,args):
    global current_threads

    result = func(args)
    return result

def combine(pair):
    values = []
    values.append(pair[0].combine(pair[1]))
    values.append(pair[1].combine(pair[0]))
    for v in values:
        v.fit = fitness(v)

    return values

def createCandidate(value):
    specimen = TravelingSpecimen(value)
    specimen.fit = fitness(specimen)
    return specimen

if __name__ == "__main__":
    
    beginTests()