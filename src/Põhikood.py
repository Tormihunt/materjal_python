#Programm "Keelutsooni ennustaja". Autorid Tormi Hunt ja Johannes Palmiste.
#Programmi saab käivitada IDE-s "Run" nuppu vajutades

import joblib
import pandas as pd
from tkinter import *
import csv

def ennusta():
    try:
        test = list(map(float, sisendid_saama())) #Äkki tuleb mul hiljem parem mõte, kuidas sisendite olemasolu ja kõlblikkust kontrollida
    except:
        vilgutamine(6)
        return
    csv_loomine()
    regressor = joblib.load("band_gap_rf.joblib")
    user_var = pd.read_csv("user_variables.csv")
    standard_deviation = pd.read_csv("standardised_deviation_data.csv").iloc[7, 0]
    mean = pd.read_csv("mean_data.csv").iloc[7, 0]
    prediction = regressor.predict(user_var)
    prediction = prediction * standard_deviation + mean
    prediction = float(prediction[0])
    tulemus = Label(m, text=f'Tulemus: {round(float(prediction), 2)} eV', width=25, height=5)
    tulemus.grid(row = 9, column = 0)
    tulemus.config(bg='lightgreen')

def sisendid_saama():
    return [s.get() for s in sisendid]

def csv_loomine():
    rida = list(map(float, sisendid_saama()))
    tulbad = ['nelements', 'volume', 'density', 'density_atomic', 'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull',
              'efermi', 'total_magnetization', 'universal_anisotropy']
    with open("user_variables.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(tulbad)
        writer.writerow(rida)
    return

def vilgutamine(i):
    if i == 0:
        return
    varv = hoiatus.cget("background")
    uus = "red" if varv == "orange" else "orange"
    hoiatus.configure(background=uus)
    m.after(500, vilgutamine, i-1)

def tuhjenda():
    for s in sisendid:
        s.delete(0, END)

def salvesta(f):
    if f == "":
        return 0
    else:
        with open(f) as vf:
            i = 0
            for sisend in sisendid:
                vf.write(f"{sildid[i]} -- {sisend}")
                i += 1
        return True

def salvestusaken():
    uus = Toplevel(m)
    uus.title("Salvestamine")
    uus.geometry("400x300")
    uus.resizable(False, False)
    nimi = Label(uus, text="Sisesta faili nimi laiendiga!")
    uus.columnconfigure(0, weight=1)
    uus.columnconfigure(1, weight=1)
    uus.columnconfigure(2, weight=1)
    nimi.grid(row=0, column=1)
    nimi.config(font=("Arial", 20))
    sisend = Entry(uus)
    sisend.grid(row=1, column=1)
    sisend.config(font=("Arial", 20))
    salv = Button(uus, text="Salvesta", command= lambda: salvesta(sisend.get()))
    salv.grid(row=2, column=1)
    salv.config(font=("Arial", 20))

#Peaakna loomine

m = Tk()
laius = m.winfo_screenwidth()
korgus = m.winfo_screenheight()
m.title("Keelutsooni ennustaja")
m.resizable(True, True)

#Nupu 'ennusta' loomine

start = Button(m, text='Ennusta', width=25, height=5, command=ennusta)
start.grid(row=6, column=0)
start.config(bg='red')

#Hoiatuse loomine

hoiatus = Label(m, text="Täida kõik väljad numbritega!")
hoiatus.config(bg='orange', font=("Arial", 25))
hoiatus.grid(row = 0, columnspan = 5)

#Menüüd ja funktsioonid peaakna päisesse

menuu = Menu(m)
m.config(menu=menuu)
filemenu = Menu(menuu)
menuu.add_cascade(label="Tühjenda kõik väljad", command=tuhjenda)
menuu.add_command(label="Salvesta", command=salvestusaken)
helpmenu = Menu(menuu)
menuu.add_cascade(label="Abi", menu=helpmenu)
helpmenu.add_command(label='Kuidas see töötab?', command=Toplevel)
helpmenu.add_command(label='Kuidas kasutada', command=Toplevel)

exitmenu = Menu(menuu)
menuu.add_cascade(label="Väljumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja välju", command=m.quit)
exitmenu.add_command(label='Välju salvestamata', command=m.quit)



sildid = ["Elementide arv", "Ruumala", "Tihedus", "Atomaarne tihedus", "Energia aatomi kohta", "Tekkimisenergia \n aatomi kohta",
          'energy above hull', 'efermi', 'total magnetization', 'Universaalne \n anisotroopia']

sisendid = []
rida = 2
veerg = 0

for silt in sildid:
    Label(m, text = silt).grid(row = rida, column = veerg)
    s = Entry(m)
    s.grid(row = rida+1, column = veerg)
    sisendid.append(s)
    veerg = veerg + 1
    if veerg == 5:
        veerg = 0
        rida += 2

m.mainloop()