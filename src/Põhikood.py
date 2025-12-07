#Programm "Keelutsooni ennustaja". Autorid Tormi Hunt ja Johannes Palmiste.
#Programmi saab käivitada IDE-s "Run" nuppu vajutades

import joblib
import pandas as pd
from tkinter import *
import csv
import subprocess

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
    tulemus = Label(m, text=f'Tulemus: {round(float(prediction), 2)} eV')
    tulemus.grid(row = 7, column = 2, columnspan = 2)
    tulemus.config(bg='lightgreen', font=("Arial", 20))
    return prediction

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

def universaalne_salvestusaken(sulge_m):
    uus = Toplevel(m)
    v1 = IntVar()
    uus.title("Salvestamine")
    uus.geometry("400x300")
    uus.resizable(False, False)
    for c in range(3):
        uus.columnconfigure(c, weight=1)
    Label(uus, text="Sisesta faili nimi laiendiga!", bg="orange", font=("Arial", 20)).grid(row=0, column=1)
    sisend = Entry(uus, font=("Arial", 20))
    sisend.grid(row=1, column=1)
    Button(uus, text="Salvesta", font=("Arial", 20), command=lambda: salvesta_fail(sisend.get(), v1, uus, sulge_m)).grid(row=2, column=1)
    Checkbutton(uus, text="Ava peale salvestamist", variable=v1, onvalue=1, offvalue=0).grid(row=3, column=1)


def salvesta_fail(fail, v1, aken, sulge_m):
    try:
        with open(fail, "w", encoding="UTF-8") as vf:
            vf.write(f"--Ennustatud keelutsooni laius: {round(ennusta(), 2)}--\n")

            for i, sis in enumerate(sisendid):
                vf.write(f"{sildid[i].strip()} -- {sis.get()}\n")
    except:
        with open(fail, "w", encoding="UTF-8") as vf:
            vf.write("Tühjus")
    if sulge_m:
        m.destroy()
    else:
        aken.destroy()
    if v1.get() == 1:
        subprocess.call(fail, shell=True)

def salvestusaken():
    universaalne_salvestusaken(False)

def salvestus_valjumine():
    universaalne_salvestusaken(True)


def autorid():
    uus = Toplevel(m)
    uus.title("Autorid")
    uus.geometry("600x30")
    uus.columnconfigure(0, weight=1)
    uus.columnconfigure(1, weight=1)
    uus.columnconfigure(2, weight=1)
    uus.resizable(False, False)
    tekst = Label(uus, text="Käesoleva programmi autorid on Tormi Hunt ja Johannes Palmiste.")
    tekst.grid(column=1)
    tekst.config(font=("Arial", 15))

#Peaakna loomine

m = Tk()
laius = m.winfo_screenwidth()
korgus = m.winfo_screenheight()
m.title("Keelutsooni ennustaja")
m.resizable(True, True)

#Nupu 'ennusta' loomine

start = Button(m, text='Ennusta', command=ennusta, width=15)
start.grid(row=7, columnspan = 2)
start.config(font=("Arial", 20))
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
menuu.add_cascade(label="Teave", menu=helpmenu)
helpmenu.add_command(label='Autorid', command=autorid)
helpmenu.add_command(label='Kuidas seda kasutada?', command=lambda: subprocess.call("Kasutusjuhend.pdf", shell = True))

exitmenu = Menu(menuu)
menuu.add_cascade(label="Väljumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja välju", command=salvestus_valjumine)
exitmenu.add_command(label='Välju salvestamata', command=m.quit)

sildid = ["Elementide arv (n)", "Ruumala  (Å3/rakk)", "Tihedus (g/cm3)", "Atomaarne tihedus", "Energia aatomi kohta", "Tekkimisenergia \n aatomi kohta \n (eV/aatom)",
          'energy above hull \n (eV/aatom)', 'efermi', 'total magnetization', 'Universaalne \n anisotroopia']

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