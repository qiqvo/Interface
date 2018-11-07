import matplotlib
import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from math import *
from worksheet import Worker
import numpy as np
from tkinter import *
Pi = 3.14159265359

k1, k2, k = 2, 3, 5
c = 3
def y1(x, t):
	return x**k1 * exp(-k2*t)
def u1(x, t):
	return  k2* x*k1 *(-exp(-k2* t)) - k * ((k1 - 1)*k1*x**(k1 - 2) *exp(-k2 *t))

def y2(x, t):
	return sin(x*t)
def u2(x, t):
	return x*cos(t*x) + k*t**2 *sin(t* x)

def y3(x, t):
	return x**2 + x*t - t**2
def u3(x, t):
	return x - 2*t - k*2

def G1(x, t):
	return exp(-x**2 / (4*k *t))/(2*sqrt(Pi*t*k)) if t > 0 else 0	
def G2(x, y): # laplace
	return ln(x**2 + y**2)/(4* Pi)
def G3(x, t): # wave 
	return 1/(2*c) if t - abs(x/c) > 0 else 0


class Index_Funcs(object):
	def __init__(self, figure, ax):
		self._main_figure = figure
		self._main_plot_ax=ax
		self.T = self.a = self.b = 0
		self.marked_dots_T = []
		self.marked_dots_ab = []
		self.function = None
		self.operator = None
		self.operatorList = [("Lu = du/dt - k d^2 u/dx^2", G1)]
							# "Lu = d^2 u/dx^2 + d^2 u/dy^2", 
							# "Lu = d^2 u/dt^2 - c^2 d^2 u/dx^2"]
		self.functionList = [("y(x, t) = x**k1 * exp(-k2*t)", y1, u1), 
							("y(x, t) = sin(x*t)", y2, u2),
							("y(x, t) = x**2 + x*t - t**2", y3, u3)]
		   
	"""Helper class for marking dots on the separate UI window"""
	class DotBuilder:
		def __init__(self, dots, a, b, T):
			self.dots = dots
			self.left, self.right, self.time = a, b, T
			self._dots_ab = []
			self._dots_T  = []
			self._markedx = []
			self._markedy = []
			__far_left = a - a*0.2 - b*0.2 - T*0.2
			__far_right = b + b*0.2 + a*0.2 + T*0.2
			__far_down = - T*0.2 - a*0.2 - b*0.2
			self.cid = dots.figure.canvas.mpl_connect('button_press_event', self)
			plt.scatter([__far_left, 0, __far_right], [0, __far_down, 0], s=0.1, color = "#111111")

		"""When class object is called, if mouse click is in the scope, the dot is remembered"""
		def __call__(self, event):
			if event.inaxes!=self.dots.axes: 
				return
			if (event.xdata <= self.left and event.ydata <= self.time and event.ydata >= 0):
				self._dots_ab.append((event.xdata, event.ydata))
				self._markedx.append(event.xdata)
				self._markedy.append(event.ydata)
			if (event.xdata >= self.right and event.ydata <= self.time and event.ydata >= 0):
				self._dots_ab.append((event.xdata, event.ydata))
				self._markedx.append(event.xdata)
				self._markedy.append(event.ydata)
			if (event.ydata < 0 and event.xdata >= self.left and event.xdata <= self.right):
				self._dots_T.append((event.xdata, event.ydata))
				self._markedx.append(event.xdata)
				self._markedy.append(event.ydata)
			self.dots.set_color('r')
			self.dots.set_data(self._markedx, self._markedy)
			self.dots.figure.canvas.draw()
		
	"""Creates a window to mark the dots s_0, s_g
	After pressing confirm button dots are written in the class variable"""
	def dot_marker(self, event):
		fig = plt.figure()
		ax = fig.add_subplot(111, aspect="equal")
		ax.set_title('Позначте точки ')
		ax.add_patch(patches.Rectangle((self.a, 0), self.b - self.a, self.T, fc = 'b'))
		dot, = ax.plot([self.a + self.b/2], [self.T/2], 'b.')
		dotbuilder = self.DotBuilder(dot, self.a, self.b, self.T)
	
		def confirm(event):
			self.marked_dots_ab = dotbuilder._dots_ab.copy()
			self.marked_dots_T = dotbuilder._dots_T.copy()
			plt.close(fig)

		conf_buuton = widg.Button(plt.axes([0.8, 0.05, 0.1, 0.05]), "ОК")
		conf_buuton.on_clicked(confirm)
		plt.show()

	"""Opens a window, that lists avaliable operators, and gives opartunity to choose one"""
	def operator_listbox(self, event):
		top = Tk()
		Lb_oper = Listbox(top, width = 40)
		i = 1
		for op in self.operatorList:
			Lb_oper.insert(i, op[0])
			i += 1
		Lb_oper.pack()
    
		def confirm():
			self.operator = Lb_oper.curselection()[-1]
			self.update_text()
			top.destroy()
      
		B = Button(top, text = "Підтвердити оператор", command = confirm)
		B.pack()
		top.mainloop()

	"""Opens a window, that lists avaliable functions, and gives oportunity to choose one"""
	def function_listbox(self, event):
		top = Tk()
		Lb_func = Listbox(top, width = 40)
		i = 1
		for op in self.functionList:
			Lb_func.insert(i, op[0])
			i += 1
		Lb_func.pack()
    
		def confirm():
			self.function = Lb_func.curselection()[-1]
			self.update_text()
			top.destroy()
      
		B = Button(top, text = "Підтвердити функцію", command = confirm)
		B.pack()
		top.mainloop()

	def get_function(self):
		if self.function is not None:
			return self.functionList[self.function]
		else:
			return "y(x, t) = 0", lambda x, t : 0, lambda x, t : 0
	
	def get_operator(self):
		if self.operator is not None:
			return self.operatorList[self.operator]
		else:
			return "Lu = 0", lambda x, t : 0
	
	def submit_T(self, text_T):
		_t = 0
		try:
			_t = float(text_T)
		except:
			return "T should be a number"
		if _t >= 0:
			self.T = _t
		else:
			self.T = 0
		self.marked_dots_T = []
		self.marked_dots_ab = []
	
	def submit_a(self, text_a):
		_a = 0
		try:
			_a = float(text_a)
		except:
			return "a should be a number"
		self.a = _a
		self.marked_dots_T = []
		self.marked_dots_ab = []
	
	def submit_b(self, text_b):
		_b = 0
		try:
			_b = float(text_b)
		except:
			return "b should be a number"
		if _b >= self.a:
			self.b = _b
		else:
			self.b = self.a
		self.marked_dots_T = []
		self.marked_dots_ab = []
	
	def show(self, event):
		top = Tk()
		text = Text(top)
		mass = "The task will be solved for operator " + self.operatorList[self.operator] + " on the edges [a, b] = [" \
				+ str(self.a) + ", " + str(self.b) + "], T = " + str(self.T) + "\n The function is " + \
				self.functionList[self.function] 
		text.insert(INSERT, mass)
		text.pack()
		B = Button(top, text = "ОК", command = top.destroy)
		B.pack()
		top.mainloop()
	
	def set_text(self, text_oper, text_func):
		self.__text_oper = text_oper
		self.__text_func = text_func
	
	"""Changes text of operator and function in UI"""
	def update_text(self):
		text_operator, self.__G = self.get_operator()
		self.__text_oper.set_text(text_operator)
		text_function, self.__y, self.__u = self.get_function()
		self.__text_func.set_text(text_function)
	

	"""This function will collect the inputed data, solve the task and redraw solution"""
	def evaluateB(self, event):
		y, u, G = self.__y, self.__u, self.__G
		
		print("Evaluation began")
		w = Worker(y, u, G)   
		w.set_region_rectangle(self.a, self.b, self.T)
		w.set_modeling_function_points(self.marked_dots_T, self.marked_dots_ab)
		w.action()

		X = np.arange(self.a, self.b, 0.1)
		Y = np.arange(0, self.T, 0.1)
		X, Y = np.meshgrid(X, Y)

		print("Computing function in points")
		Z1 = np.array([[y(X[i][j], Y[i][j]) for j in range(len(X[0]))] for i in range(len(X))])
		Z2 = np.array([[w.y_inf(X[i][j], Y[i][j]) for j in range(len(X[0]))] for i in range(len(X))])
		Z3 = np.array([[(w.y_0(X[i][j], Y[i][j]) + w.y_G(X[i][j], Y[i][j]) + Z2[i][j])[0] for j in range(len(X[0]))] for i in range(len(X))])
		print("Operations finished")

		self._main_plot_ax.plot_surface(X, Y, Z1, color='b')
		# self._main_plot_ax.plot_surface(X, Y, Z2, color='y')
		self._main_plot_ax.plot_surface(X, Y, Z3, color='r') 
		fake2Dline1 = matplotlib.lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
		# fake2Dline2 = matplotlib.lines.Line2D([0],[0], linestyle="none", c='y', marker = 'o')
		fake2Dline3 = matplotlib.lines.Line2D([0],[0], linestyle="none", c='r', marker = 'o')
		# self._main_plot_ax.legend([fake2Dline1, fake2Dline2, fake2Dline3], ['Значення y', 'Значення y_inf', "Розв'язок"], numpoints = 1)
		self._main_plot_ax.legend([fake2Dline1, fake2Dline3], ['Значення y', "Розв'язок"], numpoints = 1)

		self._main_plot_ax.figure.canvas.draw()


