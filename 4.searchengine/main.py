import urllib.request
import searchengine
import nn

if __name__ == '__main__':
    print('PyCharm')

    crawler = searchengine.crawler("searchengine.db")

    #crawler.calculatepagerank()

    searcher = searchengine.searcher("searchengine.db")

    searcher.query("программирование python")

    """
    t,v = searcher.getmatchrows("программирование lua")
    [print(line) for line in t]
    """

    #crawler.crawl(["https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5"], depth=2)
    """
    
    t = crawler.con.execute("select urlid from wordlocation where wordid = 1 ")
    for i in t:
        print(str(i))
        
   
    "select wl.word from wordlist wl where wl.rowid in (select wloc.wordid form wordlocation wloc where wloc.location in (2226, 2064) ) "
    t = crawler.con.execute("select wl.word from wordlist wl, wordlocation wloc  where wl.rowid == wloc.wordid and wloc.location in (2226, 2064)")
    for i in t:
        print(str(i))
    """

    #crawler.creatindextables()

    """
    c= urllib.request.urlopen("https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5")
    content = c.read()
    print(content[0:50])
    """

    mynet = nn.searchnet("nn.db")
    #mynet.maketables()

    wWorld,wRiver, wBank= 101,102,103
    uWorldBank, uRiver, uEarth = 201,202,203

    mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth])

    for c in mynet.con.execute("select * from wordhidden"): print(c)
    for c in mynet.con.execute("select * from hiddenurl"): print(c)

    for i in mynet.getresult([wWorld, wBank],[uWorldBank,uRiver, uEarth]): print(i)

    #mynet.trainauery([wWorld, wBank],[uWorldBank,uRiver, uEarth], uWorldBank)

    for i in mynet.getresult([wWorld, wBank], [uWorldBank, uRiver, uEarth]): print(i)

    #checkresults
    allurls = [uWorldBank, uRiver, uEarth]
    """ 
    for i in range(30):
        mynet.trainauery([wWorld,wBank],allurls,uWorldBank)
        mynet.trainauery([wRiver, wBank], allurls, uRiver)
        mynet.trainauery([wWorld], allurls, uEarth)
    """

    for i in mynet.getresult([wWorld,wBank], allurls): print(i,end=" ")
    print()
    for i in mynet.getresult([wRiver, wBank], allurls): print(i,end=" ")
    print()
    for i in mynet.getresult([wBank], allurls): print(i,end=" ")
    print()
