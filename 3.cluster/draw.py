from PIL import Image,ImageDraw

def printclust(clust, labels=None, n=0):
    print(" "*n,end="")
    if clust.id <0:
        print("-")
    else:
        if labels==None:
            print(clust.id)
        else:
            print(labels[clust.id])

    if clust.left != None: printclust(clust.left, labels, n=n+1)
    if clust.right != None: printclust(clust.right, labels, n=n + 1)

def getheight(clust):
    # if leaf
    if clust.left==None and clust.right ==None: return 1

    return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
    if clust.left==None and clust.right==None: return 0
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

def drawdendrogram (clust, labels, jpeg='cluster.jpg'):
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)

    scaling = float(w-150)/depth

    img=Image.new("RGB",(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    img.save(jpeg, "JPEG")


    drawnode(draw,clust,10,(h/2),scaling,labels, img)

    img.save(jpeg,"JPEG")

def drawnode(draw,clust,x,y,scaling, labels,img):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2 = getheight(clust.right) * 20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2

        #line lenght
        ll=clust.distance*scaling

        #vertical line from this cluster to child
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        #horizontal to 1 child
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        #horizontla to 2 child
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        img.save('cluster.jpg', "JPEG")
        drawnode(draw,clust.left,x+ll,top+h1/2, scaling,labels,img)
        img.save('cluster.jpg', "JPEG")
        drawnode(draw, clust.right, x+ll, bottom - h2/2, scaling, labels,img)
        img.save('cluster.jpg', "JPEG")
    else:
        draw.text((x+5,y-7),labels[clust.id],fill=(0,0,0))