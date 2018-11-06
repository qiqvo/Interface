#!/usr/bin/env python3

import random as r
import matplotlib.pyplot as plt
from math import exp, sqrt
import numpy as np
# from numpy
from scipy import integrate

from functools import partial # to bind functions
# from math import *
from copy import copy

from new_method import calcul
from support import integral

# TODO: add flexibility to have no point selected 

class Worker:
	def __init__(self, y, u, G):
		self.y = y
		self.u = u
		self.G = G

	def set_region_rectangle(self, a, b, T, t0 = 0):
		self.a = a
		self.b = b
		self.T = T

	# TODO SMOKI: calculate integral faster
	def y_inf(self, x, t):
		return integral(lambda x1: integral(lambda t1: self.G(x1 - x, t1 - t) * self.u(x1, t1), 0, self.T), self.a, self.b)

	def set_modeling_function_points(self, s_0, s_G):
		# points of observation before [0, T]
		self.s_0 = s_0
		# points of observation outside [a, b]
		self.s_G = s_G

		self.M_0 = len(s_0) # number of observations before [0, T]
		self.M_G = len(s_G) # number of observations outside [a, b]

	def action(self):
		B11 = list(map(lambda s: lambda x: self.G(x - s[0], 0 - s[1]), self.s_0))
		B12 = list(map(lambda s: lambda x: self.G(x - s[0], 0 - s[1]), self.s_G))
		
		B21 = list(map(lambda s: lambda x, t: self.G(x - s[0], t - s[1]) if x == self.a or x == self.b else 0, self.s_0))
		B22 = list(map(lambda s: lambda x, t: self.G(x - s[0], t - s[1]) if x == self.a or x == self.b else 0, self.s_G))
		
		Y_0 = [lambda x: self.y(x, 0) - self.y_inf(x, 0)]
		Y_G = [lambda x, t: self.y(x, t) - self.y_inf(x, t) if x == self.a or x == self.b else 0]
		
		u_all = calcul(B11, B12, B21, B22, Y_0, Y_G, self.M_0, self.M_G, self.a, self.b, self.T)
		self.u_0, self.u_G = u_all[:self.M_0], u_all[self.M_0:]
		
		self.y_0 = lambda x, t: sum(self.G(x - self.s_0[i][1], t - 0) * self.u_0[i] for i in range(self.M_0))
		print('ph4')
		self.y_G = lambda x, t: sum(self.G(x - self.s_G[i][0], t - self.s_G[i][1]) * self.u_G[i] for i in range(self.M_G))
		print('ph5')
		self.solution = lambda x, t : self.y_0(x, t) + self.y_G(x, t) + self.y_inf(x, t)
		print('ph6')

		return self.solution