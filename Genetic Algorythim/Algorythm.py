import Candidate
import Population
import random
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation


ax = plot.axes(projection="3d")
x = []
y = []
z = []
list_of_rows = []
list_of_rows.clear()
list_of_rows.append(["X", "Y", "Z"])


def funciton_z(x, y):
    return 1/((x+3) ** 3 + x*y+y**2)


def Display_function(x_min, y_min, x_max, y_max, dx, dy):

    x = np.linspace(x_min, x_max, (int(abs(x_max-x_min)/dx)))
    y = np.linspace(y_min, y_max, (int(abs(y_max-y_min)/dy)))

    X, Y = np.meshgrid(x, y)
    Z = 1/((X+3) ** 3 + X*Y+Y**2)
    ax.plot_surface(X, Y, Z, alpha=.5)


def BinaryVector(num=[]):
    binary = []
    for i in range(len(num)):
        binary_pom = []
        while(num[i] > 0):
            binary_pom.append(num[i] % 2)
            num[i] = int(num[i] / 2)
        # Dopisac autonomiczne odczytywanie dlugosci
        while(7-len(binary_pom)):
            binary_pom.append(0)
        binary_pom.reverse()
        binary.append(binary_pom)
    return binary


class Talgorythm:
    def __init__(self, candidates_numer, max_population_count):
        self.Present_population = Population.Tpopulation(
            candidates_numer, [], True, 0)
        self.Previous_population = 0
        self.candidates_numer = candidates_numer
        self.max_population_count = max_population_count

    def stop(self):
        if(self.Present_population.get_id_of_population() <= self.max_population_count):
            return True
        else:
            return False

    def run(self):
        list_of_rows.clear()
        list_of_rows.append(["X", "Y", "Z"])
        Display_function(0, 0, 100, 100, 1, 1)
        while(self.stop()):
            self.Present_population.calculate()
            print("Populacja nr:", self.Present_population.get_id_of_population())
            print("Najlepszy osobnik: ")
            for i in range(Candidate.GENS_COUNT):
                print(self.Present_population.get_best_candidate().get_val(i), end=" ")
            print("Score: ", self.Present_population.get_best_candidate().get_score())
            self.Previous_population = self.Present_population
            # Losowanie populacji nastepnej
            # self.Present_population = Population.Tpopulation(
            #    self.candidates_numer, [], True, self.Previous_population.get_id_of_population())
            # Algorytm Genetyczny
            self.Present_population = Population.Tpopulation(
                self.candidates_numer, self.get_new_population(
                    self.Previous_population),
                False, self.Previous_population.get_id_of_population())

    def get_new_population(self, pop=Population.Tpopulation(5, [], True, 0)):
        # Zmienne
        norm = pop.get_norm()
        suma, dlugosc, pot = 0, 0, 0
        lista_par, nowy_genotyp, id_genow, geny, pom = [], [], [], [], []
        # geny.clear()
        # Losowanie Par
        for i in range(self.candidates_numer*2):
            los = random.uniform(0, 100)
            for j in range(self.candidates_numer):
                suma += norm[j]
                if(los <= suma):
                    suma = 0
                    lista_par.append(BinaryVector(pop.get_list_of_id(j)))
                    break
        # Obliczanie dlugosci kombinacji genow
        for i in range(Candidate.GENS_COUNT):
            dlugosc += len(lista_par[0][i])
        # Glowna petla funkcji
        for i in range(0, self.candidates_numer*2, 2):
            licznik = 0
            los = random.randint(0, 100)
            # Krzyzowanie
            if(los <= 75):
                podzial = random.randint(0, dlugosc-1)
                #print("Podzial: ", podzial)
                #print("Rodzic 1: ", lista_par[i])
                #print("Rodzic 2: ", lista_par[i+1])
                for j in range(Candidate.GENS_COUNT):
                    nowy_genotyp.append([])
                    for q in range(len(lista_par[i][j])):
                        if(licznik < podzial):
                            nowy_genotyp[j].append(lista_par[i][j][q])
                            licznik += 1
                        else:
                            nowy_genotyp[j].append(lista_par[i+1][j][q])
                            licznik += 1
            else:
                if(random.randint(0, 1)):
                    nowy_genotyp = lista_par[i]
                else:
                    nowy_genotyp = lista_par[i+1]
            # Mutacja
            for j in range(Candidate.GENS_COUNT):
                for q in range(len(nowy_genotyp[j])):
                    los = random.randint(0, 100)
                    if(los < 5):
                        if(nowy_genotyp[j][q] == 1):
                            nowy_genotyp[j][q] = 0
                        else:
                            nowy_genotyp[j][q] = 1
            #print("Nowy genotyp: ", nowy_genotyp)
            # Zamiana ID na format dziesietny
            for j in range(Candidate.GENS_COUNT):
                id_genow.append(0)
                for q in range(len(nowy_genotyp[j])-1, -1, -1):
                    id_genow[j] += nowy_genotyp[j][q] * pow(2, pot)
                    pot += 1
                pot = 0
            # Wyswietlanie osobnikow wychodzacych
            print("Osobnik nr ", int((i+2)/2), ": ", end="")
            for j in range(Candidate.GENS_COUNT):
                print(id_genow[j], end="")
                if(j != Candidate.GENS_COUNT - 1):
                    print(" ,", end="")
            print("")
            # Wyswietlanie punktu
            max_x = pop.candidates_list[0].genotype[0].get_max_val()
            max_y = pop.candidates_list[0].genotype[1].get_max_val()
            if(id_genow[0] > max_x):
                x = (int(max_x))
            else:
                x = id_genow[0]
            if(id_genow[1] > max_y):
                y = (int(max_y))
            else:
                y = id_genow[1]
            z.append(funciton_z(x, y))
            pom.append(x)
            pom.append(y)
            pom.append(funciton_z(x, y))

            list_of_rows.append(pom.copy())
            pom.clear()
            # Czyszczenie i return
            geny.append(id_genow.copy())

            nowy_genotyp.clear()
            id_genow.clear()
        return geny
