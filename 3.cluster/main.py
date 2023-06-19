import generatefeedvector, cluster, draw

if __name__ == '__main__':
    blognames, wors, data = cluster.readfile("blogdata.txt")
    clust = cluster.hcluster(data)
    #draw.printclust(clust,blognames)
    draw.drawdendrogram(clust,blognames)

