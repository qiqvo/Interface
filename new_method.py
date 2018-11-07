import numpy as np
from support import integral

# admits functional approach
def matr_to_function_transform(A):
	return lambda i, j: A[i][j]

# admits functional approach
def transpose(fA):
	return lambda i, j: fA(j, i)

# apply rule to elements in matrixes in matrix-product manner
# returns functional 
def prod(fA, fB, rule_mult, rule_sum, n, m, K):
	R = [[0 for _ in range(m)] for _ in range(n)]
	for i in range(n):
		for j in range(m):
			for k in range(K):
				if R[i][j] == 0:
					R[i][j] = rule_mult(fA(i, k), fB(k, j))
				else:
					R[i][j] = rule_sum(R[i][j], rule_mult(fA(i, k), fB(k, j)))

	return matr_to_function_transform(R)


# returns matrix of real values
def matrix_integrate_x(fA, a, b, n, m):
	IntA = [[0 for _ in range(m)] for _ in range(n)]
	for i in range(n):
		for j in range(m):
			IntA[i][j] = integral(fA(i, j), a, b)
	return IntA

# returns matrix of real values
def matrix_integrate_xt(fA, a, b, T, n, m):
	IntA = [[0 for _ in range(m)] for _ in range(n)]
	for i in range(n):
		for j in range(m):
			IntA[i][j] = integral(lambda t: (fA(i, j)(a, t)), 0, T) + \
						integral(lambda t: (fA(i, j)(b, t)), 0, T)	

	return IntA

def combine_matrix(P11, P12, P21, P22):
	n = len(P11) + len(P21) # height
	m = len(P11[0]) + len(P12[0]) # long

	P = [[0 for _ in range(m)] for j in range(n)] 
	def copy_block(wh, block, pi, pj):
		for i in range(len(block)):
			for j in range(len(block[0])):
				wh[i + pi][j + pj] = block[i][j]

	copy_block(P, P11, 0, 0)
	copy_block(P, P12, 0, len(P11[0]))
	copy_block(P, P21, len(P11), 0)
	copy_block(P, P22, len(P11), len(P11[0]))

	return P


def calcul(_B1, _B2, _B3, _B4, _Y1, _Y2, M_0, M_G, a, b, T):

	fB1, fB2, fB3, fB4 = matr_to_function_transform([_B1]), \
					matr_to_function_transform([_B2]), \
					matr_to_function_transform([_B3]), \
					matr_to_function_transform([_B4]), 
	ftrB1, ftrB2, ftrB3, ftrB4 = transpose(fB1), transpose(fB2), \
					transpose(fB3), transpose(fB4)

	fY1, fY2 = matr_to_function_transform([_Y1]), \
			matr_to_function_transform([_Y2])

	### int (B* B)	

	rule_mult_x = lambda f, g: lambda x: f(x) * g(x) 
	rule_mult_xt = lambda f, g: lambda x, t: f(x, t) * g(x, t) 

	rule_sum_x = lambda f, g: lambda x: f(x) + g(x) 
	rule_sum_xt = lambda f, g: lambda x, t: f(x, t) + g(x, t) 

	P11 = np.array(matrix_integrate_x(prod(ftrB1, fB1, rule_mult_x, rule_sum_x, M_0, M_0, 1), a, b, M_0, M_0))
	P21 = np.array(matrix_integrate_x(prod(ftrB1, fB2, rule_mult_x, rule_sum_x, M_0, M_G, 1), a, b, M_0, M_G))
	P31 = np.array(matrix_integrate_x(prod(ftrB2, fB1, rule_mult_x, rule_sum_x, M_G, M_0, 1), a, b, M_G, M_0))
	P41 = np.array(matrix_integrate_x(prod(ftrB2, fB2, rule_mult_x, rule_sum_x, M_G, M_G, 1), a, b, M_G, M_G))

	P12 = np.array(matrix_integrate_xt(prod(ftrB3, fB3, rule_mult_xt, rule_sum_xt, M_0, M_0, 1), a, b, T, M_0, M_0))
	P22 = np.array(matrix_integrate_xt(prod(ftrB3, fB4, rule_mult_xt, rule_sum_xt, M_0, M_G, 1), a, b, T, M_0, M_G))
	P32 = np.array(matrix_integrate_xt(prod(ftrB4, fB3, rule_mult_xt, rule_sum_xt, M_G, M_0, 1), a, b, T, M_G, M_0))
	P42 = np.array(matrix_integrate_xt(prod(ftrB4, fB4, rule_mult_xt, rule_sum_xt, M_G, M_G, 1), a, b, T, M_G, M_G))

	P1 = P11 + P12
	P2 = P21 + P22
	P3 = P31 + P32
	P4 = P41 + P42

	P = combine_matrix(P1, P2, P3, P4)

	### int (B* Y)
	Y11 = np.array(matrix_integrate_x(prod(ftrB1, fY1, rule_mult_x, rule_sum_x, M_0, 1, 1), a, b, M_0, 1))
	Y21 = np.array(matrix_integrate_x(prod(ftrB2, fY1, rule_mult_x, rule_sum_x, M_G, 1, 1), a, b, M_G, 1))

	Y12 = np.array(matrix_integrate_xt(prod(ftrB3, fY2, rule_mult_xt, rule_sum_xt, M_0, 1, 1), a, b, T, M_0, 1))
	Y22 = np.array(matrix_integrate_xt(prod(ftrB4, fY2, rule_mult_xt, rule_sum_xt, M_G, 1, 1), a, b, T, M_G, 1))

	Y1 = Y11 + Y12
	Y2 = Y21 + Y22

	Y = combine_matrix(Y1, [[]], Y2, [[]]) 

	u = np.linalg.solve(P, Y)
	return u

# TODO SMOKI: calculate error