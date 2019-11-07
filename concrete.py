
import random
import math
import time
from collections import deque
from threading import Thread, Lock
from multiprocessing import Process

class Worker(Thread):
    def __init__(self, id, func):
        super(Worker,self).__init__()
        self.id = id
        self.func = func
        self.jobs_pending = False
        self.results = []
        self.new_jobs = deque()
        self.jobs_completed = 0
        self.running = True

    def run(self):
        while self.running:
            # print(self.id, "Checking for jobs",self.jobs_pending,str(self.jobs_completed))
            # print(self.new_jobs)
            if len(self.new_jobs)==0:
                # print(self.id, "No jobs")
                self.jobs_pending = False
                time.sleep(1)
                next
            else:
                # print(self.id, "Found jobs")
                self.job_running = True
                # print(self.id,"Starting Job",str(self.jobs_completed))
                jobs = self.new_jobs.popleft()
                result = []
                for job in jobs:
                    result.append(self.func(job))
                
                self.results.append(result)
                self.jobs_completed += 1
                # print(self.id,"Job",str(self.jobs_completed),"Completed")
                self.job_running = False
        print(self.id, "Exiting")

    def add_jobs(self, new_jobs):
        self.new_jobs.append(new_jobs)
        self.jobs_pending = True
        self.jobs_complete = False
        # print(self.id, "Adding", str(len(new_jobs)), " Jobs",self.jobs_pending,self.jobs_complete,str(self.jobs_completed))

    def get_last_results(self):
        if self.jobs_completed>0:
            return self.results[self.jobs_completed-1]
        else:
            return None
    

class Vector:
    def __init__(self, position:list = [0,0,0]):
        self.position = position
        
    def dim(self):
        return len(self.position)

    def distance(self,other):
        return Vector.distance(self,other)
    
    def __str__(self):
        return str(self.position)

    @staticmethod
    def distance(vec1, vec2):
        
        value = 0
        dim = min(vec1.dim(),vec2.dim())

        for i in range(0,dim):
            value += math.sqrt(abs(pow(vec1.position[i],2)-pow(vec2.position[i],2)))

        return value

class Node:
    def __init__(self, id, position:Vector = Vector()):
        self.id = id
        self.position = position

    def __eq__(self, value):
        if not isinstance(value,Node):
            return self.id == value
        
        if self is value:
            return True
        
        return self.id == value.id
    
    def __ne__(self, value):
        return not self.__eq__(value)
    
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return self.__str__()

class Object:
    def __str__(self):
        return super().__str__()

class TravelingSpecimen(Object):

    lock = Lock()
    __id__ = 0
    @staticmethod
    def __new_id__():
        TravelingSpecimen.lock.acquire()
        new_id = TravelingSpecimen.__id__
        TravelingSpecimen.__id__ += 1
        TravelingSpecimen.lock.release()
        return new_id

    

    def __init__(self, value:list, id = None, parentIdA = None, parentIdB = None, mutationCount = 0):
        if id == None:
            self.id = TravelingSpecimen.__new_id__()
        self.parentIdA = parentIdA
        self.parentIdB = parentIdB
        self.mutationCount = mutationCount
        self.value = value

    def distance(self):
        value = 0

        for i in range(0,len(self.value)-1):
            v1 = self.value[i]
            v2 = self.value[i+1]
            value += Vector.distance(v1.position,v2.position)
        
        return value

    def combine(self, other):
        _min = 1
        _max = len(self.value)-2

        newValue = self.value[:]
        
        hasMutation = random.random()<0.02
        mutInd = None
        mutCount = max((self.mutationCount,other.mutationCount))

        # print(newValue)
        if hasMutation:
            mutInd1 = random.randint(_min,_max)
            mutInd2 = None

            while mutInd2==None or mutInd2==mutInd1:
                mutInd2 = random.randint(_min,_max)

            v1 = newValue[mutInd1]
            v2 = newValue[mutInd2]

            newValue[mutInd2] = v1
            newValue[mutInd1] = v2

            mutCount+=1
        
        indices = []
        while len(indices)<len(newValue)/2:
            ind = None
            while ind == None or newValue[0] == other.value[ind] or ind in indices:
                ind = random.randint(_min,_max)
            indices.append(ind)
        
        remove = []
        
        for i in range(0,len(indices)):
            ind = None
            for j in range(1,len(newValue)-1):
                if newValue[j]==other.value[indices[i]]:
                    ind = j
                    break   
            
            if ind == None:
                print("Error",other.value[indices[i]]," not in ", newValue)
                exit(1)
            else:
                newValue[ind] = None
        
        indices.sort(reverse = False)

        # output = "Adding: "
        # for i in indices:
        #     output+=str(other.value[i]) + " "
        # output += "\nRemoving: "
        # for i in remove:
        #     output += str(newValue[i]) + " "

        # print(output)

        # print(self.value)
        # print(newValue)
        # print()

        while len(indices)>0:
            ind = indices.pop()
            i = ind+1
            while i<len(newValue):
                if newValue[i] == None:
                    del newValue[i]
                else:
                    i+=1

            newValue.insert(ind,other.value[ind])

        i=0
        while i < len(newValue):
            if newValue[i] == None:
                del newValue[i]
            else:
                i += 1

        # print(indices)
        # print(remove)
        # exit(1)

        # print(self.value)
        # print(newValue)
        # print()

        for val in self.value:
            if val not in newValue:
                print("Error: Missing Value",val)
                print(self.value)
                print(newValue)
                exit(1)
        
        

        # print(self.value)
        # print(newValue)
        # exit(1)
            
        
        # print(newValue)
        return TravelingSpecimen(newValue,None, self.id, other.id, mutCount)

    def __str__(self):
        return "Id: {0} Mutation Count: {1} Parent A: {2} Parent B: {3} Values: [{4}]".format(str(self.id),str(self.mutationCount),str(self.parentIdA),str(self.parentIdB),self.value)

    def __repr__(self):
        return self.__str__() + "\n"

    def __eq__(self, value):
        if not isinstance(value,TravelingSpecimen):
            return self.value == value
        
        return self.value == value.value
    
    def __ne__(self, value):
        return not self.__eq__(value)

class BinarySpecimen(Object):
    def __init__(self,value:list,mutationCount = 0):
        self.value = value
        self.mutationCount = mutationCount

    def combine(self, other):
        ind = []
        newValue = self.value[:]
        
        hasMutation = random.random()<0.02
        mutInd = None
        mutCount = max((self.mutationCount,other.mutationCount))
        if hasMutation:
            mutInd = random.randint(0,len(self.value)-1)
            mutCount+=1

        for i in range(0,int(len(self.value)/2)):
            n = None
            while n == None or n in ind:
                n = random.randint(0,len(self.value))
            ind.append(n)

        for i in range(0,len(newValue)):
            if mutInd != None and mutInd == i:
                if newValue[i]==0:
                    newValue[i]=1
                else:
                    newValue[i]=0
            elif i not in ind:
                newValue[i]=other.value[i]
        
        return BinarySpecimen(newValue,mutCount)

    def __str__(self):
        return "Value: " + str(self.value) + " Mutation Count:" + str(self.mutationCount)

    def __repr__(self):
        return self.__str__() + "\n"