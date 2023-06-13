from math import sqrt

#Dictionary with movies ratings
critics = {
    "Lisa Rose": {"Lady in the Water": 2.5, "Snakes on a Plane": 3.5, "Just My Luck":3.0, "Superman Returns":3.5, "You,My and Dupree":2.5,"The Night Listener":3.0},
    "Gene Seymour":{"Lady in the Water": 3.0, "Snakes on a Plane": 3.5, "Just My Luck":1.5, "Superman Returns":5.0, "You,My and Dupree":3.5,"The Night Listener":3.0},
    "Michael Phillips":{"Lady in the Water": 2.5, "Snakes on a Plane": 3.0, "Superman Returns":3.5,"The Night Listener":4.0},
    "Claudia Puig":{"Snakes on a Plane": 3.5, "Just My Luck":3.0, "Superman Returns":4.0, "You,My and Dupree":2.5,"The Night Listener":4.5},
    "Mick LaSalle":{"Lady in the Water": 3.0, "Snakes on a Plane": 4.0, "Just My Luck":2.0, "Superman Returns":3.0, "You,My and Dupree":2.0,"The Night Listener":3.0},
    "Jack Matthews":{"Lady in the Water": 3.0, "Snakes on a Plane": 4.0, "Superman Returns":5.0, "You,My and Dupree":3.5,"The Night Listener":3.0},
    "Toby":{"Snakes on a Plane": 4.5, "Superman Returns":4.0, "You,My and Dupree":1.0}}

def sim_distance_temp():
   return 1/(1+sqrt(pow(5-4,2)+pow(4-1,2)))
def sim_distance(prefs, person1, person2):
    #find items, which was graded both
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    #if there is no any common grade return 0
    if len(si)==0: return 0

    #find distanse
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in si])
    return 1/(1+sum_of_squares)

def sim_person(prefs, p1, p2):
    # find items, which was graded both
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)
    if n==0: return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    #sum of squared number
    sum1Sq= sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    #person coeficient
    num = pSum-(sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    return num/den

def topMatches(prefs, person, n=5, similatiry = sim_person):
    scores =[(similatiry(prefs, person, other ), other) for other in prefs if other!= person]

    scores.sort()
    scores.reverse()
    return scores[0:n]

def getReccomendations(prefs, person, similarity=sim_person):
    totals={}
    simSums={}

    for other in prefs:
        if other==person: continue
        sim = similarity(prefs,person,other)

        if sim <= 0: continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                # coeficient*score
                totals[item]+=prefs[other][item]*sim
                # sum coeficients
                simSums.setdefault(item,0)
                simSums[item]+=sim

    rankings= [(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

# переварачиваем данные
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            result[item][person]=prefs[person][item]
    return result

def calculateSimiliarItems(prefs, n=10):
    # создать словарь похожих образцов
    result = {}

    itemPrefs=transformPrefs(prefs)
    for item in itemPrefs:
        scores = topMatches(itemPrefs, item, n=n, similatiry=sim_distance)
        result[item] = scores
    return result

def getRecomendationItems(prefs, itemMatch, user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    for (item, raiting) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            if item2 in userRatings: continue
            scores.setdefault(item2,0)
            scores[item2]+=similarity*raiting

            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    rankings = [(score/totalSim[item],item) for (item,score) in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings







