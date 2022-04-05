from email.mime import base
import numpy as np
import osmnx as ox
import networkx as nx

#İşlem zaman alıyor, daha önce indirilmişse tekrar indirilmesin.
try:
    G = ox.load_graphml('optimization/nilufer.graphml')
    print('Nilüfer bölgesi için kaydedilen harita bilgisi okundu ve graf oluşturuldu.')
except:
    place = "Nilüfer,Bursa,Turkey"
    G = ox.graph_from_place(place, network_type="drive")
    ox.save_graphml(G, filepath='gorukle.graphml')
    print("Nilüfer bölgesi için graf kaydedildi.")
    G = ox.load_graphml('nilufer.graphml')
    print('Nilüfer bölgesi için kaydedilen harita bilgisi okundu ve graf oluşturuldu.')

def path(fleet_size, capacity, coordinates):
    base = [[40.22318, 28.85092]]
    address = base + coordinates
    print(address)
    distance_matrix = []

    import warnings
    warnings.filterwarnings('ignore')
    for i in range(len(address)):
        baslangic = address[i]
        gecici_matrix = []
        for j in range(len(address)):
            if address[i][0] == address[j][0] and address[i][1] == address[j][1]:
                gecici_matrix.append(0.0)
            else:
                orig = ox.get_nearest_node(G, (address[i][0], address[i][1]))
                # print(f"Başlangıç(origin) = {orig}")
                dest = ox.get_nearest_node(G, (address[j][0], address[j][1]))
                # print(f"Başlangıç ={address[i][0], address[i][1]}")
                # print(f"Hedef ={address[j][0], address[j][1]}")
                # print(f"i:{i} j:{j}")
                # print(f"----------------------------------")
                # print(f"Hedef(destination) = {dest}")
                route = ox.shortest_path(G, orig, dest, weight="length")
                # route = int(nx.shortest_path_length(G, orig, dest, weight='length', method='dijkstra'))
                sonuc = sum(ox.utils_graph.get_route_edge_attributes(G, route, "length"))
                gecici_matrix.append(sonuc)
        distance_matrix.append(gecici_matrix)

    distance_matrix = np.array(distance_matrix)

    ############################################################################

    # Required Libraries
    import pandas as pd
    import sys
    sys.path.insert(0, "/optimization/src/pyVRP.py")
    from optimization.src.pyVRP import  build_coordinates, build_distance_matrix, genetic_algorithm_vrp, plot_tour_coordinates

    ######################## EXAMPLE - 01 ####################################

    # Load Dataset Case 1 - Distance Matrix (YES); Coordinates (NO)
    coordinates     = build_coordinates(distance_matrix)
    parameters      = pd.read_csv('optimization/VRP-01-Parameters.txt', sep = '\t') 
    parameters      = parameters.values

    # Model Parametreleri
    n_depots    =  1           # mesafe matrisinin ilk n satırı depo olarak kabul edilmektedir.
    time_window = 'without'    # zaman maliyeti hesaba katılacak mı ?
    route       = 'closed'     # açık rota mı kapalı rota mı ?
    model       = 'vrp'        # hangi model kullanılacak ?
    graph       = False        # default değer

    # Araç Parametreleri
    vehicle_types =   1        # Araç tipi sayısı
    fixed_cost    = [ 0 ]     # Sabit maliye ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
    variable_cost = [ 1 ]     # Değişken maliyet  ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
    capacity      = [ 5 ]     # Araç kapasitesi 
    velocity      = [ 1 ]     # Mesafe matrisini bölen bir sabit. ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
    fleet_size    = [ 4 ]     # Mevcut araç sayısı

    # GA Parametreleri
    penalty_value   = 1000     # GA Target Function Penalty Value for Violating the Problem Constraints
    population_size = 75       # GA Population Size
    mutation_rate   = 0.10     # GA Mutation Rate
    elite           = 1        # GA Elite Member(s) - Total Number of Best Individual(s) that (is)are Maintained 
    generations     = 10     # GA Number of Generations

    ga_report, ga_vrp = genetic_algorithm_vrp(coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph)
    
    routes = []

    for j in range(0,len(ga_vrp[1])):
        nodes = ga_vrp[1][j].copy()
        nodes.insert(0,0)
        nodes.insert(len(nodes),0)
        print(nodes)
        print("--------------------------")
        fleet_path = []
        for k in nodes:
            fleet_path.append([k,address[k][0],address[k][1]])
        routes.append(fleet_path)
        print(routes)

    response = {}
    for x in range(0,len(ga_vrp[1])):
        response[f"{x+1}"] = routes[x]
    
    return response
        

"""
def path(fleet_size, capacity, coordinates):
    return {"response":f"filo sayısı = {fleet_size}, kapasitesi = {capacity}, adresler = {coordinates}"}
"""
