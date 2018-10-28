import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import matplotlib.patches as pat
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



class Index_Funcs(object):
    def __init__(self):
        self.T = self.a = self.b = 0
        self.markedDots_T = []
        self.markedDots_ab = []
        self.function = None
        self.operator = None
        
    # https://stackoverflow.com/questions/40467672/add-dropdown-list-and-text-box-in-matplotlib-and-show-plot-according-to-the-inpu
    # !DO AS A LISTBOX
    def submit_operator(self):
        pass
    
    # !DO AS A LISTBOX
    def submit_function(self):
        pass

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

    # ! this one will be last - after averytjing is set up
    def evaluateB(self, event):
        pass

    def __mouse_click_on(self, event):
        ix, iy = event.xdata, event.ydata
        print("x = ", ix, " y = ", iy)
        if((ix < self.a or ix > self.b) and (iy <= self.T and iy >=0)):
            self.markedDots_T.append((ix, iy))
        elif((ix >= self.a and ix <= self.b) and iy <= 0):
            self.markedDots_ab.append((ix, iy))


    def __mouse_click_off(self, event):
        self.fig.canvas.mpl_disconnect(self.cid)

    def dot_marker(self, event):
        self.fig = plt.figure()
        self.cid = fig.canvas.mpl_connect("mouse click event", self.__mouse_click_on)
        rect = plt.Rectangle((self.a, 0), self.b, self.T, fc = 'b')
        plt.gca().add_patch(rect)
        plt.axis('scaled')
        plt.show()
        ax = [0.01, 0.01, 0.05, 0.02]
        stop_marking = widg.Button(ax, "Stop marking dots")
        stop_marking.on_clicked(self.__mouse_click_off)
        plt.close(fig = self.fig)




class Window:
    def __init__(self, fig, figsize = (1, 1)):
        # * Placement
        self._figure = fig      # matplotlib figure
        #self._oper_text = plt.axes([0.1, 0.85, 0.1, 0.05])       # left, 1st field
        #! ADD
        #self._oper_field = plt.axes([0.1, 0.78, 0.1, 0.05])       # *needs to be a scroolbox 
        # field with available operators
        self._func_field =  plt.axes([0.07, 0.66, 0.09, 0.04])         # *simple TextBox with eval function
        # # field with available functions
        self._T_field = plt.axes([0.1, 0.49, 0.05, 0.035])              # *textbox with eval
        self._a_field = plt.axes([0.1, 0.39, 0.05, 0.035])            # left, third field
        self._b_field = plt.axes([0.1, 0.32, 0.05, 0.035])            # left, third field
        # 4th field button
        self._mark_dots = plt.axes([0.1, 0.23, 0.05, 0.035])
        # evaluate
        self._eval_field = plt.axes([0.85, 0.05, 0.1, 0.05])      # for evaluate #!button
        self.callback = Index_Funcs()
        self._init_fields_()

    def _init_fields_(self):
        # TODO: 1st field, 2nd field ---- as listboxes
        # * 1st field
        # TODO:
        plt.text(-8.2, 15.5, r'Choose operator L:', fontsize=12)           # first field --- listbox
        # * 2nd field 
        # TODO: 
        plt.text(-8.2, 13.4, "Choose the function", fontsize=12)
        #self._oper_txtbox = widg.TextBox(self._func_field, "y(x, t) = ", initial="0")
        #self._oper_txtbox.on_submit(self.callback.submit_y)
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
