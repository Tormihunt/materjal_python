from tkinter import *

m = Tk()
laius = m.winfo_screenwidth()
korgus = m.winfo_screenheight()
m.geometry("%dx%d" % (laius, korgus))
m.title("Projekt")
#top = Toplevel()
#top.title("Kuidas kasutada")
#top.mainloop()
menuu = Menu(m)
m.config(menu=menuu)
filemenu = Menu(menuu)
menuu.add_cascade(label="Salvesta", menu=filemenu)
helpmenu = Menu(menuu)
menuu.add_cascade(label="Kuidas kasutada?", menu=helpmenu)
exitmenu = Menu(menuu)
menuu.add_cascade(label="Valjumine", menu=exitmenu)
exitmenu.add_command(label="Salvesta ja valju", command = m.quit)
exitmenu.add_command(label='Valju salvestamata', command = m.quit)



m.mainloop()