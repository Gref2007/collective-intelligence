import re

from bs4 import BeautifulSoup
import bs4
from urllib import request,parse
import sqlite3

ignorewords = {"the","of", "to","and", "a", "in", "is", "it"}

class crawler:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self,table, field, value, createnew=True):
        cur = self.con.execute("select rowid from {0:s} where {1:s}='{2:s}'".format(table,field, value))
        res = cur.fetchone()
        if res ==None:
            cur = self.con.execute("insert into {0:s}({1:s}) values('{2:s}')".format(table,field,value))
            return cur.lastrowid
        else: return res[0]

    #index new page
    def addtopindex(self, url, soup):
        if self.isindexed(url):return
        print("indexing {0:s}".format(url))

        #get list of words
        text=self.gettextonly(soup)
        words = self.separatewords(text)

        #get url id
        urlid = self.getentryid("urllist","url", url)


        #link word with url
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords:continue
            wordid = self.getentryid("wordlist","word", word)
            self.con.execute("insert into wordlocation(urlid, wordid, location)\
                             values ({0:d}, {1:d}, {2:d})".format(urlid,wordid,i))

    #get text from html without html
    def gettextonly(self, soup):
        if soup.name in ("script","style","meta") or type(soup) == bs4.element.Comment: return
        v=soup.string
        if v ==None:
            c=soup.contents
            resulttext=""
            for t in c:
                subtext = self.gettextonly(t)
                if subtext:
                    resulttext += subtext + "\n"
            return  resulttext
        else:
            return v.strip()

    def separatewords(self, text):
        splitter = re.compile('\\W+')
        return [s.lower() for s in splitter.split(text) if s!= ""]

    def isindexed(self, url):
        u = self.con.execute("select rowid from urllist where url='{0:s}'".format(url)).fetchone()
        if u!= None:
            v=self.con.execute("select * from wordlocation where urlid = {0:d}".format(u[0])).fetchone()
            if v!=None:return True
        return False


    #link from one page to another
    def addlinkref(self,urlFrom, urlTo, lingText):
        pass

    def crawl(self, pages, depth=1):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=request.urlopen(page)
                except:
                    print("can't open {0:s}".format(page))
                    continue
                soup=BeautifulSoup(c.read())
                self.addtopindex(page,soup)

                links=soup("a")
                for link in links:
                    if("href" in dict(link.attrs)):
                        url=parse.urljoin(page, link["href"])
                        if url.find("'")!=-1: continue
                        url = url.split("#")[0]
                        if url[0:4]=="http" and not self.isindexed(url):
                            newpages.add(url)
                            linkText=self.gettextonly(link)
                            self.addlinkref(page,url,linkText)
                self.dbcommit()
            pages=newpages



    def creatindextables(self):
        self.con.execute("create table urllist(url)")
        self.con.execute("create table wordlist(word)")
        self.con.execute("create table wordlocation(urlid, wordid,location)")
        self.con.execute("create table link(fromid integer, toid integer)")
        self.con.execute("create table linkwords(wordid, linkid)")

        self.con.execute("create index wordidx on wordlist(word)")
        self.con.execute("create index ulridx on urllist(url)")
        self.con.execute("create index wordurlidx on wordlocation(wordid)")
        self.con.execute("create index urltoidx on link(fromid)")
        self.con.execute("create index urofromidx on link(toid)")

        self.dbcommit()

class searcher:

    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self,q):
        fieldlist = "w0.urlid"
        tablelist = ""
        clauselist = ""
        wordids=[]

        words = q.split(" ")
        tablenum = 0

        for word in words:
            wordrow = self.con.execute("select  rowid from wordlist where word='{0}'".format(word)).fetchone()
            if wordrow!= None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenum>0:
                    tablelist += ","
                    clauselist += " and "
                    clauselist += "w{0:d}.urlid = w{1:d}.urlid and ".format(tablenum-1, tablenum)
                fieldlist+=", w{0:d}.location".format(tablenum)
                tablelist += " wordlocation w{0:d}".format(tablenum)
                clauselist+= "w{0:d}.wordid={1:d}".format(tablenum,wordid)
                tablenum +=1

        #put together
        fullquery = "select {0:s} from {1:s} where {2:s}".format(fieldlist,tablelist,clauselist)
        cur=self.con.execute(fullquery)
        rows = [row for row in cur]
        return rows, wordids

    def getscoredlist(self, rows, wordids):
        totalscores = dict([(row[0],0) for row in rows])

        weights =




        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url]+= weight*scores[url]

        return totalscores

    def frequenctscore(self, rows):
        counts = {row[0]:0 for row in rows}
        for row in rows: counts[row[0]]+=1
        return self.normalizescores(counts)

    def locationscore(self, rows):
        locations = {row[0]: 1000000 for row in rows}
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]:
                locations[row[0]] = loc
        return self.normalizescores(locations, smallBetter=1)

    def distancescore(self,rows):

        #if only 1 word in document return that all document win. I don't now why did it
        if len(rows[0])<=2:
            return {row[0]: 1.0 for row in rows}

        mindistances =  {row[0]: 1000000 for row in rows}

        for row in rows:
            distance = sum([abs(row[i]-row[i-1]) for i in range(2, len(row))])
            if distance < mindistances[row[0]]:
                mindistances[row[0]] = distance
        return self.normalizescores(mindistances, smallBetter=1)

    def geturlname(self, id):
        return self.con.execute("select url from urllist where rowid={0:d}".format(id)).fetchone()[0]

    def query(self,q):
        rows,wordids=self.getmatchrows(q)

        scores = self.getscoredlist(rows,wordids)
        rankedscores=sorted( [(score, url) for (url, score) in scores.items()], reverse=1)

        for (score, urlid) in rankedscores[0:10]:
            print("{0:f}\t{1}\t{2:s}".format(score, urlid, self.geturlname(urlid)))

    def normalizescores(self, scores, smallBetter=0):
        vsmall = 0.0001 # prevent 0 div

        if smallBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore/max(vsmall,l))) for (u,l) in scores.items()])
        else:
            maxscore= max(scores.values())
            if maxscore ==0: maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])
