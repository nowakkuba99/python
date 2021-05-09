import Candidate


class Tpopulation:

    def __init__(self, number_of_candidates, candidates_, losowosc, population_id):
        self.cans_count = number_of_candidates
        self.population_id = population_id + 1
        self.candidates_list = []
        self.norm = []
        self.best_val = 0
        if(losowosc == False):
            for i in range(self.cans_count):
                self.candidates_list.append(
                    Candidate.Tcandidate(candidates_[i], False))
        else:
            for i in range(self.cans_count):
                self.candidates_list.append(Candidate.Tcandidate([], True))

    def get_list_of_id(self, number):
        lista_genow = []
        for i in range(Candidate.GENS_COUNT):
            lista_genow.append(self.candidates_list[number].get_id_of_gen(i))
        return lista_genow

    def get_norm(self):
        return self.norm

    def calculate(self):
        suma, best_val = 0, 0
        for i in range(self.cans_count):
            self.candidates_list[i].rate()
            val = self.candidates_list[i].get_score()
            suma += val
        for i in range(self.cans_count):
            self.candidates_list[i].rate()
            val = self.candidates_list[i].get_score()
            self.norm.append(val / suma * 100)
            if(i):
                best_val = max(best_val, val)
            else:
                best_val = val
            self.best_val = best_val

    def get_best_candidate(self):
        i = 0
        while(self.candidates_list[i].get_score() != self.best_val):
            i += 1
        return self.candidates_list[i]

    def get_id_of_population(self):
        return self.population_id
