
import random
import math

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
    def __init__(self,value:list,mutationCount = 0):
        self.value = value
        self.mutationCount = mutationCount

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
        # if hasMutation:
        #     mutInd = random.randint(0,len(self.value)-2)
        #     mutCount+=1

        if hasMutation:
            mutInd1 = random.randint(_min,_max)
            mutInd2 = None

            while mutInd2==None or mutInd2==mutInd1:
                mutInd2 = random.randint(_min,_max)

            v1 = self.value[mutInd1]
            v2 = self.value[mutInd2]

            self.value[mutInd2] = v1
            self.value[mutInd1] = v2

            mutCount+=1
        else:
            ind = None
            while ind == None or self.value[0] == other.value[ind]:
                ind = random.randint(_min,_max)
            
            rem = None

            for i in range(1,len(self.value)):
                if self.value[i]==other.value[ind]:
                    rem = i
                    break
            
            del newValue[rem]
            newValue.insert(ind,other.value[ind])

        # for i in range(1,(int(len(self.value)-1)/4)):
        #     n = None
        #     while n == None or n in ind:
        #         n = random.randint(0,len(self.value))
        #     ind.append(n)

        # for i in range(0,len(ind)):
            
            # newValue[i]=other.value[i]
        #if mutInd != None and mutInd == i:
        return TravelingSpecimen(newValue,mutCount)

# def combine(self, other):
#         _min = 1
#         _max = len(self.value)-2

#         newValue = self.value[:]
        
#         hasMutation = random.random()<0.02
#         mutInd = None
#         mutCount = max((self.mutationCount,other.mutationCount))
#         # if hasMutation:
#         #     mutInd = random.randint(0,len(self.value)-2)
#         #     mutCount+=1

#         if hasMutation:
#             mutInd1 = random.randint(_min,_max)
#             mutInd2 = None

#             while mutInd2==None or mutInd2==mutInd1:
#                 mutInd2 = random.randint(_min,_max)

#             v1 = self.value[mutInd1]
#             v2 = self.value[mutInd2]

#             self.value[mutInd2] = v1
#             self.value[mutInd1] = v2

#             mutCount+=1
#         else:
#             indices = []
#             while len(indices) < len(self.value)/2:
#                 ind = None
#                 while ind == None or self.value[0] == other.value[ind]:
#                     ind = random.randint(_min,_max)
#                 indices.append(ind)

#             for i in range(1,len(indices)):
#                 rem = None
#                 for j in range(1,len(self.value)):
#                     if self.value[j]==other.value[indices[i]]:
#                         rem = j
#                         break
#                 if rem != None:
#                     del newValue[rem]
#                     newValue.insert(indices[i],other.value[indices[i]])

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
        
        return BinarySpecimen(newValue,mutCount)

    def __str__(self):
        return "Value: " + str(self.value) + " Mutation Count:" + str(self.mutationCount)

    def __repr__(self):
        return self.__str__() + "\n"