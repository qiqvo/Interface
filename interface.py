import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from math import exp, sqrt
from worksheet import Worker
import numpy as np
from tkinter import *
Pi = 3.14159265359


class Index_Funcs(object):
        def __init__(self, figure):
            self._main_figure = figure
            self.T = self.a = self.b = 0
            self.marked_dots_T = []
            self.marked_dots_ab = []
            self.function = None
            self.operator = None
            # TODO: think of en effecient way to do this
            # TODO: also need a function that returns Green function
            self.operators = (lambda x: 21*x + 3, lambda x: 3*x*x + 3, lambda x: 21)
            self.operatorList = ["Lu = 21u + 3", "Lu = 3u^2 + u", "Lu = 12"]
            self.functions = (lambda x: 23*x + 4, lambda x: x*x + 5, lambda x: 21*x, lambda x: 49*x**4 + 45*x)
            self.functionList = ["f(x) = 23x + 4 * x^2 + 5", "f(x) = 12x", "f(x) = 49 * x^4 + 45x"]
           
	class DotBuilder:
		"""Helper class for marking dots on the separate UI window"""
                def __init__(self, dots, a, b, T):
                    self.dots = dots
                    self.left, self.right, self.time = a, b, T
                    self._dots_ab = []
                    self._dots_T = []
                    self._markedx = []
                    self._markedy = []
                    __far_left = a - a*0.2 - b*0.2 - T*0.2
                    __far_right = b + b*0.2 + a*0.2 + T*0.2
                    __far_down = - T*0.2 - a*0.2 - b*0.2
                    self.cid = dots.figure.canvas.mpl_connect('button_press_event', self)
                    plt.scatter([__far_left, 0, __far_right], [0, __far_down, 0], s=0.1, color = "#111111")

                def __call__(self, event):
			"""When class object is called, if mouse click is in the scope, the dot is remembered"""
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
        
        def dot_marker(self, event):
		"""Creates a window to mark the dots s_0, s_g
		After pressing confirm button dots are written in the class variable"""
            fig = plt.figure()
            ax = fig.add_subplot(111, aspect="equal")
            ax.set_title('click to mark dots')
            ax.add_patch(patches.Rectangle((self.a, 0), self.b, self.T, fc = 'b'))
            dot, = ax.plot([self.a + self.b/2], [self.T/2], 'b.')
            dotbuilder = DotBuilder(dot, self.a, self.b, self.T)
		
            def confirm(event):
                self.marked_dots_ab = dotbuilder._dots_ab.copy()
                self.marked_dots_T = dotbuilder._dots_T.copy()
                plt.close(fig)

            conf_buuton = widg.Button(plt.axes([0.8, 0.05, 0.1, 0.05]), "Confirm")
            conf_buuton.on_clicked(confirm)
            plt.show()
	
	def operator_listbox(self, event):
		"""Opens a window, that lists avaliable operators, and gives opartunity to choose one"""
            top = Tk()
            Lb_oper = Listbox(top, width = 40)
            i = 1
            for op in self.operatorList:
                Lb_oper.insert(i, op)
                i += 1
            Lb_oper.pack()

            def confirm():
                self.operator = Lb_oper.curselection()[-1]
                self.update_text()
                top.destroy()

            B = Button(top, text = "Confirm operator", command = confirm)
            B.pack()
            top.mainloop()

        def function_listbox(self, event):
		"""Opens a window, that lists avaliable functions, and gives opartunity to choose one"""
            top = Tk()
            Lb_func = Listbox(top, width = 40)
            i = 1
            for op in self.functionList:
                Lb_func.insert(i, op)
                i += 1
            Lb_func.pack()

            def confirm():
                self.function = Lb_func.curselection()[-1]
                self.update_text()
                top.destroy()

            B = Button(top, text = "Confirm function", command = confirm)
            B.pack()
            top.mainloop()

        def get_function(self):
            if self.function is not None:
                return self.functionList[self.function]
            else:
                return "y(x, t) = 0"

        def get_operator(self):
            if self.operator is not None:
                return self.operatorList[self.operator]
            else:
                return "Lu = 0"

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
        
        def submit_a(self, text_a):
            _a = 0
            try:
                _a = float(text_a)
            except:
                return "a should be a number"
            self.a = _a
        
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


        def show(self, event):
            top = Tk()
            text = Text(top)
            mass = "The task will be solved for operator " + self.operatorList[self.operator] + " on the edges [a, b] = [" \
                    + str(self.a) + ", " + str(self.b) + "], T = " + str(self.T) + "\n The function is " + \
                    self.functionList[self.function] 
            text.insert(INSERT, mass)
            text.pack()
            B = Button(top, text = "Ok", command = top.destroy)
            B.pack()
            top.mainloop()

        def set_text(self, text_oper, text_func):
            self.__text_oper = text_oper
            self.__text_func = text_func

        def update_text(self):
		"""Changes text of operator and function in UI"""
            self.__text_oper.set_text(self.get_operator())
            self.__text_func.set_text(self.get_function())

        # ! this one will be last - after averytjing is set up
        # TODO: finish this
        def evaluateB(self, event):
		"""This function will collect the inputed data, solve the task and redraw solution"""
            k1, k2 = 2, 3
            k = 1
            def y(x, t):
	            return x**k1 * exp(-k2*t)
            def G(x, t):
                return exp(-abs(x)**2 / (4*k**2 *t))/(2*k*sqrt(Pi*abs(t))) if t > 0 else 0

            def u(x, t):
                return  k2* x*k1 *(-exp(-k2* t)) - k**2 * ((k1 - 1)*k1*x**(k1 - 2) *exp(-k2 *t))
                # return x

            w = Worker(y, u, G)         # ! wait for appropriate functions
            w.set_region_rectangle(self.a, self.b, self.T)
            w.set_modeling_function_points(self.marked_dots_T, self.marked_dots_ab)

            w.action()

            X = np.arange(self.a, self.b, 0.1)
            Y = np.arange(0, self.T, 0.1)

            Xs = [[X[i] for j in range(Y)] for i in range(len(X))]
            Ys = [[Y[i] for j in range(Y)] for i in range(len(X))]
            Z1 = [[y(X[i], Y[j]) for j in range(Y)] for i in range(len(X))]
            Z2 = [[w.y_inf(X[i], Y[j]) for j in range(Y)] for i in range(len(X))]
            Z3 = [[w.y_0(X[i], Y[j]) + w.y_G(X[i], Y[j]) + Z2[i*len(X) + j] for j in range(Y)] for i in range(len(X))]

            plt.plot(Xs, Ys, Z1, "yo", label='y')
            plt.plot(Xs, Ys, Z2, "ro", label="y_inf")
            plt.plot(Xs, Ys, Z3, "bo", label='solution')
            plt.legend()
            #ax.set_zlim(-5, 12)


