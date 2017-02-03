from Tkinter import *
import tkMessageBox
from math import *
import __future__

WIDTH = 500   # WIDTH = root.winfo_screenwidth()
HEIGHT = 450  # HEIGHT = root.winfo_screenheight()
w = 75
W = 160
H = 25

obj = [["R", "U", "omega"],
       ["C1", "C2", "L"],
       ["L", "r", "Z_C", "C", "U_Cmax"],
       ["L", "r", "Z_C", "C", "U_RCmax"],
       ["L", "r", "C", "P", "I", "U_dmax"]
      ]
entry = [{}, {}, {}, {}, {}]
LAB = ["",
       "< 1 >   C1, C2 -> P1 = P2",
       "< 2 >   C -> U_C max",
       "< 3 >   C -> U_RC max",
       "< 4 >   C -> P, I, U_d max"]
calc = {}
clear = {}

def GetVal(cnt, s):
	return 1.0 * eval(compile(entry[cnt][s].get().replace("e", "E"), '<string>', 'eval', __future__.division.compiler_flag))


def NewVal(cnt, s, v):
	entry[cnt][s].delete(0, len(entry[cnt][s].get()))
	entry[cnt][s].insert(END, v)


def Calc(cnt):
	R = GetVal(0, "R")
	U = GetVal(0, "U")
	omega = GetVal(0, "omega")

	if (cnt == 1):
		if (entry[cnt]["C1"].get() == "" or entry[cnt]["C2"].get() == ""):
			tkMessageBox.showinfo("Error", "Please enter value of C1 and C2")
			return None

		C1 = GetVal(cnt, "C1")
		C2 = GetVal(cnt, "C2")
		L = (1.0 / C1 + 1.0 / C2) / (2.0 * omega * omega)

		NewVal(cnt, "L", L)

	elif (cnt == 2):
		if (entry[cnt]["L"].get() == "" or entry[cnt]["r"].get() == ""):
			tkMessageBox.showinfo("Error", "Please enter value of L and r")
			return None

		L = GetVal(cnt, "L")
		r = GetVal(cnt, "r")
		_R = R + r
		Z_L = omega * L
		Z_C = (_R * _R + Z_L * Z_L) / Z_L
		C = 1.0 / (omega * Z_C)
		U_Cmax = (U * sqrt(_R * _R + Z_L * Z_L)) / _R

		NewVal(cnt, "Z_C", Z_C)
		NewVal(cnt, "C", C)
		NewVal(cnt, "U_Cmax", U_Cmax)

	elif (cnt == 3):
		if (entry[cnt]["L"].get() == "" or entry[cnt]["r"].get() == ""):
			tkMessageBox.showinfo("Error", "Please enter value of L and r")
			return None

		L = GetVal(cnt, "L")
		r = 0 #r = GetVal(cnt, "r")
		_R = R + r
		Z_L = omega * L
		Z_C = (Z_L + (Z_L * Z_L + 4 * _R * _R)) / 2.0
		C = 1.0 / (omega * Z_C)
		U_RCmax = (U * (Z_L + (Z_L * Z_L + 4 * _R * _R))) / (2.0 * _R)

		NewVal(cnt, "Z_C", Z_C)
		NewVal(cnt, "C", C)
		NewVal(cnt, "U_RCmax", U_RCmax)

	elif (cnt == 4):
		if (entry[cnt]["L"].get() == "" or entry[cnt]["r"].get() == ""):
			tkMessageBox.showinfo("Error", "Please enter value of L and r")
			return None

		L = GetVal(cnt, "L")
		r = GetVal(cnt, "r")
		Z_L = omega * L
		_R = R + r
		C = 1.0 / (omega * omega * L)
		P = U * U / _R
		I = U / R
		U_dmax = I * sqrt(r * r + Z_L * Z_L)

		NewVal(cnt, "C", C)
		NewVal(cnt, "P", P)
		NewVal(cnt, "I", I)
		NewVal(cnt, "U_dmax", U_dmax)


def Clear(cnt):
	for element in obj[cnt]:
		entry[cnt][element].delete(0, len(entry[cnt][element].get()))


#-------------------------------------------------------------------
root = Tk()
root.wm_title("RLC - C")
root.resizable(0, 0)  # disable maximize window size

frame = Frame(root, height=HEIGHT, width=WIDTH)
frame.pack()
#------------------------------------------------------------------
# Init
F = 3 * H + 10
H_frame = 7 * H + 5

for cnt in range(len(LAB)):
	if (cnt > 0):
		labelframe = LabelFrame(root, text=LAB[cnt])
		labelframe.pack(fill="both")
		labelframe.place(x = WIDTH // 2 * ((cnt-1) % 2), y = F, width = WIDTH / 2, height = H_frame)

		for i in range(len(obj[cnt])):
			element = obj[cnt][i]

			LAB1 = Label(labelframe, text=element + " = ", justify=LEFT)
			LAB1.pack(side=LEFT)
			LAB1.place(x = 0, y = 5 + i * H, height=H, width=w)

			entry[cnt][element] = Entry(labelframe)
			entry[cnt][element].pack(side=RIGHT)
			entry[cnt][element].place(x = w, y = 5 + i * H, height=H, width=W)

		if (cnt % 2 == 0):
			F += H_frame
	else:
		for i in range(len(obj[cnt])):
			element = obj[cnt][i]

			LAB1 = Label(root, text = element + " = ", justify = LEFT)
			LAB1.pack(side = LEFT)
			LAB1.place(x = 0, y = i * H, height = H, width = w)

			entry[cnt][element] = Entry(root)
			entry[cnt][element].pack(side = RIGHT)
			entry[cnt][element].place(x = w, y = i * H, height = H, width = W)

X = WIDTH // 2
Y = 0
h = 30
w = 60

for i in range(1, len(LAB)):
	calc[i] = Button(root, text = "Calc <"+str(i)+">", command = lambda cnt = i: Calc(cnt))
	calc[i].pack()
	calc[i].place(x = X+(i-1)*w, y = Y, height = h, width = w)

	clear[i] = Button(root, text = "Clear <"+str(i)+">", command = lambda cnt = i: Clear(cnt))
	clear[i].pack()
	clear[i].place(x = X+(i-1)*w, y = Y+h, height = h, width = w)

# -------------------------------------------------------------------
root.mainloop()
