import csv
import numpy as np
import argparse

x = []
y = []
z = []
list_of_rows = []
list_of_rows.clear()
list_of_rows.append(["X", "Y", "Z"])
pom = []

# 0 - Stożek
# 1 - Ackley function
# 2 - Himmelblau's function
# 3 - Holder’s table


def myParser():
    parser = argparse.ArgumentParser()
    # Obowiązkowe argumenty
    parser.add_argument("Population_size", type=int,
                        help="Number of candidates in one population")
    parser.add_argument(
        "Iteration", type=int, help="Number of generations that are going to be computed")
    parser.add_argument(
        "Function", type=int, help=f"Type of function to optimize:\n\t0 - x\u00b2 + y\u00b2\n\t1 - Ackley function\n\t2 - Himmelblau's function\n\t3 -Hölder table function")
    parser.add_argument(
        "Initial_step", type=float, help="Initial step for new candidates creating")
    parser.add_argument(
        "Parameter_1", type=float, help="Parameter 1 for the step proportion - exploration/exploatation \n\tStep[iter] = Initial_Step * (1/(1+e^(iter-(MaxStep/P1))/P2))")
    parser.add_argument(
        "Parameter_2", type=float, help="Parameter 2 for the step proportion - exploration/exploatation \n\tStep[iter] = Initial_Step * (1/(1+e^(iter-(MaxStep/P1))/P2))")
    parser.add_argument(
        "Best_succession", type=int, help="Number of best candidates that are going to take part in new population generation")

    args = parser.parse_args()
    return args


def Function(x, y, PICK_):
    if(PICK_ == 0):
        return (x**2 + y**2)
    elif(PICK_ == 1):
        return -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.e + 20
    elif(PICK_ == 2):
        return (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    elif(PICK_ == 3):
        return -np.absolute(np.sin(x) * np.cos(y) * np.exp(np.absolute(1 - (np.sqrt(x**2 + y**2)/np.pi))))


def main(pop, MaxStep, PICK, Initial_Step, P1, P2, n):
    np.random.RandomState()
    # Range
    if(PICK == 0 or PICK == 3):
        InitialRangeX = [-10, 10]
        InitialRangeY = [-10, 10]
    elif(PICK == 1 or PICK == 2):
        InitialRangeX = [-5, 5]
        InitialRangeY = [-5, 5]

    # Population Parameters
    n = 10  # N best succession

    list_of_rows.clear()
    list_of_rows.append(["X", "Y", "Z"])
    Step = np.zeros(MaxStep)
    # Solutions Array
    P = np.zeros((pop, 3))
    # Loop
    EndingCondition = 0
    iter = 0

    # Random first population
    for k in range(pop):
        P[k][0] = InitialRangeX[0] + np.random.rand() * \
            (InitialRangeX[1]-InitialRangeX[0])
        P[k][1] = InitialRangeY[0] + np.random.rand() * \
            (InitialRangeY[1]-InitialRangeY[0])

    while(EndingCondition == 0):
        Step[iter] = Initial_Step * (1/(1+np.e**(iter-(MaxStep/P1))/P2))

        for k in range(pop):
            P[k][2] = Function(P[k][0], P[k][1], PICK)
            pom.append(P[k][0])
            pom.append(P[k][1])
            pom.append(P[k][2])
            list_of_rows.append(pom.copy())
            pom.clear()
        P_sorted = P[P[:, 2].argsort()]
        P[0] = P_sorted[0]
        for k in range(1, pop):
            index_1 = np.random.randint(0, n)
            index_2 = np.random.randint(0, n)
            P[k][0] = P_sorted[index_1, 0] + \
                Step[iter] * np.random.uniform(-1, 1)
            P[k][1] = P_sorted[index_2, 1] + \
                Step[iter] * np.random.uniform(-1, 1)
            if(P[k][0] < InitialRangeX[0]):
                P[k][0] = InitialRangeX[0]
            else:
                if(P[k][0] > InitialRangeX[1]):
                    P[k][0] = InitialRangeX[1]
            if(P[k][1] < InitialRangeY[0]):
                P[k][1] = InitialRangeY[0]
            else:
                if(P[k][1] > InitialRangeY[1]):
                    P[k][1] = InitialRangeY[1]
        Best = P_sorted[0, :]
        iter += 1
        if(iter == MaxStep):
            EndingCondition = 1
    print(Best)

    with open('test.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(list_of_rows)
    return Best


if __name__ == '__main__':
    myArgs = myParser()
    main(myArgs.Population_size, myArgs.Iteration, myArgs.Function,
         myArgs.Initial_step, myArgs.Parameter_1, myArgs.Parameter_2, myArgs.Best_succession)
