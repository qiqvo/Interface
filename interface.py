import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import matplotlib.patches as pat
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tkinter import *


class Index_Funcs(object):
    def __init__(self):
        self.T = self.a = self.b = 0
        self.markedDots_T = []
        self.markedDots_ab = []
        self.function = None
        self.operator = None
        self.operatorList = ["Lu = 21u + 3", "Lu = 3u' + u", "Lu = 12"]
        self.functionList = ["f(x) = 23x + 4 * x^2 + 5", "f(x) = 12x", "f(x) = 49 * x^4 + 45x"]


    def operator_listbox(self, event):
        top = Tk()
        Lb_oper = Listbox(top, width = 40)
        i = 1
        for op in self.operatorList:
            Lb_oper.insert(i, op)
            i += 1
        Lb_oper.pack()

        def confirm():
            self.operator = Lb_oper.curselection()[-1]
            top.destroy()

        B = Button(top, text = "Confirm operator", command = confirm)
        B.pack()
        top.mainloop()


    def function_listbox(self, event):
        top = Tk()
        Lb_func = Listbox(top, width = 40)
        i = 1
        for op in self.functionList:
            Lb_func.insert(i, op)
            i += 1
        Lb_func.pack()

        def confirm():
            self.function = Lb_func.curselection()[-1]
            top.destroy()

        B = Button(top, text = "Confirm function", command = confirm)
        B.pack()
        top.mainloop()


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

    # TODO: make it work
    # TOFIX: bounds of blue box or axis
    def dot_marker(self, event):

        def __mouse_click_on(event):
            # doesn't go here for some reason
            ix, iy = event.xdata, event.ydata
            print("x = ", ix, " y = ", iy)
            if((ix < self.a or ix > self.b) and (iy <= self.T and iy >=0)):
                self.markedDots_T.append((ix, iy))
            elif((ix >= self.a and ix <= self.b) and iy <= 0):
                self.markedDots_ab.append((ix, iy))

        fig = plt.figure()
        cid = fig.canvas.mpl_connect("mouse click event", __mouse_click_on)
        rect = plt.Rectangle((self.a, 0), self.b, self.T, fc = 'b')
        plt.gca().add_patch(rect)
        plt.axis('scaled')
        plt.show()


        def __mouse_click_off(event):
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig = fig)


        ax = [0.1, 0.1, 0.05, 0.02]
        stop_marking = widg.Button(ax, "Stop marking dots")
        stop_marking.on_clicked(__mouse_click_off)


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


    # TODO: this one will be last - after averytjing is set up
    def evaluateB(self, event):
        pass


class Window:
    def __init__(self, fig, figsize = (1, 1)):
        # * Placement
        self._figure = fig      # matplotlib figure
        # 1st and 2nd fields
        self._choose_operator = plt.axes([0.05, 0.8, 0.125, 0.05])   
        self._choose_function = plt.axes([0.05, 0.7, 0.125, 0.05])   
        # 3d field
        self._T_field = plt.axes([0.1, 0.49, 0.05, 0.035])              # *textbox with eval
        self._a_field = plt.axes([0.1, 0.39, 0.05, 0.035])            # left, third field
        self._b_field = plt.axes([0.1, 0.32, 0.05, 0.035])            # left, third field
        # 4th field button
        self._mark_dots = plt.axes([0.1, 0.23, 0.05, 0.035])
        # evaluate
        self._show_field = plt.axes([0.85, 0.1, 0.1, 0.05])      # show values
        self._eval_field = plt.axes([0.85, 0.05, 0.1, 0.05])      # for evaluate #!button
        self.callback = Index_Funcs()
        self._init_fields_()


    def _init_fields_(self):
        # * 1st field
        self._operator_b = widg.Button(self._choose_operator, r'Choose operator L', color = '0.7')
        self._operator_b.on_clicked(self.callback.operator_listbox)
        # * 2nd field
        self._function_b = widg.Button(self._choose_function, "Choose the function", color = '0.7')
        self._function_b.on_clicked(self.callback.function_listbox)
        # * 3rd field
        plt.text(-8.2, 9.8, "Input T value for [0, T] interval", fontsize=12)
        self._valueT_txtbox = widg.TextBox(self._T_field, "T = ", initial="0")
        self._valueT_txtbox.on_submit(self.callback.submit_T)
        plt.text(-8.2, 7.8, "Input a and b values for [a, b] interval", fontsize=12)
        self._valuea_txtbox = widg.TextBox(self._a_field, "a = ", initial="0")
        self._valuea_txtbox.on_submit(self.callback.submit_a)
        self._valueb_txtbox = widg.TextBox(self._b_field, "b = ", initial="0")
        self._valueb_txtbox.on_submit(self.callback.submit_b)
        # * 4th field
        self._chose_ab_T_dots = widg.Button(self._mark_dots, "Mark dots", color = '0.7')
        self._chose_ab_T_dots.on_clicked(self.callback.dot_marker)
        # * Show chosen parameters
        self._show_chosen = widg.Button(self._show_field, "Show task", color='0.9')
        self._show_chosen.on_clicked(self.callback.show)
        # * EVALUATE button
        self._eval_button = widg.Button(self._eval_field, "Evaluate", color='0.9')
        self._eval_button.on_clicked(self.callback.evaluateB)



fig = plt.figure(figsize=(16, 9), dpi = 80)#, facecolor='#696969', edgecolor= "#696969")
ax = fig.gca(projection='3d')
wind = Window(fig)

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

ax.plot_surface(X, Y, Z)
plt.show()
