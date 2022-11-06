#!/usr/bin/env python3


# Task 1    
def Travellers(List):
    from constraint import Problem, AllDifferentConstraint
    problem = Problem()

    people = ["claude", "olga", "pablo", "scott"]
    times = ["2:30", "3:30", "4:30", "5:30"]
    destinations = ["peru", "romania", "taiwan", "yemen"]

    t_variables = list(map(lambda x: "t_" + x, people))
    d_variables = list(map(lambda x: "d_" + x, people))

    problem.addVariables(t_variables, times)
    problem.addVariables(d_variables, destinations)

    problem.addConstraint(AllDifferentConstraint(), t_variables)
    problem.addConstraint(AllDifferentConstraint(), d_variables)

    # Olga is leaving 2 hours before the traveller from Yemen .
    for person in people:
        problem.addConstraint(
            (lambda x, y, z: (y != "yemen") or
                             ((x == "4:30") and (z == "2:30")) or
                             ((x == "5:30") and (z == "3:30"))),
            ["t_" + person, "d_" + person, "t_olga"])

    # Claude is either the person leaving at 2:30 pm or the traveller leaving at 3:30 pm.
    for person in people:
        problem.addConstraint((lambda x: (x == "2:30" or x == "3:30")), ["t_claude"])

    # The person leaving at 2:30 pm is flying from Peru
    for person in people:
        problem.addConstraint(
            (lambda x, y: (x == "2:30" or y != "peru")), ["t_" + person, "d_" + person]
        )

    # The person flying from Yemen is leaving earlier than the person flying from Taiwan
    for person1 in people:
        for person2 in people:
            if person1 == person2:
                continue
            problem.addConstraint((lambda x, y, z, w: ((x == "4:30" or y != "yemen") and (z == "5:30" or w != "taiwan")) or (x == "3:30" or y != "yemen") and ((z == "5:30" or z == "4:30") or w != "taiwan") or (x == "2:30" or y != "yemen") and ((z == "5:30" or z == "4:30", z == "3:30") or w != "taiwan")), ["t_" + person1, "d_" + person1, "t_" + person2, "d_" + person2])

    # The four travellers are Pablo, the traveller flying from Yemen, the person leaving at 2:30 pm
    # and the person leaving at 3:30 pm.
    for person in people:
        problem.addConstraint(lambda x, y: (y != "yemen") and (x != "2:30" or x != "3:30"), ["t_pablo", "d_pablo"])

    def lambda1(i):
        return lambda x: x == times
    for i in List:
        peoples = i[0]
        times = i[1]
        problem.addConstraint(lambda1(i), ["t_" + peoples])

    return problem.getSolutions()


# Task 2
def CommonSum(n):
    return (n*((n*n) + 1))/2


# Task 3
def msqList(m, pairList):
    from constraint import Problem , AllDifferentConstraint , ExactSumConstraint
    problem = Problem()
    problem.addVariables(range(0, m * m), range(1, m * m + 1))

    problem.addConstraint(AllDifferentConstraint(), range(0, m * m))

    for r in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [r * m + i for i in range(m)])

    for c in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [c + m * i for i in range(m)])

    problem.addConstraint(ExactSumConstraint(CommonSum(m)), [i * m + i for i in range(m)])
    problem.addConstraint(ExactSumConstraint(CommonSum(m)), [i * m + (m - i - 1) for i in range(m)])

    def lambda2(i):
        return lambda x: x == i[1]

    for i in pairList:
        problem.addConstraint(lambda2(i), [i[0]])

    return problem.getSolutions()


# Task 4
def pmsList(m, pairList):
    from constraint import Problem , AllDifferentConstraint , ExactSumConstraint
    problem = Problem()
    problem.addVariables(range(0, m * m), range(1, m * m + 1))

    problem.addConstraint(AllDifferentConstraint(), range(0, m * m))

    for r in range(m):       
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [r * m + i for i in range(m)])

    for c in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [c + m * i for i in range(m)])


    dd = []
    for j in range(m):
        d = []
        for i in range(m):
            if j >= m - i:
                d.append(j + (i * m + i) - m)
            else:
                d.append(j + (i * m + i))
        dd.append(d)

    for j in range(m):
        d = []
        for i in range(m):
            if j >= m - i:
                d.append(i * m + (m - i - 1) - j + m)
            else:
                d.append(i * m + (m - i - 1) - j)
        dd.append(d)

    for i in dd:
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), i)

    def lambda2(i):
        return lambda x: x == i[1]

    for i in pairList:
        problem.addConstraint(lambda2(i), [i[0]])

    return problem.getSolutions()


# Debug
if __name__ == '__main__':
    print("debug run...")
    print(Travellers([["olga", "2:30"]]))
    print((CommonSum(4)))
    print(msqList(4,[[0,13],[1,12],[2,7]]))
    print(pmsList(4,[[0,13],[1,12],[2,7]]))

