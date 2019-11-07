#target < 10800
from concrete import *

import random
import os, sys, csv
import time
import datetime
import math

candidates = []
nodes = []
max_threads = 6
current_threads = 0
workers = []

def fitness(specimen:TravelingSpecimen):
    fit = specimen.distance()
    return fit

def initWorkers():
    for i in range(0,max_threads):
        w = Worker(i, combine)
        w.start()
        workers.append(w)

def beginTests(_nodes = []):
    data = "data{0}.csv"
    output = "output{0}.txt"

    index = 0
    while os.path.exists(data.format(index)):
        index += 1
    
    data_path = data.format(index)

    index = 0
    while os.path.exists(output.format(index)):
        index += 1

    output_path = output.format(index)

    o = open(output_path,"w")
    d = open(data_path,"w")

    print("Beginning Tests")
    initNodes(_nodes)
    initCandidates()

    output_header = "Generation\tMax Fit\tMin Fit\tAverage Fit\tCandidates\tTime\n"
    data_header = "Generation,Id,Fitness,Mutation Count,Parent A,Parent B"
    
    index = 0
    for v in candidates[0].value:
        data_header += ",Value {0}".format(index)
        index += 1
    data_header += "\n"

    o.write(output_header)
    d.write(data_header)
    
    output = ""
    for c in candidates:
        output += "{0},{1},{2},{3},{4},".format(str(0),str(c.id),str(c.fit),str(c.mutationCount),str(c.parentIdA),str(c.parentIdB))
        output += ",".join(map(str,c.value))
        output += "\n"

    d.write(output)

    # initWorkers()
    maxFit = None
    sameCount = 0
    genCount = 0
    last_improved = 0
    print(output_header)
    while sameCount<100000:
        genCount+=1
        results = createCandidates()
        if maxFit == None or results[0]<maxFit:
            output = ""
            for c in candidates:
                output += "{0},{1},{2},{3},{4},".format(str(genCount),str(c.id),str(c.fit),str(c.mutationCount),str(c.parentIdA),str(c.parentIdB))
                output += ",".join(map(str,c.value))
                output += "\n"

            d.write(output)
            exit(1)

            last_improved = genCount
            display = maxFit == None or round(results[0],6)<round(maxFit,6)
            maxFit = results[0]
            sameCount=0
            if display:
                output = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(genCount,round(maxFit,6),round(results[1],6),round(results[2],6),len(candidates),str(datetime.datetime.now()))
                print(output)
                o.write(output + "\n")
        elif results[0] == maxFit:
            sameCount+=1
        # printCandidates()
        if genCount%10000==0:
            output = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(genCount,round(maxFit,6),round(results[1],6),round(results[2],6),len(candidates),str(datetime.datetime.now()))
            o.write(output + "\n")
            print("Generation: ",genCount, " \tLast Improved Gen: ", last_improved," \tMax Fit: ", round(maxFit,6), " \tMin Fit: ", round(results[1],6), " \tAverage Fit: ", round(results[2],6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))

    print("---\nGeneration: ",genCount," \tMax Fit: ", round(maxFit,6), " \tCandidates: ", len(candidates), " \tTime: ", str(datetime.datetime.now()))        
    print("Best Candidates:")
    for i in range(0,3):
        print("Rank",i+1,"\t",candidates[i])
    
    d.close()
    o.close()

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

def initCandidates(values:list = [], count = 512):
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
    global workers
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
    
    for i in range(0,len(candidates)-1):
        # print("Starting Job ",i)
        job = (candidates[i],candidates[i+1])
        jobs.append(job)

    if len(workers) == 0:
        for job in jobs:
            results = combine(job)
            cand.extend(results)
    else:
        split_count = len(workers)
        
        for i in range(0,split_count):
            s = int(i * (len(jobs)/split_count))
            e = int((i + 1) * (len(jobs)/split_count))
            if e>len(jobs):
                e=len(jobs)
            # print(i,s,e)
            workers[i].add_jobs(jobs[s:e])
        
        running = True
        while running:
            running = False
            for w in workers:
                if w.jobs_pending:
                    running = True
                    time.sleep(0.05)
                    break
        
        for w in workers:
            results = w.get_last_results()
            if results != None:
                for result in results:
                    cand.extend(result)
            else:
                print("Error getting results")
                exit(1)

    [candidates.append(value) for value in cand if value not in candidates]
    candidates.sort(key=lambda x:x.fit)
    fit = [value.fit for value in candidates]
    candidates = candidates[:keepCount]

    value = (fit[0],fit[len(fit)-1],(sum(fit)/len(fit))-sum(old_fit)/len(old_fit))
    return value

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

def read_file(path):
    values = []
    _id = 0
    with open(path,"r") as f:
        for line in f.readlines():
            val = line.rstrip("\n").split(",")
            pos = []
            for v in val:
                pos.append(int(v))
            n = Node(_id,Vector(pos))
            _id += 1
            values.append(n)

    return values

if __name__ == "__main__":
    _nodes = []
    if len(sys.argv) > 1:
        _nodes = read_file(sys.argv[1])
    beginTests(_nodes)