import advancedclassify

if __name__ == '__main__':
    matchmaker = advancedclassify.loadmatch("matchmaker.csv")
    agesonly = advancedclassify.loadmatch("agesonly.csv", allnum=False)

    advancedclassify.plotagematches(agesonly)