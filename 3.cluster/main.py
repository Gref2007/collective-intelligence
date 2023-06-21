import generatefeedvector, cluster, draw

if __name__ == '__main__':
    blognames, words, data = cluster.readfile("blogdata.txt")
    #rdata = cluster.rotatedata(data)
    #kclust = cluster.kluster(data, k = 10)
    #draw.printkcluster(kclust, blognames)
    #clust = cluster.hcluster(data)
    #draw.printclust(clust,blognames)
    #draw.drawdendrogram(clust,words)
    coords = cluster.scaledown(data, rate=0.01)
    draw.draw2d(coords, blognames)

