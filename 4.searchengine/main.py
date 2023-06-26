import urllib.request
import searchengine


if __name__ == '__main__':
    print('PyCharm')

    crawler = searchengine.crawler("searchengine.db")

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
    crawler = searchengine.crawler("")
        crawler.crawl(["https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5"])
    """

    """
    c= urllib.request.urlopen("https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5")
    content = c.read()
    print(content[0:50])
    """

