import math
import tkinter as tk
from tkinter import ttk
from bottom_manager import BottomManager
from bottom_types import BottomTypes
from user_data import UserData


def calculate():
    textarea.delete(1.0, tk.END)

    btype = cbType.get()

    udata = UserData(
        float(cbDiameter.get()),
        float(ePressure.get()),
        float(eTension.get()),
        float(eAdd.get()),
        float(cbDurK.get())
    )
    if btype == BottomTypes.FLAT:
        K = float(cbKF.get())
        if K is None:
            err()
        udata.K = K
    elif btype == BottomTypes.SPHERICAL:
        K = float(cbKS.get())
        if K is None:
            err()
        udata.K = K
    elif btype == BottomTypes.CONICAL:
        a = to_rad(float(cbAlphC.get()))
        if a is None:
            err()
        udata.alpha = a

    btm = BottomManager.get(btype)
    s = btm.get_params(udata)

    result_text = f"Рассчитанная толщина крышки: {s} мм"
    textarea.insert(tk.END, result_text)


types = BottomTypes.list()
dur_koefs = [1, 0.9, 0.8, 0.65]

root = tk.Tk()
root.geometry("800x600")

lbType = ttk.Label(root, text="Тип крышки: ")
lbType.place(x=25, y=25)
cbType = ttk.Combobox(root, values=types, state="readonly")
cbType.place(x=140, y=25, width=250, height=20)

lbDiameter = ttk.Label(root, text="Диаметр, мм: ")
lbDiameter.place(x=25, y=65)
cbDiameter = ttk.Combobox(root, values=None, state="readonly")
cbDiameter.place(x=140, y=65, width=250, height=20)

lbPressure = ttk.Label(root, text="Давление, МПа: ")
lbPressure.place(x=25, y=105)
ePressure = ttk.Entry(root)
ePressure.place(x=140, y=105, width=250, height=20)

lbTension = ttk.Label(root, text="Напряжение, МПа: ")
lbTension.place(x=25, y=145)
eTension = ttk.Entry(root)
eTension.place(x=140, y=145, width=250, height=20)

lbDurK = ttk.Label(root, text="Коэфф. прочности: ")
lbDurK.place(x=25, y=185)
cbDurK = ttk.Combobox(root, values=dur_koefs, state="readonly")
cbDurK.place(x=140, y=185, width=250, height=20)

lbAdd = ttk.Label(root, text="Прибавка, мм: ")
lbAdd.place(x=25, y=225)
eAdd = ttk.Entry(root)
eAdd.place(x=140, y=225, width=250, height=20)

# specific data

# flat
lbKF = ttk.Label(root, text="Коэфф. чертежа: ")
lbKF.place(x=415, y=25)
lbKF.place_forget()
cbKF = ttk.Combobox(root, values=None, state="readonly")
cbKF.place(x=530, y=25, width=250, height=20)
cbKF.place_forget()

# spherical
lbKS = ttk.Label(root, text="Коэфф. чертежа: ")
lbKS.place(x=415, y=25,)
lbKS.place_forget()
cbKS = ttk.Combobox(root, values=None, state="readonly")
cbKS.place(x=530, y=25, width=250, height=20)
cbKS.place_forget()

# conical
lbAlphC = ttk.Label(root, text="Угол наклона: ")
lbAlphC.place(x=415, y=25,)
lbAlphC.place_forget()
cbAlphC = ttk.Combobox(root, values=None, state="readonly")
cbAlphC.place(x=530, y=25, width=250, height=20)
cbAlphC.place_forget()


lbTA = ttk.Label(root, text="Окно вывода:")
lbTA.place(x=25, y=350)

textarea = tk.Text(root)
textarea.place(x=25, y=375, width=650, height=200)

btnCalculate = ttk.Button(root, text="Рассчитать", command=calculate)
btnCalculate.place(x=695, y=375, width=80, height=25)

btnExit = ttk.Button(root, text="Выход", command=exit)
btnExit.place(x=695, y=550, width=80, height=25)


def display_additive(event):
    lbKF.place_forget()
    cbKF.place_forget()
    lbKS.place_forget()
    cbKS.place_forget()
    lbAlphC.place_forget()
    cbAlphC.place_forget()

    btype = cbType.get()
    btm = BottomManager.get(btype)
    bdata = btm.get_data()

    cbDiameter.configure(values=bdata[0])

    if btype == BottomTypes.FLAT:
        lbKF.place(x=415, y=25)
        cbKF.place(x=530, y=25, width=250, height=20)
        cbKF.configure(values=bdata[1])
    elif btype == BottomTypes.SPHERICAL:
        lbKS.place(x=415, y=25)
        cbKS.place(x=530, y=25, width=250, height=20)
        cbKS.configure(values=bdata[1])
    elif btype == BottomTypes.CONICAL:
        lbAlphC.place(x=415, y=25)
        cbAlphC.place(x=530, y=25, width=250, height=20)
        cbAlphC.configure(values=bdata[1])


cbType.bind('<<ComboboxSelected>>', display_additive)


def err():
    pass


def to_rad(angle):
    return angle*math.pi/180


root.mainloop()
