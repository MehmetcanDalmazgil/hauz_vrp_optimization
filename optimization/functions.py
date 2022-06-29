import warnings
import numpy as np
import pandas as pd
import osmnx as ox
import networkx as nx
import sys

sys.path.insert(0, "/optimization/src/pyVRP.py")
from optimization.src.pyVRP import  build_coordinates, build_distance_matrix, genetic_algorithm_vrp, plot_tour_coordinates

def get_maps():
    # Daha önce indilirilmişse harita bilgilerini çekiyoruz.
    try:
        G = ox.load_graphml('optimization/nilufer.graphml')
        print('Nilüfer bölgesi için kaydedilen harita bilgisi okundu ve graf oluşturuldu.')
    except:
        place = "Nilüfer,Bursa,Turkey"
        G = ox.graph_from_place(place, network_type="drive")
        ox.save_graphml(G, filepath='nilufer.graphml')
        print("Nilüfer bölgesi için graf kaydedildi.")
        G = ox.load_graphml('nilufer.graphml')
        print('Nilüfer bölgesi için kaydedilen harita bilgisi okundu ve graf oluşturuldu.')
    
    return G

def set_order_id(order_id):
    order_id.insert(0,0)
    order_id.insert(len(order_id),0)
    return order_id

def show_request(fleet_size, capacity, coordinates):
    print("***************Request***************")
    print(f"fleet_size = {fleet_size}")
    print(f"capacity = {capacity}")
    print(f"coordinates = {coordinates}")
    print("*************************************")

def add_base_coordinates(coordinates):
    base = [[40.22318, 28.85092]]
    address = base + coordinates
    return address

def create_distance_matrix(address):
    G = get_maps()
    distance_matrix = []
    warnings.filterwarnings('ignore')
    for i in range(len(address)):
        baslangic = address[i]
        gecici_matrix = []
        for j in range(len(address)):
            if address[i][0] == address[j][0] and address[i][1] == address[j][1]:
                gecici_matrix.append(0.0)
            else:
                orig = ox.get_nearest_node(G, (address[i][0], address[i][1]))
                dest = ox.get_nearest_node(G, (address[j][0], address[j][1]))
                route = ox.shortest_path(G, orig, dest, weight="length")
                sonuc = sum(ox.utils_graph.get_route_edge_attributes(G, route, "length"))
                gecici_matrix.append(sonuc)
        distance_matrix.append(gecici_matrix)
    distance_matrix = np.array(distance_matrix)

    return distance_matrix

def saved_csv_distance_matrix(distance_matrix, order_id):
    print("**************Mesafe Matrisi Oluşturma************")
    df = pd.DataFrame(distance_matrix, columns =order_id[0:-1])
    print('Distance matrix oluşturuldu ve kaydedildi.')
    df.to_csv(r'distance_matrix.csv', index = False)
    print("*************************************")

def read_to_csv_distance_matrix():
    print("**************Dosya Okuma************")
    print('Distance matrix dosyadan okundu.')
    df = pd.read_csv('distance_matrix.csv')
    vals = df.values
    distance_matrix = vals.tolist()
    distance_matrix = np.array(distance_matrix)
    print("*************************************")
    return distance_matrix


def test_optimization(coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity,vehicle_types, n_depots, route, model, time_window, fleet_size, graph):

    mutation_list = [0.10,0.40,0.70]
    crossover_list = [0.20,0.50,0.80]
    population_size_list = [15,25,40,75]
    generations_list = [10,100,200]
    elitizm_list = [1,2,4]

    for mutation_rate in mutation_list:
        for population_size in population_size_list:
            for generations in generations_list:
                for elitizm in elitizm_list:
                    penalty_value   = 1000    # GA Target Function Penalty Value for Violating the Problem Constraints
                    population_size = population_size  # GA Population Size
                    mutation_rate   = mutation_rate            # GA Mutation Rate
                    elite           = elitizm                # GA Elite Member(s) - Total Number of Best Individual(s) that (is)are Maintained 
                    generations     = generations      # GA Number of Generations

                    # print("**************Optimization***********")
                    ga_report, ga_vrp,distance,time = genetic_algorithm_vrp(coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph)
                    # print("*************************************")
                    with open("sonuclar.txt", "a") as f:
                        f.write(f"{population_size},{mutation_rate},{elite},{generations},{time},{distance}" + "\n")
                    print(f"Sonuç: {distance}, Population: {population_size},Mutation: {mutation_rate},Elitizm:{elite},Generations: {generations},Time:{time}")
                    print("*************************************")
    return {"result":"test işlemi tamamlandı"}


def multiple_optimization(order_id, coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph):

    result = []
    for i in range(0,10):
        print("**************Optimization***********")
        ga_report, ga_vrp,cost = genetic_algorithm_vrp(coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph)
        print("*************************************")
        
        response_routes = []
        hesaplama_routes = []
        result.append(cost)
        print("***************Paths*****************")
        for j in range(0,len(ga_vrp[1])):
            nodes = ga_vrp[1][j].copy()
            nodes.insert(0,0)
            nodes.insert(len(nodes),0)
            # print(nodes)
            # print("--------------------------")
            fleet_routes = []
            for index, k in enumerate(nodes):
                fleet_routes.append(order_id[k])
                response_routes.append({"id": order_id[k], "carrierNumber": j+1, "queueNumber": index  })
            print(f"{j+1}.fleet: {fleet_routes}")
            hesaplama_routes.append(fleet_routes)
        print("*************************************")
    print("****************Result***************")
    for idx, x in enumerate(result):
        print(f"{idx+1}.sonuç = {x}")
    result.sort()
    print(f"Optimum = {result[0]}")
    print("*************************************")
    print(hesaplama_routes)

    return response_routes

def single_optimization(order_id, coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph):

    print("**************Optimization***********")
    ga_report, ga_vrp,cost,time = genetic_algorithm_vrp(coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph)
    print("*************************************")
    response_routes = []
    print("***************Paths*****************")
    for j in range(0,len(ga_vrp[1])):
        nodes = ga_vrp[1][j].copy()
        nodes.insert(0,0)
        nodes.insert(len(nodes),0)
        # print(nodes)
        # print("--------------------------")
        fleet_routes = []
        for index, k in enumerate(nodes):
            # fleet_size.append([order_id[k],address[k][0],address[k][1]])
            fleet_routes.append(order_id[k])
            response_routes.append({"id": order_id[k], "carrierNumber": j+1, "queueNumber": index  })
        # print(f"{j+1}.fleet: {response_routes}")
        # print("--------------------------")
        print(f"{j+1}.fleet: {fleet_routes}")
    print("*************************************")
    print("****************Time*****************")
    print(f"Runtime: {time} seconds")
    print("*************************************")
    # print(response_routes)

    # response = {}
    # for x in range(0,len(ga_vrp[1])):
    #     response[f"{x+1}"] = response_routes[x]
        # print(f"{x}: {response_routes[x][0]}")
    
    return response_routes

