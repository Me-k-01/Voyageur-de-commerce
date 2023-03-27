from random import randint, shuffle, random

def fitness(path, cost_mat): # Renvoie le coût d'un chemin, par rapport à la matrice d'adjacence
    travel_length = 0
    
    for i in range(0, len(path)):
        depart = path[i-1] # On compte aussi l'arrète entre la premiere et dernière ville (-1 en python -> dernier élément) 
        arrival = path[i]
        travel_length += cost_mat[depart][arrival]
    
    return travel_length  

def mort(pop):
    # Décremente la vie d'un individu et tue si <= 0
    new_pop = []
    
    for path in pop:
        path[1] -= 1
        
        # On ne garde que les individus vivants
        if path[1] >= 0:
            new_pop.append(path)
            
    return new_pop

# Selectionne de manière stockastique la partie de la population avec le meilleur fitness
def selection(population, nb_select, mat_cost):  
    """
    nb_select : taille de la population en sortie
    """
    
    new_pop = []
    # Selection des individus de la population 
    for _ in range(nb_select):
        f_sum = 0
        # Somme des fitness pour ponderation
        for indiv in population:
            f_sum += 1 / fitness(indiv[0], mat_cost) 
        # Parmis tout les individu
        # On en selectionne un
        r = random() * f_sum
        s = 0
        for indiv in population:
            s += 1 / fitness(indiv[0], mat_cost) # fi
            if r <= s:
                new_pop.append(indiv)
                break            
    return new_pop
    
    
"""    

def croisement(population, nb_enfants, life_time):
    for _ in range(0, nb_enfants // 2):
        # Selection des parents
        indice_parent1 = randint(0, len(population)-1)
        indice_parent2 = randint(0, len(population)-1)
        #print("indice du parent1:",indice_parent1,"  indice du parent 2:",indice_parent2)
        #print("taille de la pop:",len(population)-1)

        parent1=population[indice_parent1][0]
        parent2=population[indice_parent2][0]
        indice_same=randint(1, len(parent1) - 1)
        enfant1 = []
        enfant2 = []
        enfant1_temp = []
        enfant2_temp = []

        for x in range(0, indice_same):
            enfant1_temp.append(parent1[x])
            enfant2_temp.append(parent2[x])

        for y in range(indice_same, len(parent1)):
            enfant1_temp.append(parent2[y])
            enfant2_temp.append(parent1[y])

        for a in range(0, len(enfant1_temp)):
            if enfant1_temp[a] not in enfant1:
                enfant1.append(enfant1_temp[a])
            if enfant2_temp[a] not in enfant2:
                enfant2.append(enfant2_temp[a])
        
        for b in range(0, len(parent1)):
            if b not in enfant1:
                enfant1.append(b)
            if b not in enfant2:
                enfant2.append(b)
        
        population.append([enfant1, life_time])
        population.append([enfant2, life_time])
        #print(population)
 
"""

def select_indiv(population, quantity): # Choisit deux chemins de parents  
    i = 1
    selection = []
    while i <= quantity:
        # On selectionne un individu dans la population
        r_index = randint(0, len(population)-i)
        indiv = population[r_index][0]
        # On sépare le parent du reste des individus pour le choix du second parent, en le metant à la fin de la liste.
        population[r_index], population[-i] = population[-i], population[r_index]
        selection.append(indiv)
        i += 1  
    return selection 

def find_missing(arr):
    n = len(arr)
    missing = [] 
    for node in range(n):
        if node not in arr:
            missing.append(node)
    return missing 

def pick_index(arr): # tire un indice aléatoire de la liste  
    return randint(0, len(arr)-1)
 
# Change suivant un array avec index
def change(path, path_chunk, index): 
    """
    path : tableau du chemin
    path_chunk: tableau plus petit
    index: indice tel que taille du morceau + index < taille du chemin
    """
    size = len(path_chunk)
    if size + index > len(path):
        raise Exception("Taille de tableau dépassé")  
    # On remplace les anciennes valeurs par les nouvelle 
    left = path[:index] # Morceau gauche du chemin
    right = path[index + size:] # Morceau droit
    mod_arr = list(path_chunk)
    
    missing = find_missing(left+path_chunk+right) # On déduit les éléments manquants, à cause des redondances
    # Elimination des redondances en esquivant la partie de la liste qui a été modifié
    # On check chaque éléments rajouté et on tire parmis les elements manquants
    while missing: # Tant qu'il y a des elements manquants 
        #print("nouveau chemin",left+path_chunk+right)
        #print("tableau des elements inséré:", mod_arr)
        #print("tableau des elements manquants au nouveau chemin:", missing)
        added_node = mod_arr.pop() # On cherche parmis les elements inséré s'il n'y a pas une ville redondante
        if added_node in left:
            i = left.index(added_node)   
            left[i] = missing.pop(pick_index(missing)) # Ajout d'un element manquant  
        if added_node in right:
            i = right.index(added_node)   
            right[i] = missing.pop(pick_index(missing)) # Ajout d'un element manquant 

    return left + path_chunk + right
     

