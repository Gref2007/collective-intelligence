import treepredict

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print(treepredict.divideset(treepredict.my_data,2,"yes"))
    #print(treepredict.giniimpurity(treepredict.my_data))
    #print(treepredict.entropy(treepredict.my_data))
    tree = treepredict.buildtree(treepredict.my_data)
    #treepredict.printtree(tree)
    treepredict.prune(tree, 0.8)
    treepredict.drawtree(tree, "prunetree.jpg")
    #print(treepredict.classify(['(direct)','UAS','yes',5],tree))
    print(treepredict.mdclassify(['google', None, 'yes', None], tree))