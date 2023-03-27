from random import shuffle, random
import numpy as np

def population_init(nb_ville, size):
    population = []
    
    for _ in range(size):
        circuit = list(range(nb_ville))
        shuffle(circuit) # circuit random
        population.append([circuit, 5])
        
    return population

def get_path_cost(cost_mat, path): # Renvoie le coût d'un chemin, par rapport à la matrice d'adjacence
    travel_length = 0
    
    for i in range(0, len(path)):
        depart = path[i-1] # On compte aussi l'arrète entre la premiere et dernière ville (-1 en python -> dernier élément) 
        arrival = path[i]
        travel_length += cost_mat[depart][arrival]
    
    return travel_length  


class Agent:
    def __init__(self, nodes_to_explore, deposit_Q, prob_explore_Y=1, pheromone_influence=1, distance_influence=1):
        self.starting_node = 0 # Toute les fourmies commencent au même endroit
        self.deposit_Q = deposit_Q
        self.null_prob = prob_explore_Y 
        # Pour la decision de l'exploration
        self.pheromone_influence = pheromone_influence # Importance des phéromone
        self.distance_influence = distance_influence # Importance de la distance d'une ville
        self.reset_exploration(list(nodes_to_explore)) 
    
     
    def reset_exploration(self, nodes_to_explore):
        self.unexplored = nodes_to_explore
        self.unexplored.remove(self.starting_node)
        self.explored = [self.starting_node]
    
    
    def deposite_pheromone(self, mat_cost, mat_pheromone):
        pheromone_quantity = self.deposit_Q / get_path_cost(mat_cost, self.explored) 
        
        for i in range(1, len(self.explored)):
            depart = self.explored[i-1]
            arrival = self.explored[i]
            
            # On dépose les phéromones sur les arrettes
            mat_pheromone[depart][arrival] += pheromone_quantity
          
          
      
    def choose_next_location(self, mat_cost, mat_pheromone):
        # On choisit la prochaine ville à explorer aléatoirement selon les phéromones,
        # avec une probabilité non-nul d'explorer une ville qui n'a pas reçu de dépots de phéromone.
        # Retourne un indice parmis la liste des unexplored
        
        depart = self.explored[-1] 
        sum = 0
        
        # On somme les differente pheromone pour pondérer les probabilités
        for arrival in self.unexplored:
            # On a une proba non nul pour qu'un agent puisse explorer une ville jamais exploré par les autres agents controllé par le parametre Y
            sum += self.null_prob \
                + mat_pheromone[depart][arrival] ** self.pheromone_influence \
                + 1/mat_cost[depart][arrival] ** self.distance_influence # ηij la visibilité, qui est égale à l’inverse de la distance de deux villes i et j 
        
        # random qui decide de la prochaine ville à explorer
        r = random() *  sum
        s = 0 
        # Recherche de la ville qui vient d'être choisit
        for i, arrival in enumerate(self.unexplored): 
            s += self.null_prob \
                + mat_pheromone[depart][arrival] ** self.pheromone_influence \
                + 1/mat_cost[depart][arrival] ** self.distance_influence
            
            # On s'arrette lorsque l'on a trouvé la prochaine ville, et on retourne son indice dans unexplored
            if s >= r:
                return i
            
    def explore(self, mat_cost, mat_pheromone):
        # Tant qu'on a pas tout exploré
        while len(self.unexplored) > 0:
            # On choisit la prochaine destination parmis ceux qui reste à explorer 
            next_i = self.choose_next_location(mat_cost, mat_pheromone) 
            curr_node = self.unexplored.pop(next_i)
            self.explored.append(curr_node)
            
        # Une fois la tournée terminé, l'agent dépose les phéromones
        self.deposite_pheromone(mat_cost, mat_pheromone)
        # On reset les villes explorer pour pouvoir recommencer l'exploration 
        self.reset_exploration(self.explored)
                
            
            
def evaporation(mat_pheromone, disipation_rate):
    for i in range(len(mat_pheromone)):
        for j in range(len(mat_pheromone[0])):
            if mat_pheromone[i][j] > 0:
                mat_pheromone[i][j] -= disipation_rate
                
def index_max(arr, exclude_indices): # retourne l'indice dont la valeur est maximal, et qui n'est pas dans exclude_indices   
    # On n'explore pas a partir du premier, au cas où l'élément 0 fait partir de exclude_indices
    best_i = None 
    for i in range(len(arr)): 
        if best_i == None:
            if i not in exclude_indices: 
                best_i = i
            continue 
        
        if arr[best_i] < arr[i] and i not in exclude_indices:
            best_i = i
            
    return best_i

def find_best(mat_pheromone): # Trouve le chemin le plus parcourus
    path = [0] # On démart à 0, car on cherche un cycle hamiltonien, donc le meilleur circuit passera forcement par cette ville, indépendament de l'ordre.
    # Pour chaque ville
    for _ in range(1, len(mat_pheromone)):
        depart = path[-1]
        arrival = index_max(mat_pheromone[depart], path)
        path.append(arrival)
    return path


def algo_fourmis(mat_cost, time_max=100, verbal=False): 
    """
    time_max : Nombre de cycle max
    """
    size = len(mat_cost)
    ###### Paramètres ###### 
    agents_number = 10 # Nombre d'agents qui parcours la matrice d'adjacence
    disipation_rate = 0.01 # Taux de dissipation par cycle
    deposit_Q = 1 # Parametre qui influ le taux de phéromones déposé par les agents
    prob_explore_Y = 0.1 # Probabilité non-nul d'explorer une ville inexploré
    pheromone_influence = 4 # Influence des phéromones sur la decision de la prochaine ville que visite l'agent
    distance_influence = 2 # Influence du coût de l'arrête sur la decision de la prochaine ville que visite l'agent

    mat_pheromone = np.zeros((size, size)) # Les phéromones sont placés sur les arrêtes
    agents = [Agent(list(range(size)), deposit_Q, prob_explore_Y, pheromone_influence, distance_influence) for _ in range(agents_number)]
    
    if verbal: 
        print("Matrice d'adjacence:")
        print(mat_cost)
            
    for i in range(time_max):
        # On avance chaque agents dans leurs exploration
        for agent in agents:
            agent.explore(mat_cost, mat_pheromone) # Un agent avance d'un noeud
        # On évapore les phéromones a chaque fin d'itération
        evaporation(mat_pheromone, disipation_rate)
        
        if verbal:
            print("iteration: ", i, ", meilleurs chemins:", get_path_cost(mat_cost, find_best(mat_pheromone)) )
    
    best_path = find_best(mat_pheromone) 
    best_cost = get_path_cost(mat_cost, best_path)
    if verbal:
        print("Meilleur chemin: ", best_path)
        print("Cout: ", best_cost)
    return best_path, best_cost
    