class Window:
	"""Setting up axes for fields and buttons"""
	def __init__(self, fig, ax, figsize = (1, 1)):
		# * Placement
		self._figure = fig      
		self.plt_ax = ax
		# 1st and 2nd fields
		self._choose_operator = plt.axes([0.03, 0.82, 0.125, 0.05])   
		self._choose_function = plt.axes([0.03, 0.67, 0.125, 0.05])   
		# 3d field
		self._T_field = plt.axes([0.052, 0.48, 0.05, 0.035])            
		self._a_field = plt.axes([0.052, 0.36, 0.05, 0.035])            
		self._b_field = plt.axes([0.052, 0.29, 0.05, 0.035])            
		# 4th field button
		self._mark_dots = plt.axes([0.03, 0.20, 0.125, 0.05])
		# evaluate
		self._eval_field = plt.axes([0.85, 0.05, 0.1, 0.05])      		# for evaluation
		# operator and function textboxes
		self.__oper_text = plt.text(-8.1, 14.4, "Lu = 0", fontsize=15, style='italic')
		self.__func_text = plt.text(-8.1, 11.5, "y(x, t) = 0", fontsize=15, style='italic')
		self.callback = Index_Funcs(fig, ax)
		self.callback.set_text(self.__oper_text, self.__func_text)
		self._init_fields_()

	def _init_fields_(self):
		# * 1st field
		self._operator_b = widg.Button(self._choose_operator, r'Оберати оператор L', color = '#ffcc66')
		self._operator_b.on_clicked(self.callback.operator_listbox)
		# * 2nd field
		self._function_b = widg.Button(self._choose_function, "Оберати функцію y(x, t)", color = '#ffcc66')
		self._function_b.on_clicked(self.callback.function_listbox)
		# * 3rd field
		plt.text(-8.2, 10.2, "Введіть значення часу T для", fontsize=15, style='italic')
		plt.text(-8.2, 9.7, "  інтервалу [0, T]:", fontsize=15, style='italic')
		self._valueT_txtbox = widg.TextBox(self._T_field, "T = ", initial="0")
		self._valueT_txtbox.on_submit(self.callback.submit_T)
		plt.text(-8.2, 7.9, "Введіть значення границі спостереження", fontsize=15, style='italic')
		plt.text(-8.2, 7.4, "  a та b інтервалу [a, b]:", fontsize=15, style='italic')
		self._valuea_txtbox = widg.TextBox(self._a_field, "a = ", initial="0")
		self._valuea_txtbox.on_submit(self.callback.submit_a)
		self._valueb_txtbox = widg.TextBox(self._b_field, "b = ", initial="0")
		self._valueb_txtbox.on_submit(self.callback.submit_b)
		# * 4th field
		self._chose_ab_T_dots = widg.Button(self._mark_dots, "Позначити точки", color = '#ffcc66')
		self._chose_ab_T_dots.on_clicked(self.callback.dot_marker)
		# * EVALUATE button
		self._eval_button = widg.Button(self._eval_field, "Обрахувати", color='#ffcc00')
		self._eval_button.on_clicked(self.callback.evaluateB)


def main():
    fig = plt.figure(figsize=(22, 12), dpi = 72)
    ax = fig.gca(projection='3d')
    ax.set(xlabel="X", ylabel="T", zlabel="Y")
    wind = Window(fig, ax)
    plt.show()


if __name__ == "__main__":
	main()
