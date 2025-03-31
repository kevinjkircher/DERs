## introduction
" This script implements the gradient descent method for unconstrained differentiable optimization in a simple example."

#
# Kevin J. Kircher, Purdue University, 2025
#

import numpy as np
import matplotlib.pyplot as plt

## objective function and its gradient
# objective function
def f(z):
    return np.exp(z[0] + 3 * z[1] - 0.1) + np.exp(z[0] - 3 * z[1] - 0.1) + np.exp(-z[0] - 0.1)

# gradient of objective function
def fGrad(z):
    return np.array([
        1,  # replace "1" with first component of gradient, similar to f = (z)
        2   # replace "2" with second component of gradient
    ])

## gradient descent implementation
# stopping conditions
K = 100  # maximum number of iterations
small = 1e-6  # stopping threshold for the norm of the gradient

# data storage
d = np.zeros((2, K)) # descent directions
x = np.zeros((2, K + 1)) # iterates
alpha = np.zeros(K + 1) # step sizes

# initialization
x[:, 0] = np.array([-2.5, 0.5]) #initial guess
alpha[0] = 1 # initial step size

# solution
for k in range(K):

    # descent direction
    # your code here

    # convergence check
    if # your code here:
        break

    # line search
    #
    # your
    # code
    # here
    #

    # iterate update
    # your code here

# trim data storage for unreached iterations
print(f'Gradient descent exited after {k+1} iterations.')
if k < K - 1:
    d = d[:, :k+1]
    x = x[:, :k+2]
    alpha = alpha[:k+2]
    K = k + 1

# plots
# function values
n = 1000 # number of grid points in each dimension
x1 = np.linspace(-3, 1, n)
x2 = np.linspace(-1, 1, n)
X1, X2 = np.meshgrid(x1, x2)
fPlot = np.zeros_like(X1)
for i in range(n):
    for j in range(n):
        fPlot[i, j] = f(np.array([X1[i, j], X2[i, j]]))

# contour plot
plt.figure(1)
plt.clf()
contour = plt.contour(X1, X2, fPlot, levels=20)
plt.clabel(contour, inline=True, fmt='%1.1f')
for k in range(K):
    plt.plot(x[0, k], x[1, k], 'o', markersize=10)
    if k > 0:
        plt.plot(x[0, k-1:k+1], x[1, k-1:k+1], 'k--')
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.axis('square')
plt.xlim([np.min(x1), np.max(x1)])
plt.ylim([np.min(x2), np.max(x2)])
plt.show()

# objective value plot
plt.figure(2)
plt.clf()
plt.subplot(3, 1, 1)
plt.semilogy(f(x) - 2.559266696658216)
plt.grid(True)
plt.ylabel('$f(x(k)) - f(x^\\star)$')
plt.xlim([1, K])
plt.ylim([1e-16, 1e1])
plt.yticks([1e-16, 1e-8, 1e0])

# gradient norm plot
gradNorms = np.zeros(K)
for k in range(K):
    gradNorms[k] = np.linalg.norm(fGrad(x[:, k]))

plt.subplot(3, 1, 2)
plt.semilogy(range(1, K + 1), gradNorms)
plt.grid(True)
plt.ylabel('$\\|\\nabla f(x(k))\\|$')
plt.xlim([1, K])
plt.ylim([1e-8, 1e1])
plt.yticks([1e-8, 1e-4, 1e0])

# step size plot
plt.subplot(3, 1, 3)
plt.plot(alpha)
plt.grid(True)
plt.ylabel('$\\alpha(k)$')
plt.xlabel('$k$')
plt.ylim([0, 1])
plt.xlim([1, K])
plt.show()
