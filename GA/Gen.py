import random
# Klasa Tgen


class Tgen:
    """Klasa Gen ma parametry: nazwa, min, max, dx, wartosc, losowosc
       Dostepne metody to : get_val() - zwraca wartosc genu
                            get_id() - zwraca id genu
                            set_val(val) - ustawia wartosc genu
                            set_id(idd) - ustawia id_genu
                            set_rand_val() - ustawia losowa wartosc genu
    """
    # Konstruktor

    def __init__(self, name, x_min, x_max, dx, val, rand):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
        self.dx = dx
        self.id = 0
        if(rand == True):
            self.set_rand_val()
        else:
            self.set_val(val)
    # Zwracanie wartosci genu

    def get_val(self):
        return self.x_min + self.id * self.dx
    # Zwracanie id genu

    def get_id(self):
        return self.id
    # Ustawianie zadanej wartosci

    def set_val(self, val):
        if(val < self.x_min):
            self.id = 0
        elif(val > self.x_max):
            self.id = (self.x_max - self.x_min)
        else:
            id_pom = 0
            while(abs(self.x_min + id_pom*self.dx - val) > self.dx/2):
                id_pom = id_pom+1
            self.id = id_pom
        print('value set corectlly')
    # Ustawianie zadanego id

    def set_id(self, idd):
        if((self.x_min + idd * self.dx) > self.x_max):
            self.id = (self.x_max - self.x_min)/self.dx
        else:
            self.id = idd
    # Losowanie wartosci genu

    def set_rand_val(self):
        id_count = abs(self.x_max - self.x_min) / self.dx + 1
        self.id = random.randint(0, id_count)

    def get_max_val(self):
        return self.x_max
