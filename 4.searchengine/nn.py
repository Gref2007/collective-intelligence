import math
import sqlite3


def dtanh(y):
    return 1.0 - y * y



class searchnet:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute("create table hiddennode(create_key)")
        self.con.execute("create table wordhidden(fromid, toid, strength)")
        self.con.execute("create table hiddenurl(fromid, toid, strength)")
        self.con.commit()

    def getstrength(self, fromid, toid, layer):
        if layer == 0:
            table = "wordhidden"
        else:
            table = "hiddenurl"
        res = self.con.execute(f"select strength from {table} where fromid = {fromid} and toid = {toid}").fetchone()
        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0:
            table = "wordhidden"
        else:
            table = "hiddenurl"
        res = self.con.execute(f"select rowid from {table} where fromid = {fromid} and toid = {toid}").fetchone()

        if res == None:
            self.con.execute(f"insert into {table} (fromid,toid,strength) values ({fromid},{toid},{strength})")
        else:
            rowid=res[0]
            self.con.execute(f"update  {table} set strength = {strength} where rowid = {rowid}")

    def generatehiddennode(self, wordids, urls):
        if len(wordids)>3: return None
        #check if already created
        createkey = "_". join(sorted([str(wi) for wi in wordids]))
        res = self.con.execute(f"select rowid from hiddennode where create_key='{createkey}'").fetchone()

        #if not, then create now
        if res==None:
            cur=self.con.execute(f"insert into hiddennode (create_key) values ('{createkey}')")
            hiddenid = cur.lastrowid

            # add weight by default
            for wordid in wordids:
                self.setstrength(wordid,hiddenid,0,1.0/len(wordids))
            for urlid in urls:
                self.setstrength(hiddenid,urlid,1,0.1)
            self.con.commit()

    def getallhiddenids(self,wordids, urlids):
        l1={}
        for wordid in wordids:
            cur = self.con.execute(f"select toid from wordhidden where fromid = {wordid}")
            for row in cur:l1[row[0]]=1
        for urlid in urlids:
            cur = self.con.execute(f"select fromid from hiddenurl where toid = {urlid}")
            for row in cur: l1[row[0]] = 1
        return list(l1.keys())

    def setupnetwork(self, wordids, urlids):
        self.wordids=wordids
        self.hiddenids=self.getallhiddenids(wordids,urlids)
        self.urlids = urlids

        #output signals from nodes
        self.ai = [1.0]*len(self.wordids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.urlids)

        #greate matrix of weights
        self.wi = [[self.getstrength(wordid, hiddenid,0) for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.wo = [[self.getstrength(hiddenid,urlid,1) for urlid in self.urlids ] for hiddenid in self.hiddenids]

    def feedforward(self):
        # only signals it is word from query, so they will have 1 point strong
        for i in range(len(self.wordids)):
            self.ai[i]=1.0

        #stimulation of hidden nodes
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i]*self.wi[i][j]
            self.ah[j]= math.tanh(sum)

        #stimulation of otput nodes
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum+self.ah[j]*self.wo[j][k]
            self.ao[k]= math.tanh(sum)

        return self.ao[:]

    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids,urlids)
        return self.feedforward()

    def backPropagate(self, targets, N=0.5):
        #find correction for output layer
        output_deltas = [0.0]*len(self.urlids)
        for k in range(len(self.urlids)):
            error= targets[k]-self.ao[k]
            output_deltas[k]= dtanh(self.ao[k])*error

        #calculate correction for hidden layer
        hidden_deltas = [0.0]*len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error = error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j])*error

        #update weight connection between hidden level and output level
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k]=self.wo[j][k]+ N*change

        #update weight connection between input level and hidden level
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j]+N*change

    def trainauery(self, wordids, urlids, selectedurl):
        #generate hidden node if need
        self.generatehiddennode(wordids, urlids)

        self.setupnetwork(wordids,urlids)
        self.feedforward()

        targets = [0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        error = self.backPropagate(targets)
        self.updatedatabase()

    def updatedatabase(self):
        #write to database
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.wordids[i], self.hiddenids[j], 0, self.wi[i][j])
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids[j], self.urlids[k], 1, self.wo[j][k])
        self.con.commit()

