#Programm "Keelutsooni ennustaja". Autorid Tormi Hunt ja Johannes Palmiste.
#Programmi saab käivitada IDE-s "Run" nuppu vajutades

import joblib
import pandas as pd
from tkinter import *
import csv

def ennusta():
    try:
        a = list(map(float, sisendid_saama())) #Äkki tuleb mul hiljem parem mõte, kuidas sisendite olemasolu ja kõlblikkust kontrollida
    except:
        hoiatus = Label(m, text="Täida kõik väljad numbritega!")
        hoiatus.config(bg='red')
        hoiatus.grid(row=9, column=0)
        return
    csv_loomine()
    regressor = joblib.load("band_gap_rf.joblib")
    user_var = pd.read_csv("user_variables.csv")
    standard_deviation = pd.read_csv("standardised_deviation_data.csv").iloc[7, 0]
    mean = pd.read_csv("mean_data.csv").iloc[7, 0]
    prediction = regressor.predict(user_var)
    prediction = prediction * standard_deviation + mean
    tulemus = Label(m, text=f'Tulemus: {round(float(prediction), 2)} eV', width=25, height=5)
    tulemus.grid(row = 9, column = 0)
    tulemus.config(bg='lightgreen')

def sisendid_saama():
    sisendid = [e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get()]
    return sisendid

def csv_loomine():
    rida = list(map(int, sisendid_saama()))
    tulbad = ['nelements', 'volume', 'density', 'density_atomic', 'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull',
              'efermi', 'total_magnetization', 'universal_anisotropy']
    with open("user_variables.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(tulbad)
        writer.writerow(rida)
    return

#Peaakna loomine

m = Tk()
laius = m.winfo_screenwidth()
korgus = m.winfo_screenheight()
m.geometry("%dx%d" % (laius, korgus))
m.title("Keelutsooni ennustaja")

#Nupu 'ennusta' loomine

start = Button(m, text='Ennusta', width=25, height=5, command=ennusta)
start.grid(row=6, column=0)
start.config(bg='red')

#Menüüd peaakna päisesse

menuu = Menu(m)
m.config(menu=menuu)
filemenu = Menu(menuu)
menuu.add_cascade(label="Salvesta", menu=filemenu)
helpmenu = Menu(menuu)
menuu.add_cascade(label="Abi", menu=helpmenu)
helpmenu.add_command(label='Kuidas see töötab?', command=Toplevel)
helpmenu.add_command(label='Kuidas kasutada', command=Toplevel)

exitmenu = Menu(menuu)
menuu.add_cascade(label="Väljumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja välju", command=m.quit)
exitmenu.add_command(label='Välju salvestamata', command=m.quit)

#Hiljem viin järgnevad plokid tsüklisse

Label(m, text='nelements').grid(row=0, column=0, columnspan=2, rowspan=2)
Label(m, text='volume').grid(row=0, column=3, columnspan=2, rowspan=2)
Label(m, text='density').grid(row=0, column=6, columnspan=2, rowspan=2)
Label(m, text='density atomic').grid(row=0, column=9, columnspan=2, rowspan=2)
Label(m, text='energy per atom').grid(row=0, column=12, columnspan=2, rowspan=2)
Label(m, text='formation energy per atom').grid(row=3, column=0, columnspan=3, rowspan=2)
Label(m, text='energy above hull').grid(row=3, column=3, columnspan=2, rowspan=2)
Label(m, text='efermi').grid(row=3, column=5, columnspan=2, rowspan=2)
Label(m, text='total magnetization').grid(row=3, column=7, columnspan=4, rowspan=2)
Label(m, text='universal anisotropy').grid(row=3, column=11, columnspan=4, rowspan=2)

e1 = Entry(m)
e2 = Entry(m)
e3 = Entry(m)
e4 = Entry(m)
e5 = Entry(m)
e6 = Entry(m)
e7 = Entry(m)
e8 = Entry(m)
e9 = Entry(m)
e10 = Entry(m)

e1.grid(row=2, column=0)
e2.grid(row=2,column=3)
e3.grid(row=2, column=6)
e4.grid(row=2, column=9)
e5.grid(row=2, column=12)
e6.grid(row=5,column=0)
e7.grid(row=5,column=3)
e8.grid(row=5,column=6)
e9.grid(row=5,column=9)
e10.grid(row=5,column=12)

m.mainloop()