import joblib
import pandas as pd
from tkinter import *
from csv import *

#vajab veel tegemist

def ennusta():
    regressor = joblib.load("./data/band_gap_rf.joblib")
    user_var = pd.read_csv("user_variables.csv")
    standard_deviation = pd.read_csv("./data/standardised_deviation_data.csv").iloc[7, 0]
    mean = pd.read_csv("./data/mean_data.csv").iloc[7, 0]
    prediction = regressor.predict(user_var)
    prediction = prediction * standard_deviation + mean
    tulemus = Label(m, text=f'Tulemus: {prediction:.2f} ev')
    tulemus.grid(row=7, column=6)

m = Tk()
laius = m.winfo_screenwidth()
korgus = m.winfo_screenheight()
m.geometry("%dx%d" % (laius, korgus))
m.title("Projekt")

menuu = Menu(m)
m.config(menu=menuu)
filemenu = Menu(menuu)
menuu.add_cascade(label="Salvesta", menu=filemenu)
helpmenu = Menu(menuu)
menuu.add_cascade(label="Abi", menu=helpmenu)
helpmenu.add_command(label='Kuidas see tootab?', command=Toplevel)
helpmenu.add_command(label='Kuidas kasutada', command=Toplevel)

exitmenu = Menu(menuu)
menuu.add_cascade(label="Valjumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja valju", command=m.quit)
exitmenu.add_command(label='Valju salvestamata', command=m.quit)

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


sisendid = []
for i in range(1, 11):
    sisend = Entry(m)
    if i <= 5:
        sisend.grid(row=2, column=(i - 1) * 3)
    else:
        sisend.grid(row=5, column=(i - 6) * 3)
    sisendid.append(sisend.get())


with open("user_variables.csv", "w") as csvfile:
    writer = writer(csvfile)
    writer.writerow(sisendid)

start = Button(m, text='Ennusta', width=25, height=5, command=ennusta)
start.grid(row=6, column=0)
start.config(bg='red')

m.mainloop()