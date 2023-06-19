import math
import random


def readfile(filename):
    lines = open(filename).readlines()

    colnames = lines[0].strip().split("\t")[1:]
    rownames = []
    data = []

    for line in lines[1:]:
        p = line.strip().split("\t")
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def person(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    length = len(v1)

    pSum = sum([v1[i] * v2[i] for i in range(length)])

    # person coefficient
    num = pSum - (sum1 * sum2 / length)
    den = math.sqrt((sum1Sq - pow(sum1, 2) / length) * (sum2Sq - pow(sum2, 2) / length))
    if den == 0: return 0

    val =  1.0 - num / den #НЕ правильно, сейчас num / den возвращает от -1 до 1. А должен как в книге от 0 до 1.
    #val =  1.0 - (((num / den)+1)/2) #ужали значине с [-1,1] до [0,1]
    return val

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.distance = distance
        self.id = id

def hcluster(rows, distance=person):
    distances={}
    currentclustid=-1

    clust=[bicluster(rows[i],id=i)for i in range(len(rows))]

    while len(clust)>1:
        lowestpair=(0,1)
        closest= distance(clust[0].vec,clust[1].vec)

        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if(clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec)
                d=distances[(clust[i].id,clust[j].id)]

                if d<closest:
                    closest=d
                    lowestpair=(i,j)

        #calculate avg value for finded 2 closest cluster for combine
        mergevec=[ (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        #greate new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest, id = currentclustid)

        currentclustid -=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def rotatedata(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def kluster(rows,distance=person, k=4):
    ranges = [(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0])) ]

    #random k centroid
    clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(100):
        print("iteration №"+ str(t))
        bestmatches = [[]for i in range(k)]

        #find closest centroid
        for j in range(len(rows)):
            row = rows[j]
            bestmatche = 0
            for i in range(k):
                d=distance(clusters[i],row)
                if d < distance(clusters[bestmatche], row): bestmatche=i
            bestmatches[bestmatche].append(j)

        #if the same result
        if bestmatches ==lastmatches:break
        lastmatches=bestmatches

        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                    for j in range(len(avgs)):
                        avgs[j]/=len(bestmatches[i])
                    clusters[i]=avgs
    return bestmatches