import optimization

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

    optimization.geneticoptimize(domain,optimization.schedulecost)
