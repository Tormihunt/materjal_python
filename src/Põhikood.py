#Programm "Keelutsooni ennustaja". Autorid Tormi Hunt ja Johannes Palmiste.
#Programmi saab käivitada IDE-s "Run" nuppu vajutades. Programmi kasutusjuhend asub failis "Kasutusjuhend.txt",
#millele pääseb ligi nii programmi kui ka vastava kausta kaudu. Vajalikud paketid on toodud failis "requirements.txt".

import joblib
import pandas as pd
from tkinter import *
import csv
import subprocess

#Keelutsooni ennustamine ja väljastamine peaknale

def ennusta():
    try:
        list(map(float, sisendid_saama()))
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
    tulemus.grid(row = 8, column = 2, columnspan = 2)
    tulemus.config(bg='lightgreen', font=("Arial", 20))
    return prediction

#Sisendite saamine väljadelt

def sisendid_saama():
    return [s.get() for s in sisendid]

#CSV faili loomine ennustuse tegemiseks

def csv_loomine():
    rida = list(map(float, sisendid_saama()))
    tulbad = ['nelements', 'volume', 'density', 'density_atomic', 'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull',
              'efermi', 'total_magnetization', 'universal_anisotropy']
    with open("user_variables.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(tulbad)
        writer.writerow(rida)
    return

#Hoiatuse vilgutamine, kui sisendid pole korrektsed

def vilgutamine(i):
    if i == 0:
        return
    varv = hoiatus.cget("background")
    uus = "red" if varv == "orange" else "orange"
    hoiatus.configure(background=uus)
    m.after(500, vilgutamine, i-1)

#Kõikide väljade väärtuste lähtestamine

def lahtesta():
    for i, var in enumerate(muutujad):
        var.set(sildid[list(sildid.keys())[i]][0])

#Salvestusakna loomine

def salvestusaken(v):
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
    Button(uus, text="Salvesta", font=("Arial", 20), command=lambda: salvesta_fail(sisend.get(), v1, uus, v)).grid(row=2, column=1)
    Checkbutton(uus, text="Ava peale salvestamist", variable=v1, onvalue=1, offvalue=0).grid(row=3, column=1)

#Sisendite ja tulemuse salvestamine tekstifaili. Funktsioon kirjutab teksitfaili sõna "Tühjus", kui sisendid pole korrektsed

def salvesta_fail(fail, v1, aken, v):
    try:
        with open(fail, "w", encoding="UTF-8") as vf:
            vf.write(f"--Ennustatud keelutsooni laius: {round(ennusta(), 2)}--\n\n")

            for i, sis in enumerate(sisendid):
                v = list(sildid.keys())[i].split()
                vf.write(f"{' '.join(v)} -- {sis.get()}\n\n")
    except:
        with open(fail, "w", encoding="UTF-8") as vf:
            vf.write("Tühjus")
    if v:
        m.destroy()
    else:
        aken.destroy()
    if v1.get() == 1:
        subprocess.call(fail, shell=True)

#Kõrvalaken autorite nimedega

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
m.resizable(False, False)

#Nupu 'ennusta' loomine

start = Button(m, text='Ennusta', command=ennusta, width=15)
start.grid(row=8, columnspan = 2)
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
menuu.add_cascade(label="Lähtesta kõik väljad", command=lahtesta)
menuu.add_command(label="Salvesta", command=lambda: salvestusaken(False))
helpmenu = Menu(menuu)
menuu.add_cascade(label="Teave", menu=helpmenu)
helpmenu.add_command(label='Autorid', command=autorid)
helpmenu.add_command(label='Kuidas seda kasutada?', command=lambda: subprocess.call("Kasutusjuhend.pdf", shell = True))

exitmenu = Menu(menuu)
menuu.add_cascade(label="Väljumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja välju", command=lambda: salvestusaken(True))
exitmenu.add_command(label='Välju salvestamata', command=m.quit)

#Sisendiväljad peaaknasse

sisendid = []
muutujad = []
rida = 2
veerg = 0

sildid = {"Elementide arv (n)": (1, 6), "Ruumala  (Å3/rakk)": (1, 1400) , "Tihedus (g/cm3)": (0.5, 20), "Atomaarne tihedus": (1, 120), "Energia aatomi kohta \n (eV/aatom)": (-80, 0), "Tekkimisenergia \n aatomi kohta \n (eV/aatom)": (-1, 1) ,
          'energy above hull \n (eV/aatom)': (0, 15), 'Fermi energia (eV)': (-10, 15), 'Täielik magneetumus ()': (0, 60), 'Universaalne \n anisotroopia': (-100, 100)}

sammud = {"Elementide arv (n)": 1, "Ruumala  (Å3/rakk)": 10, "Tihedus (g/cm3)": 0.01, "Atomaarne tihedus": 1, "Energia aatomi kohta (eV/aatom)": 1, "Tekkimisenergia \n aatomi kohta \n (eV/aatom)": 0.01, "energy above hull \n (eV/aatom)": 0.1, "Fermi energia (eV)": 0.1, "total magnetization": 1, "Universaalne \n anisotroopia": 1}

for silt in sildid:
    if isinstance(sammud[silt], float):
        var = DoubleVar(value=sildid[silt][0])
    else:
        var = IntVar(value=sildid[silt][0])
    muutujad.append(var)
    Label(m, text=silt).grid(row=rida, column=veerg)
    Scale(m, from_=sildid[silt][0], to=sildid[silt][1], resolution= sammud[silt], showvalue= 0, orient=HORIZONTAL, variable=var, tickinterval=0).grid(row=rida+1, column=veerg)
    s = Entry(m, textvariable=var)
    s.grid(row=rida+2, column=veerg)
    sisendid.append(s)
    veerg += 1
    if veerg == 5:
        veerg = 0
        rida += 3

m.mainloop()