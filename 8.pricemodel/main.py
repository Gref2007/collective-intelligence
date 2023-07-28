import  numpredict, optimization

if __name__ == '__main__':


    '''
    data = numpredict.wineset1()
    print(numpredict.weightedknn(data,(70,5)))

    print(numpredict.crossvalidate(numpredict.weightedknn, data))
    print(numpredict.crossvalidate(numpredict.knnestimate, data))

    def wknn3(d,v): return numpredict.weightedknn(d,v,k = 3)
    def knn3(d, v): return numpredict.knnestimate(d, v, k=3)


    print(numpredict.crossvalidate(wknn3, data))
    print(numpredict.crossvalidate(knn3, data))
    '''

    data = numpredict.wineset2()

    #print(numpredict.crossvalidate(numpredict.weightedknn, data))
    #print(numpredict.crossvalidate(numpredict.knnestimate, data))


    def wknn3(d, v): return numpredict.weightedknn(d, v, k=3)


    def knn3(d, v): return numpredict.knnestimate(d, v, k=3)


    #print(numpredict.crossvalidate(wknn3, data))
    #print(numpredict.crossvalidate(knn3, data))

    #costf = numpredict.createcostfunction(numpredict.knnestimate, data)
    #print( optimization.annealingoptimize(numpredict.weightdomain, costf, step=2))

    data = numpredict.wineset3()

    print(numpredict.probguess(data,[99,20],40,80))
    print(numpredict.probguess(data, [99, 20], 80, 120))
    print(numpredict.probguess(data, [99, 20], 120, 1000))
    print(numpredict.probguess(data, [99, 20], 30, 120))

    #numpredict.cumulativegraph(data,(1,1),120)
    numpredict.probabilitygraph(data, (1, 1), 120)
