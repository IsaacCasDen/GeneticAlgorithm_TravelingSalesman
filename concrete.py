
import random

class Object:
    def __str__(self):
        return super().__str__()

class TravelingSpecimen(Object):
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
            mutInd = random.randint(0,len(self.value)-2)
            mutCount+=1

        for i in range(0,int(len(self.value)/2)):
            n = None
            while n == None or n in ind:
                n = random.randint(0,len(self.value))
            ind.append(n)

        for i in range(0,len(newValue)):
            if i not in ind:
                newValue[i]=other.value[i]
        #if mutInd != None and mutInd == i:
        return Specimen(newValue,mutCount)

    def __str__(self):
        return "Value: " + str(self.value) + " Mutation Count:" + str(self.mutationCount)

    def __repr__(self):
        return self.__str__() + "\n"

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
        
        return Specimen(newValue,mutCount)

    def __str__(self):
        return "Value: " + str(self.value) + " Mutation Count:" + str(self.mutationCount)

    def __repr__(self):
        return self.__str__() + "\n"