def croisement(population, nb_enfants, life_time, change_size=2): # Génère une liste d'enfants
    n_ville = len(population[0][0]) 
    enfants = []
    # Choix des parents (retourne une liste des chemins des parents selectionnés)
    parents = select_indiv(population, nb_enfants) 
    
    for i in range(0, nb_enfants, 2): # Pour chaque couple de parents
        ###### Croisement entre les deux parents ######
        parent_1 = parents[i]
        parent_2 = parents[i+1]
        # On crée deux enfants
        enfant_1 = list(parent_1)
        enfant_2 = list(parent_2) 
        
        # On change une des valeurs du premier enfant avec une valeur du second parent.
        r_index = randint(0, n_ville-1-change_size) 
        enfant_1 = change(enfant_1, parent_2[r_index:r_index+change_size], r_index)
        enfant_2 = change(enfant_2, parent_1[r_index:r_index+change_size], r_index)  
        
        enfants.append([enfant_1, life_time])
        enfants.append([enfant_2, life_time])
    
    return enfants

 
def mutation(pop, mutation_amount, mutation_influence):  # Quantité de mutation et influence en pourcentage
    last_index = len(pop) - 1
    n_ville = len(pop[0][0])
    stop_index = len(pop) - mutation_amount * len(pop)
    # Tant qu'il reste des mutations à faire
    while last_index >= stop_index :
        # Random entre seulement les parties de la population qui n'ont pas déjà recu de mutation
        i = randint(0, last_index) 
        # On applique la mutation
        for _ in range(int(mutation_influence * n_ville)):
            curr_indiv = pop[i][0]
            # Indices random
            r_index_1 = randint(0, n_ville-1) 
            r_index_2 = randint(0, n_ville-1)
            while r_index_2 == r_index_1: # forcer une autre valeur
                r_index_2 = randint(0, n_ville-1)
            # Swap de deux valeurs randoms
            curr_indiv[r_index_1], curr_indiv[r_index_2] = curr_indiv[r_index_2], curr_indiv[r_index_1]
            
        # On deplace l'individu muté vers la partie de la population déjà muté
        pop[i], pop[last_index] = pop[last_index], pop[i]
        # On decremente l'indice de séparation des deux parties du tableau
        last_index -= 1
        
def verif(population, mat_cost): #Cherche dans la population l'existence d'un meilleur parcours
    valeur = float('inf') 
    for indiv in population:
        f = fitness(indiv[0], mat_cost)
        if f <= valeur: #Sauvegarde de la meilleure valeur et chemin possible
            valeur = f
            chemin = indiv[0]
    return chemin, valeur

def population_init(mat, size, n_lives=5): #Initialise une population de taille size avec parcours aléatoire et nb cycles à 5
    population = []
    
    for _ in range(0, size):
        circuit = list(range(0, len(mat[0])))
        shuffle(circuit) # circuit random
        population.append([circuit, n_lives])
        
    return population

def algo_genetique(mat_cost, time_max=100, verbal=False): 
    """
    time_max : Nombre de cycle max
    """
    ###### Paramètres ###### 
    population_size = 10 # Taille initial de la population
    life_time = 10 # Nombre de cycle avant la mort d'un individu
    nb_enfants = 2 # Nombre d'enfant par cycle
    # Pourcentage de mutation
    mutation_amount = 0.2 # Taux d'individu a muter dans la population
    mutation_influence = 0.8 # Taux de changement sur l'individu à muter
    # Taille de l'heredité d'un parent
    mixte_length = len(mat_cost) - 1
    
    if verbal:
        print(mat_cost)
    
    time = 0 # Cycle actuel 
    population = population_init(mat_cost, population_size, life_time) 
    population = selection(population, population_size, mat_cost)
     
    while time < time_max and len(population) >= 2: 
        #croisement(population, nb_enfants, life_time)
        
        # On insert les enfants dans la populations
        population += croisement(population, nb_enfants, life_time, mixte_length)
        mutation(population, mutation_amount, mutation_influence)
        population = selection(population, population_size, mat_cost)
        population = mort(population) 
        time += 1
        
        if verbal:
            chemin_min, val_min = verif(population, mat_cost) 
            print("iteration:", time, ", nb individu:", len(population), "val_min :", val_min ) 
    
    chemin_min, val_min = verif(population, mat_cost) 
    if verbal: 
        print("Chemin min: ", chemin_min, " pour un cout de: ", val_min)
    return chemin_min, val_min
    
    
if __name__ == "__main__":
    from test import create_matrix
    #algo_genetique(create_matrix(10), time_max=100, verbal=True)
    
    e = croisement([
        [[0, 1, 2, 3, 4], 0],
        [[2, 4, 1, 3, 0], 0] 
        ], 2, life_time=0, change_size=4)
    
    print(e)