class Window:
    def __init__(self, fig, figsize = (1, 1)):
	"""Setting up axes for fields and buttons"""
        # * Placement
        self._figure = fig      # matplotlib figure
        # 1st and 2nd fields
        self._choose_operator = plt.axes([0.03, 0.82, 0.125, 0.05])   
        self._choose_function = plt.axes([0.03, 0.67, 0.125, 0.05])   
        # 3d field
        self._T_field = plt.axes([0.052, 0.49, 0.05, 0.035])              # *textbox with eval
        self._a_field = plt.axes([0.052, 0.38, 0.05, 0.035])            # left, third field
        self._b_field = plt.axes([0.052, 0.31, 0.05, 0.035])            # left, third field
        # 4th field button
        self._mark_dots = plt.axes([0.03, 0.23, 0.125, 0.05])
        # evaluate
        self._eval_field = plt.axes([0.85, 0.05, 0.1, 0.05])      # for evaluate #!button
        # operator and function textboxes
        self.__oper_text = plt.text(-8.1, 14.4, "Lu = 0", fontsize=15, style='italic')
                #bbox={'facecolor': '#99CCFF', 'alpha': 0.5, 'pad': 10})
        self.__func_text = plt.text(-8.1, 11.5, "y(x, t) = 0", fontsize=15, style='italic')
                #bbox={'facecolor': '#99CCFF', 'alpha': 0.5, 'pad': 10})
        self.callback = Index_Funcs(fig)
        self.callback.set_text(self.__oper_text, self.__func_text)
        self._init_fields_()

    def _init_fields_(self):
        # * 1st field
        self._operator_b = widg.Button(self._choose_operator, r'Choose operator L', color = '#ffcc66')
        self._operator_b.on_clicked(self.callback.operator_listbox)
        # * 2nd field
        self._function_b = widg.Button(self._choose_function, "Choose the function", color = '#ffcc66')
        self._function_b.on_clicked(self.callback.function_listbox)
        # * 3rd field
        plt.text(-8.2, 10.2, "Input T value for [0, T] interval:", fontsize=15, style='italic')
                #bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
        self._valueT_txtbox = widg.TextBox(self._T_field, "T = ", initial="0")
        self._valueT_txtbox.on_submit(self.callback.submit_T)
        plt.text(-8.2, 7.9, "Input a and b values for [a, b] interval:", fontsize=15, style='italic')
                #bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
        self._valuea_txtbox = widg.TextBox(self._a_field, "a = ", initial="0")
        self._valuea_txtbox.on_submit(self.callback.submit_a)
        self._valueb_txtbox = widg.TextBox(self._b_field, "b = ", initial="0")
        self._valueb_txtbox.on_submit(self.callback.submit_b)
        # * 4th field
        self._chose_ab_T_dots = widg.Button(self._mark_dots, "Mark dots", color = '#ffcc66')
        self._chose_ab_T_dots.on_clicked(self.callback.dot_marker)
        # * EVALUATE button
        self._eval_button = widg.Button(self._eval_field, "Evaluate", color='#ffcc00')
        self._eval_button.on_clicked(self.callback.evaluateB)

def main():
    fig = plt.figure(figsize=(22, 12), dpi = 80)
    ax = fig.gca(projection='3d')
    wind = Window(fig)

    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)

    ax.plot_surface(X, Y, Z)
    plt.show()


if __name__ == "__main__":
    main()
