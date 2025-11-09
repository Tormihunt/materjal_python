from tkinter import *

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

def Kuidas_kasutada():
    top = Toplevel()
    top.geometry("%dx%d" % (laius, korgus))
    top.title("Kuidas kasutada?")
    top.mainloop()
def Kuidas_tootab():
    top = Toplevel()
    top.geometry("%dx%d" % (laius, korgus))
    top.title("Kuidas tootab?")
    top.mainloop()

exitmenu = Menu(menuu)
menuu.add_cascade(label="Valjumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja valju", command = m.quit)
exitmenu.add_command(label='Valju salvestamata', command = m.quit)

Label(m, text='nelements').grid(row=0, column=0)
Label(m, text='volume').grid(row=0, column=1)
Label(m, text='density').grid(row=0, column=2)
Label(m, text='density atomic').grid(row=0, column=3)
Label(m, text='energy per atom').grid(row=0, column=4)
Label(m, text='formation energy per atom').grid(row=0, column=5)
Label(m, text='energy above hull').grid(row=0, column=6)
Label(m, text='efermi').grid(row=0, column=7)
Label(m, text='total magnetization').grid(row=0, column=8)
Label(m, text='universal anisotropy').grid(row=0, column=9)

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

e1.grid(row=1, column=0)
e2.grid(row=1, column=1)
e3.grid(row=1, column=2)
e4.grid(row=1, column=3)
e5.grid(row=1, column=4)
e6.grid(row=1, column=5)
e7.grid(row=1, column=6)
e8.grid(row=1, column=7)
e9.grid(row=1, column=8)
e10.grid(row=1, column=9)

def valjund():
    if e1 == '0':
        sonum = 'Valjad on taitmata'
        messageVar = Message(m, text=sonum)
        messageVar.config(bg = 'red')
        messageVar.grid(row=4, column=1)
    else:

        Valjund = f'Keelutsooni laius on 12.1 eV'
        messageVar = Message(m, text=Valjund)
        messageVar.config(bg='lightgreen')
        messageVar.place(x=100, y=100)

start = Button(m, text='Ennusta', width=25, command=valjund)
start.grid(row=2, column=0)
start.config(bg='red')
m.mainloop()