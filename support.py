def gen_x(a, b, N= 250):
	return [a + (b-a)/N * i for i in range(N+1)]

def evalIntSimpson(func, a, b):
	return (b-a)/6 * (func(a) + 4* func((a+b)/2) + func(b))

def IntSimpson(func, arr):
	return sum([evalIntSimpson(func, arr[k], arr[k+1]) for k in range(len(arr) - 1)])


def integral(f, a, b):
	# return quad(f, a, b)[0]
	return IntSimpson(f, gen_x(a, b, 5*(b-a)))

def deriv(f, x):
	dx = 0.0001
	return (f(x+dx) - f(x-dx))/(2*dx)

def dderiv(f, x):
	df = lambda x: deriv(f, x)
	return deriv(df, x)
