
import recommendations
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(recommendations.critics["Lisa Rose"]["Lady in the Water"])
    print(recommendations.sim_distance(recommendations.critics,"Mick LaSalle", "Jack Matthews"))
    print(recommendations.sim_person(recommendations.critics, "Mick LaSalle", "Jack Matthews"))

    print(recommendations.topMatches(recommendations.critics,"Toby", 3))
    print(recommendations.getReccomendations(recommendations.critics,"Toby"))


