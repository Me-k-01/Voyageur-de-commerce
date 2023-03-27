from algo_gen import algo_genetique
from algo_four import algo_fourmis
import numpy as np
from random import randint

# Chargement de la matrice adjacence à partir d'un fichier
def load_matrix():
    mat = []
    with open('mat_adjacence', 'r') as file:   
        for l in file.readlines():  
            val = [int(x) for x in l.split()]
            mat.append(val)            
    return mat

# Créer une matrice d'adjacence dont le cout du circuit Hamiltonien optimal est celui de la périphérie  
def create_matrix(n_ville):
    mat = np.zeros((n_ville, n_ville))
    
    for i in range(n_ville):
        for j in range(i, n_ville):
            cout = randint(2, 10)
            if i == j:
                cout = 0
            i_after = i+1 if i+1 < n_ville else 0
            if i_after == j:
                cout = 1
                 
            mat[i][j] = cout
            mat[j][i] = cout
    mat[n_ville-1][0] = 1
    mat[0][n_ville-1] = 1

    return mat

