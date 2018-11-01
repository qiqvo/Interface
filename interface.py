import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import matplotlib.patches as patches
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

        # TODO: take the mouse clicks and add confirm button
        def dot_marker(self, event):
            class DotBuilder:
                def __init__(self, dots, a, b, T):
                    self.dots = dots
                    self.left, self.right, self.time = a, b, T
                    self.marked_dots_ab = []
                    self.marked_dots_T = []
                    self.__markedx = []
                    self.__markedy = []
                    __far_left = a - a*0.5 - b*0.5
                    __far_right = b + b*0.5 + a*0.5
                    __far_down = - T
                    self.cid = dots.figure.canvas.mpl_connect('button_press_event', self)
                    plt.scatter([__far_left, 0, __far_right], [0, __far_down, 0], s=[0.1, 0.1, 0.1], color = "#111111")

                def __call__(self, event):
                    print('click', event)
                    print("xydata : ", event.xdata, event.ydata)
                    print("a = ", self.left, "   b = ", self.right, "   T = ", self.time)
                    if event.inaxes!=self.dots.axes: return
                    
                    if (event.xdata <= self.left and event.ydata <= self.time and event.ydata >= 0):
                        self.marked_dots_ab.append((event.xdata, event.ydata))
                        self.__markedx.append(event.xdata)
                        self.__markedy.append(event.ydata)
                        print("Added to ab")
                    if (event.xdata >= self.right and event.xdata <= self.time and event.ydata >= 0):
                        self.marked_dots_ab.append((event.xdata, event.ydata))
                        self.__markedx.append(event.xdata)
                        self.__markedy.append(event.ydata)
                        print("Added to ab")
                    if (event.ydata < 0 and event.xdata >= self.left and event.ydata <= self.right):
                        self.marked_dots_T.append((event.xdata, event.ydata))
                        self.__markedx.append(event.xdata)
                        self.__markedy.append(event.ydata)
                        print("Added to t")
                    plt.scatter(self.__markedx, self.__markedy, s=1, color='#111111')

            fig = plt.figure()
            ax = fig.add_subplot(111, aspect="equal")
            ax.set_title('click to mark dots')
            ax.add_patch(patches.Rectangle((self.a, 0), self.b, self.T, fc = 'b'))
            dot, = ax.plot([0], [0])  # empty line
            dotbuilder = DotBuilder(dot, self.a, self.b, self.T)
            plt.show()

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

        # ! this one will be last - after averytjing is set up
        def evaluateB(self, event):
            pass


class Window:
    # TODO: update function and operator text
    # TODO: https://stackoverflow.com/questions/39223286/how-to-refresh-text-in-matplotlib
    def __init__(self, fig, figsize = (1, 1)):
        # * Placement
        self._figure = fig      # matplotlib figure
        # 1st and 2nd fields
        self._choose_operator = plt.axes([0.03, 0.82, 0.125, 0.05])   
        self._choose_function = plt.axes([0.03, 0.67, 0.125, 0.05])   
        # 3d field
        self._T_field = plt.axes([0.07, 0.49, 0.05, 0.035])              # *textbox with eval
        self._a_field = plt.axes([0.07, 0.38, 0.05, 0.035])            # left, third field
        self._b_field = plt.axes([0.07, 0.31, 0.05, 0.035])            # left, third field
        # 4th field button
        self._mark_dots = plt.axes([0.03, 0.23, 0.125, 0.05])
        # evaluate
        self._show_field = plt.axes([0.85, 0.1, 0.1, 0.05])      # show values
        self._eval_field = plt.axes([0.85, 0.05, 0.1, 0.05])      # for evaluate #!button
        self.__oper_text = plt.text(-7.8, 14.4, "Lu = 0", fontsize=12, style='italic',
                bbox={'facecolor': '#99CCFF', 'alpha': 0.5, 'pad': 10})
        self.__func_text = plt.text(-7.8, 11.5, "y(x, t) = 0", fontsize=12, style='italic',
                bbox={'facecolor': '#99CCFF', 'alpha': 0.5, 'pad': 10})
        self.callback = Index_Funcs()
        self._init_fields_()

    def _init_fields_(self):
        # * 1st field
        #self.__oper_text = plt.text(-7.8, 14.4, "Lu = 0", fontsize=12)
        self._operator_b = widg.Button(self._choose_operator, r'Choose operator L', color = '0.7')
        self._operator_b.on_clicked(self.callback.operator_listbox)
        self.__oper_text.set_text(self.callback.get_operator())
        # * 2nd field
        #self.__func_text = plt.text(-7.8, 11.5, "y(x, t) = 0", fontsize=12)
        self._function_b = widg.Button(self._choose_function, "Choose the function", color = '0.7')
        self._function_b.on_clicked(self.callback.function_listbox)
        self.__func_text.set_text(self.callback.get_function())

        # * 3rd field
        plt.text(-8.2, 10.2, "Input T value for [0, T] interval:", fontsize=12, style='italic',
                bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
        self._valueT_txtbox = widg.TextBox(self._T_field, "T = ", initial="0")
        self._valueT_txtbox.on_submit(self.callback.submit_T)
        plt.text(-8.2, 7.9, "Input a and b values for [a, b] interval:", fontsize=12, style='italic',
                bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
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
