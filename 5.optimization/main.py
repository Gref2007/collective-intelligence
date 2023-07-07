import optimization
import dorm
import socialnetwork

if __name__ == '__main__':

    domain = [(0,8)]*(len(optimization.people)*2)
    """

    s = optimization.randomoptimize(domain, optimization.schedulecost)
    print(optimization.schedulecost(s))
    optimization.printschedule(s)

    s = optimization.hillclimb(domain, optimization.schedulecost)
    print(optimization.schedulecost(s))
    optimization.printschedule(s)

    s = optimization.annealingoptimize(domain, optimization.schedulecost)
    print(optimization.schedulecost(s))
    optimization.printschedule(s)
    """

    #optimization.geneticoptimize(domain,optimization.schedulecost)

    """
    s= optimization.randomoptimize(dorm.domain, dorm.dormcost)
    print(dorm.dormcost(s))
    s= optimization.geneticoptimize(dorm.domain, dorm.dormcost)
    print(dorm.dormcost(s))
    """


    s = optimization.randomoptimize(socialnetwork.domain,socialnetwork.crosscount)
    print(socialnetwork.crosscount(s))

    #s = optimization.annealingoptimize(socialnetwork.domain, socialnetwork.crosscount, step=50)
    socialnetwork.drawnetwork(s)
