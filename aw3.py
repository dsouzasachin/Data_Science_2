# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 18:50:04 2021

@author: SACHIN F DSOUZA
"""

import pandas as pd
from urllib.request import urlopen
from sklearn.decomposition import PCA
from tqdm.notebook import tqdm
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

data = np.genfromtxt("aw3.txt",delimiter=',')

x_ar = data[:,0]
y_ar = data[:,1]

#Values being Initialized
B0 = 1;
B1 = 1;
n = len(data);

#1.3 : for B0 = 1 and B1 = 1
y_pr = B0 + B1*x_ar
errors = y_ar-y_pr
sqrd_errors = errors**2
sum_errors = sum(sqrd_errors)

loss_value = sum_errors/n

print("1.3  Loss Value for B0 = 1 and B1 = 1 is : ",loss_value)

#1.4
trials = 10
rate_of_learning = 0.001

for iteration in tqdm(range(trials)):
    y_pr = B0 + B1*x_ar
    change_B0 = -2*sum(y_ar-y_pr)/n
    change_B1 = -2*sum(x_ar*(y_ar-y_pr))/n
    B0 = B0 - rate_of_learning*change_B0
    B1 = B1 - rate_of_learning*change_B1
    
print("1.4  After {} iterations, B0 = {} AND B1 = {}".format(trials,B0,B1))

image_data = Image.open(urlopen("https://raw.githubusercontent.com/changyaochen/MECE4520/master/lectures/lecture_1/leena.png")) 
X = np.array(image_data) 

plt.figure() 
plt.imshow(image_data, cmap="gray") 
plt.show()

#2.1
print("2.1  Element at index (128,128) of matrix X is",str(X[128][128]))

#2.2
X_scal = []
for i in tqdm(range(X.shape[1])):
    column = X[:,i]
    new_column = (column-column.mean())/column.std()
    X_scal.append(new_column)

X_scal = np.asarray(X_scal).transpose()

print("2.2  The Scaled Value of X [128,128]",str(X_scal[128][128]))

#2.3

# performing PCA
pca = PCA()
pca_X = pca.fit_transform(X_scal)
print("2.3.a  The value of the first element of the first principal component",pca.components_[0][0])
# perform SVD
n = len(X_scal)
U, S, Vh = np.linalg.svd(X_scal.T @ X_scal / n)
print("2.3.b The value of the first element of the first principal component", U[0,0])

#2.4

#own code
cov_matrix = X - np.mean(X, axis = 1)
eig_val, eig_vec = np.linalg.eigh(np.cov(cov_matrix))
p = np.size(eig_vec, axis = 1)
idx = np.argsort(eig_val)
idx = idx[::-1]
eig_vec = eig_vec[:,idx]
eig_val = eig_val[idx]
pri_comp = 50
if pri_comp <p or pri_comp >0:
    eig_vec = eig_vec[:, range(pri_comp)]
    score = np.dot(eig_vec.T, cov_matrix)
    recon = np.dot(eig_vec,score) + np.mean(X, axis = 1).T
    recon_matrix = np.uint8(np.absolute(recon))

k_sum = 0
n_sum = 0
for i in range (len(recon_matrix)):
    k_sum += recon_matrix[i][i]
    n_sum += X[i][i]
    
print("2.4.a  If we only use the first 50 principal components of Xscaled to reconstruct this matrix, the reconstruction error is",str(1-k_sum/n_sum))

#from professors slides, calculate reconstruction error
U_reduced = U[:,:50]
Z = X_scal @ U_reduced
X_approx = Z @ U_reduced.T
reconstruction_error = (
        np.sum(np.square(np.linalg.norm((X_scal - X_approx), ord=2, axis=1))) 
        / np.sum(np.square(np.linalg.norm(X_scal, ord=2, axis=1)))
    )
print("2.4.b  If we only use the first 50 principal components of Xscaled to reconstruct this matrix, the reconstruction error is",reconstruction_error)