from Tkinter import *
import tkMessageBox
from math import *
import __future__

WIDTH = 250   # WIDTH = root.winfo_screenwidth()
HEIGHT = 450  # HEIGHT = root.winfo_screenheight()
w = 70
W = 180
H = 25

obj = ["R", "L", "C", "U", "omega_L", "omega_C", "omega_R", "U_Lmax", "U_Cmax",
       "omega_L1", "omega_L2", "omega_L0", "omega_C1", "omega_C2", "omega_C0"]
entry = {}


def GetVal(s):
	return 1.0 * eval(compile(entry[s].get().replace("e", "E"), '<string>', 'eval', __future__.division.compiler_flag))


def NewVal(s, v):
	entry[s].delete(0, len(entry[s].get()))
	entry[s].insert(END, v)


def Calc():
	if (entry["L"].get() == "" or entry["C"].get() == "" or entry["R"].get() == "" or entry["U"].get() == ""):
		tkMessageBox.showinfo("Error", "Please enter value of L, C, R and U")
		return None

	R = GetVal("R")
	L = GetVal("L")
	C = GetVal("C")
	U = GetVal("U")

	omega_L = 1.0 / (C * sqrt(L / C - R * R / 2.0))
	omega_C = (1.0 / L) * sqrt(L / C - R * R / 2.0)
	omega_R = 1.0 / sqrt(L * C)
	U_Lmax = (2.0 * U * L) / (R * sqrt(4 * L * C - R * R * C * C))
	U_Cmax = (2.0 * U * L) / (R * sqrt(4 * L * C - R * R * C * C))

	NewVal("omega_L", omega_L)
	NewVal("omega_C", omega_C)
	NewVal("omega_R", omega_R)
	NewVal("U_Lmax", U_Lmax)
	NewVal("U_Cmax", U_Cmax)

	if (entry["omega_L1"].get() != "" and entry["omega_L2"].get() != ""):
		omega_L1 = GetVal("omega_L1")
		omega_L2 = GetVal("omega_L2")
		omega_L0 = sqrt(2.0 / (1.0 / (omega_L1 ** 2) + 1.0 / (omega_L2 ** 2)))
		NewVal("omega_L0", omega_L0)

	if (entry["omega_C1"].get() != "" and entry["omega_C2"].get() != ""):
		omega_C1 = GetVal("omega_C1")
		omega_C2 = GetVal("omega_C2")
		omega_C0 = ((omega_C1 ** 2) + (omega_C2 ** 2)) / 2.0
		NewVal("omega_C0", omega_C0)


def Clear():
	for element in obj:
		entry[element].delete(0, len(entry[element].get()))


#-------------------------------------------------------------------
root = Tk()
root.wm_title("RLC - omega")
root.resizable(0, 0)  # disable maximize window size

frame = Frame(root, height=HEIGHT, width=WIDTH)
frame.pack()
#------------------------------------------------------------------
# Init
for i in range(len(obj)):
	element = obj[i]

	LAB = Label(root, text = element + " = ", justify = LEFT)
	LAB.pack(side = LEFT)
	LAB.place(x = 0, y = i * H, height = H, width = w)

	entry[element] = Entry(root)
	entry[element].pack(side = RIGHT)
	entry[element].place(x = w, y = i * H, height = H, width = W)

calc = Button(root, text = "Calculate!", command = Calc)
calc.pack()
calc.place(x = 35, y = 395, height = 30, width = 90)

clear = Button(root, text = "Clear", command = Clear)
clear.pack()
clear.place(x = 35 + 90, y = 395, height = 30, width = 90)
# -----------------------------------------------------------------
root.mainloop()
