"""
import Gen
import Candidate
import Population
"""
import Algorythm
import Display_Func
import csv

algorytm = Algorythm.Talgorythm(10, 20)
algorytm.run()

# Zapis wynikow do pliku csv
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(Algorythm.list_of_rows)
# Display_Func.main_func()
