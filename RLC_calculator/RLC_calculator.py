from Tkinter import *
import tkMessageBox
from math import *
import __future__

WIDTH = 500   # WIDTH = root.winfo_screenwidth()
HEIGHT = 450  # HEIGHT = root.winfo_screenheight()
w = 80
W = 160
H = 25

obj = [["R", "L", "r", "C", "U", "omega"],
       ["Z", "Z_L", "Z_C", "Z_d", "I"],
       ["U_R", "U_L", "U_C", "U_d"],
       ["P", "P_R", "cos_phi", "cos_phi_R"],
       ["phi", "phi_i", "phi_u"]
      ]
row = {}
entry = [{}, {}, {}, {}, {}]


def GetVal(s):
    cnt = row[s]
    return 1.0 * eval(compile(entry[cnt][s].get().replace("e", "E"), '<string>', 'eval', __future__.division.compiler_flag))


def NewVal(s, v):
    cnt = row[s]
    entry[cnt][s].delete(0, len(entry[cnt][s].get()))
    entry[cnt][s].insert(END, v)


def Calc():
    if (entry[row["R"]]["R"].get() == "" or entry[row["L"]]["L"].get() == "" or entry[row["C"]]["C"].get() == ""
        or entry[row["r"]]["r"].get() == "" or entry[row["U"]]["U"].get() == "" or entry[row["omega"]]["omega"].get() == ""):
        tkMessageBox.showinfo("Error", "Please enter value of R, L, r, C, omega and U")
        return None

    R = GetVal("R")
    L = GetVal("L")
    C = GetVal("C")
    r = GetVal("r")
    U = GetVal("U")
    omega = GetVal("omega")

    _R = R + r
    Z_L = omega * L
    Z_C = 1.0 / (omega * C)
    Z_d = sqrt(Z_L * Z_L + r * r)
    Z = sqrt((_R ** 2) + ((Z_L - Z_C) ** 2))
    I = U / Z
    U_R = R * I
    U_L = Z_L * I
    U_C = Z_C * I
    U_d = Z_d * I
    P = ((U ** 2) / ((_R ** 2) + ((Z_L - Z_C) ** 2))) * _R
    P_R = ((U ** 2) / ((_R ** 2) + ((Z_L - Z_C) ** 2))) * R
    cos_phi = _R / Z
    cos_phi_R = R / Z
    phi = acos(cos_phi)  # phi = phi_u - phi_i

    NewVal("Z", Z)
    NewVal("Z_L", Z_L)
    NewVal("Z_C", Z_C)
    NewVal("Z_d", Z_d)
    NewVal("I", I)

    NewVal("U_R", U_R)
    NewVal("U_L", U_L)
    NewVal("U_C", U_C)
    NewVal("U_d", U_d)

    NewVal("P", P)
    NewVal("P_R", P_R)
    NewVal("cos_phi", cos_phi)
    NewVal("cos_phi_R", cos_phi_R)

    NewVal("phi", phi)

    if (entry[row["phi_u"]]["phi_u"].get() != ""):
        phi_u = GetVal("phi_u")
        phi_i = phi_u - phi
        NewVal("phi_i", phi_i)

    elif (entry[row["phi_i"]]["phi_i"].get() != ""):
        phi_i = GetVal("phi_i")
        phi_u = phi_i + phi
        NewVal("phi_u", phi_u)


def Clear():
    for cnt in range(len(obj)):
        for element in obj[cnt]:
            entry[cnt][element].delete(0, len(entry[cnt][element].get()))


#-------------------------------------------------------------------
root = Tk()
root.wm_title("RLC Calculator")
root.resizable(0, 0)  # disable maximize window size

frame = Frame(root, height=HEIGHT, width=WIDTH)
frame.pack()
#------------------------------------------------------------------
# Init
F = (len(obj[0]) + 1) * H
H_frame = 6 * H

for cnt in range(len(obj)):
    if (cnt > 0):
        for i in range(len(obj[cnt])):
            element = obj[cnt][i]
            row[element] = cnt

            LAB1 = Label(root, text=element + " = ", justify=LEFT)
            LAB1.pack(side=LEFT)
            LAB1.place(x = 0+(cnt-1)%2 * (w+W), y = F + i * H, height=H, width=w)

            entry[cnt][element] = Entry(root)
            entry[cnt][element].pack(side=RIGHT)
            entry[cnt][element].place(x = w+(cnt-1)%2 * (w+W), y = F + i * H, height=H, width=W)

        if (cnt % 2 == 0):
            F += H_frame
    else:
        for i in range(len(obj[cnt])):
            element = obj[cnt][i]
            row[element] = cnt

            LAB1 = Label(root, text = element + " = ", justify = LEFT)
            LAB1.pack(side = LEFT)
            LAB1.place(x = 0, y = i * H, height = H, width = w)

            entry[cnt][element] = Entry(root)
            entry[cnt][element].pack(side = RIGHT)
            entry[cnt][element].place(x = w, y = i * H, height = H, width = W)

X = 55 + WIDTH // 2
Y = 0
h = 30
w = 60

calc = Button(root, text = "Calculate", command = Calc)
calc.pack()
calc.place(x = X, y = Y, height = h, width = w)

clear = Button(root, text = "Clear", command = Clear)
clear.pack()
clear.place(x = X+w, y = Y, height = h, width = w)
# -------------------------------------------------------------------
root.mainloop()
