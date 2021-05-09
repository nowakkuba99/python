import Gen
GENS_COUNT = 2


class Tcandidate:
    def __init__(self, lista_genow, losowosc):
        self.score = 0
        self.genotype = []
        self.genotype.append(Gen.Tgen("X", 0, 100, 1, 0, True))
        self.genotype.append(Gen.Tgen("Y", 0, 100, 1, 0, True))
        if(losowosc == True):
            for i in range(GENS_COUNT):
                self.genotype[i].set_rand_val()
        else:
            for i in range(GENS_COUNT):
                self.genotype[i].set_id(lista_genow[i])

    def get_id_of_gen(self, number):
        return self.genotype[number].get_id()

    def get_val(self, number):
        return self.genotype[number].get_val()

    def rate(self):
        x = self.genotype[0].get_val()
        y = self.genotype[1].get_val()
        self.score = pow((x+3), 3) + x * y+pow(y, 2)  # (x+3)^3 + x*y+y^2
        if(self.score):
            self.score = 1 / self.score

    def get_score(self):
        return self.score
