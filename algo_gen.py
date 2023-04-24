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
 
def selection(population, nb_select, mat_cost):  
    """
    Selectionne de manière stockastique une partie de la population. Les chances de selection sont inversement proportionnel au fitness.
        population : liste 3D, un individu est un couple
        nb_select : taille de la population en sortie
        mat_cost : matrice d'adjacence
    """
    
    new_pop = []
    # Selection des individus de la population 
    for _ in range(nb_select):
        p_sum = 0 
        # Somme des proba d'être choisis pour avoir des proportions
        for indiv in population:
            p_sum += 1 / fitness(indiv[0], mat_cost)  # p_choisis inversement proportionnel au fitness
            
        # Parmi tout les individu, on en selectionne un
        r = random() * p_sum
        selector = 0
        for indiv in population:
            selector += 1 / fitness(indiv[0], mat_cost) 
            if r <= selector: # On a trouvé l'individu séléctionné
                new_pop.append(indiv)
                break

    return new_pop

def find_missing(arr):
    missing = [] 
    for node in range(len(arr)):
        if node not in arr:
            missing.append(node)
    return missing 

def pick_index(arr): # tire un indice aléatoire de la liste  
    return randint(0, len(arr)-1)
 

def change(path, path_chunk, index): 
    """
    Modifie les valeurs d'un tableau depuis un indice donné avec les valeurs d'un autre sous-tableau.
        path : tableau du chemin
        path_chunk: tableau plus petit
        index: indice tel que taille du morceau + index < taille du chemin
    """
    #print(path)
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
    population_size = len(population)
    #if nb_enfants > len(population):
    #    raise Exception("Nombre d'enfants trop grands")
    
    shuffle(population) # On s'assure de tirer des couples de parents aléatoirements
    
    for i in range(0, nb_enfants, 2): # Pour chaque couple de parents
        ###### Croisement entre les deux parents ######
        # Chemin des parents
        parent_1 = population[(i)%population_size][0] # Si on a pas assez de parents, on boucle 
        parent_2 = population[(i+1)%population_size][0]
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
        
def find_best_path(population, mat_cost): # Cherche dans la population l'existence d'un meilleur parcours
    fitness_min = float('inf') 
    path_min = None
    
    for indiv in population:
        f = fitness(indiv[0], mat_cost)
        if f <= fitness_min: # Sauvegarde de la meilleure valeur et chemin possible
            fitness_min = f
            path_min = indiv[0]
            
    return path_min, fitness_min

def population_init(mat, size, n_lives=5): #Initialise une population de taille size avec parcours aléatoire et nb cycles à 5
    population = []
    
    for _ in range(0, size):
        circuit = list(range(0, len(mat[0])))
        shuffle(circuit) # circuit random
        population.append([circuit, n_lives])
        
    return population

def algo_genetique(mat_cost, time_max=100, n_indiv=10, verbal=False): 
    """
    time_max : Nombre de cycle max
    """
    ###### Paramètres ###### 
    population_size = 20 # Taille initial de la population
    life_time = 10 # Nombre de cycle avant la mort d'un individu
    # Croisement
    nb_enfants = n_indiv # Nombre d'enfant par cycle
    mixte_length = len(mat_cost) // 2 # Taille de l'heredité d'un parent
    # Pourcentage de mutation
    mutation_amount = 0.2 # Taux d'individu a muter dans la population
    mutation_influence = 0.8 # Taux de changement sur l'individu à muter
    ########################
    
    if verbal:
        print(mat_cost)
    
    time = 0 # Cycle actuel 
    population = population_init(mat_cost, population_size, life_time) 
    population = selection(population, population_size, mat_cost)
     
    while time < time_max and len(population) >= 2: 
        # On insert les enfants dans la populations
        population += croisement(population, nb_enfants, life_time, mixte_length)
        mutation(population, mutation_amount, mutation_influence)
        population = selection(population, population_size, mat_cost)
        population = mort(population) 
        time += 1
        
        if verbal:
            chemin_min, val_min = find_best_path(population, mat_cost) 
            print("iteration:", time, ", nb individu:", len(population), "val_min :", val_min ) 
    
    chemin_min, val_min = find_best_path(population, mat_cost) 
    if verbal: 
        print("Chemin min: ", chemin_min, " pour un cout de: ", val_min)
    return chemin_min, val_min
    
    
if __name__ == "__main__":
    from test import create_matrix
    algo_genetique(create_matrix(7), time_max=100, verbal=True)
    