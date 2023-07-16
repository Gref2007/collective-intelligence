import docclass

if __name__ == '__main__':

    """
    
    cl=docclass.classifier(docclass.getwords)
    docclass.sampletrain(cl)
    print(cl.fprob("money","good"))
    print(cl.weightedprob("money", "good", cl.fprob))
    docclass.sampletrain(cl)
    print(cl.weightedprob("money", "good", cl.fprob))
    """

    """
    cl = docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    print(cl.prob("quick rabbit", "good"))
    print(cl.prob("quick rabbit", "bad"))
    """

    """
    cl = docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    print(cl.classify("quick rabbit", default="unknown"))
    print(cl.classify("quick money", default="unknown"))
    cl.setthreshold("bad",3.0)
    print(cl.classify("quick money", default="unknown"))
    for i in range(10): docclass.sampletrain(cl)
    print(cl.classify("quick money", default="unknown"))
    """
    """
    cl = docclass.fisherclassifier(docclass.getwords)
    docclass.sampletrain(cl)
    print(cl.cprob("quick", "good"))
    print(cl.fisherprob("quick rabbit", "good"))
    print(cl.fisherprob("quick rabbit", "bad"))
    """

    """    
    cl = docclass.fisherclassifier(docclass.getwords)
    docclass.sampletrain(cl)
    print(cl.classify("quick rabbit"))
    print(cl.classify("quick money"))
    cl.setminimum("bad",0.8)
    print(cl.classify("quick rabbit"))
    cl.setminimum("good", 0.4)
    print(cl.classify("quick money"))
    """

    cl = docclass.fisherclassifier(docclass.getwords)
    cl.setdb("test.db")
    docclass.sampletrain(cl)
    cl2 = docclass.naivebayes(docclass.getwords)
    cl2.setdb("test.db")
    print(cl2.classify("quick money"))


