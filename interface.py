import matplotlib.pyplot as plt
import matplotlib.widgets as widg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Index_Funcs(object):
    def __init__(self):
        self._values = {}

    def submit_y(self):
        pass

    def submit_T(self):
        pass
    
    def submit_a(self):
        pass
    
    def submit_b(self):
        pass

    def evaluateB(self):
        pass

    def update_ab(self):
        pass
    
    def update_T(self):
        pass

class Window:
    def __init__(self, fig, figsize = (1, 1)):
        # * Placement
        self._figure = fig      # matplotlib figure
        #self._oper_text = plt.axes([0.1, 0.85, 0.1, 0.05])       # left, 1st field
        #! ADD
        #self._oper_field = plt.axes([0.1, 0.78, 0.1, 0.05])       # *needs to be a scroolbar 
        # field with available operators
        #self._func_text =  plt.axes([0.1, 0.73, 0.1, 0.05])         # left, second field
        self._func_field =  plt.axes([0.07, 0.66, 0.09, 0.04])         # *simple TextBox with eval function
        # # field with available functions
        # self._ab_text = plt.axes([0.1, 0.59, 0.1, 0.05])            # left, third field
        # self._T_text = plt.axes([0.1, 0.52, 0.1, 0.05])             # *textbox with eval
        self._T_field = plt.axes([0.1, 0.49, 0.05, 0.035])              # *textbox with eval
        self._a_field = plt.axes([0.1, 0.39, 0.05, 0.035])            # left, third field
        self._b_field = plt.axes([0.1, 0.32, 0.05, 0.035])            # left, third field
        # 2 fieds for writing
        #self._choose_dots_text = plt.axes([0.1, 0.24, 0.1, 0.05])    # left, forth field - #! probably should be a button
        #self._chose_ab_field = plt.axes([0.1, 0.17, 0.1, 0.05])       #! needs to be in a separate window
        #self._chose_T_field = plt.axes([0.1, 0.1, 0.1, 0.05])        #! needs to be in a separate window
        # 2 fields for segments
        self._eval_field = plt.axes([0.85, 0.05, 0.1, 0.05])      # for evaluate #!button
        self.callback = Index_Funcs()
        self._init_fields_()

    def _init_fields_(self):
        #TODO: placements of the boxes 
        # TODO: 1st field
        plt.text(-8.2, 15.5, r'Choose operator L:', fontsize=12)           # first field --- listbox
        #ax.text(2, 6, r'Write down the function, you want to evaluate', fontsize=15)    # second field
        # * 2nd field
        plt.text(-8.2, 13.4, "Write down the function", fontsize=12)
        self._oper_txtbox = widg.TextBox(self._func_field, "y(x, t) = ", initial="0")
        self._oper_txtbox.on_submit(self.callback.submit_y)
        
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
        #self._ab_text.text(0.1, 4, "Chose the values outside the field [0, T], \n where we will have our observations", fontsize=8)
        # TODO: scroolig field for T
        #self._T_text.text(0.1, 6, "Chose the values outside the field [a, b], \n where we will have our observations", fontsize=8)
        # TODO: scrooling field for [a, b]
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
