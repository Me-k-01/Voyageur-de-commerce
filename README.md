# Voyageur-de-commerce

## Description du projet

Le projet à pour but d'impléménter deux algorithmes permettant la résolution du problème du voyageur de commerce. Le parcours à été implémentés de deux manières : par aglorithme génétique et par algorithme de colonie de fourmis.


## Pour lancer le programme
Exécuter le fichier python "test.py" pour lancer les deux algorithmes sur le fichier "mat_adjacence.txt".
```python3 test.py```

## Descriptif de test.py

Le fichier test.py a pour but de ressortir le chemin et la valeur la plus courte des deux algorithmes. Cela va ainsi permettre de comparer la précisions de nos deux algorithmes pour un même graphe.
De plus, il est possible de passer un fichier qui va contenir la distance entre les points et ainsi construire la matrice d'adjacence.
Par exemple, pour la matrice d'adjacence donné dans le fichier "mat_adjacence", le graphe ressemblera à ceci:

![Visualisation du graphe](graphe.png)

Le circuit en rouge est le chemin optimal. Il est important de noter que le programme ne renvoie pas d'image et que ce visuel est juste là pour servir d'exemple et pouvoir être comparer avec les résultats obtenus par les deux types d'algorithmes.

## Descriptif du benchmark

Une autre manière de visualiser les performances de nos algorithmes est d'utiliser le fichier "benchmark.ipynb" qui va en plus de nous donner la précision de nos deux algorithmes comparée au chemin optimal, va nous donner les temps d'exécution sur differentes nombre de ville. 
> Exemple de resultat que retournera le benchmark :

![Visualisation du rendu du benchmark](benchmark_10_indiv.png)

