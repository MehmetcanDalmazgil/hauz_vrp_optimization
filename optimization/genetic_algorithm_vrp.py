import numpy as np
import pandas as pd
import os

import sys
sys.path.insert(0, "/optimization/src/pyVRP.py")
from optimization.src.pyVRP import  build_coordinates, build_distance_matrix, genetic_algorithm_vrp, plot_tour_coordinates
from optimization.functions import *

def path(fleet_size, capacity, coordinates, order_id):

    ############################################################################
    order_id = set_order_id(order_id)
    show_request(fleet_size, capacity, coordinates)
    address = add_base_coordinates(coordinates)
    
    # if os.stat("distance_matrix.csv").st_size == 0:
    #     distance_matrix = create_distance_matrix(address)
    #     saved_csv_distance_matrix(distance_matrix,order_id)
    # else:
    #     distance_matrix = read_to_csv_distance_matrix()

    print("Başladı")
    distance_matrix = create_distance_matrix(address)
    print("Distance oluşturuldu")

    coordinates     = build_coordinates(distance_matrix)
    parameters      = pd.read_csv('optimization/VRP-01-Parameters.txt', sep = '\t') 
    parameters      = parameters.values

    ############################################################################

    if(len(capacity) == 1):
        # Model Parametreleri
        n_depots    =  1           # mesafe matrisinin ilk n satırı depo olarak kabul edilmektedir.
        time_window = 'without'    # zaman maliyeti hesaba katılacak mı ?
        route       = 'closed'     # açık rota mı kapalı rota mı ?
        model       = 'vrp'        # hangi model kullanılacak ?
        graph       = False        # default değer

        # Araç Parametreleri
        vehicle_types =   1        # Araç tipi sayısı
        fixed_cost    = [ 0 ]      # Sabit maliye ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
        variable_cost = [ 1 ]      # Değişken maliyet  ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
        capacity      = capacity   # Araç kapasitesi 
        velocity      = [ 1 ]      # Mesafe matrisini bölen bir sabit. ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
        fleet_size    = fleet_size # Mevcut araç sayısı

        # GA Parametreleri
        penalty_value   = 1000    # GA Target Function Penalty Value for Violating the Problem Constraints
        population_size = len(address) * 2      # GA Population Size
        mutation_rate   = 0.10    # GA Mutation Rate
        elite           = 2     # GA Elite Member(s) - Total Number of Best Individual(s) that (is)are Maintained 
        generations     = 200       # GA Number of Generations   

    else:
        # Model Parametreleri
        n_depots    =  1           # mesafe matrisinin ilk n satırı depo olarak kabul edilmektedir.
        time_window = 'without'    # zaman maliyeti hesaba katılacak mı ?
        route       = 'closed'     # açık rota mı kapalı rota mı ?
        model       = 'vrp'        # hangi model kullanılacak ?
        graph       = False        # default değer

        # Araç Parametreleri
        vehicle_types = len(capacity)                           # Araç tipi sayısı
        fixed_cost    = capacity                                # Sabit maliye ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
        variable_cost = list(map(lambda x: int(x/2), capacity)) # Değişken maliyet  ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
        capacity      = capacity                                # Araç kapasitesi 
        velocity      = [ 1,1 ]                                 # Mesafe matrisini bölen bir sabit. ! Sadece birden fazla araç tipi varsa bu değer değişmektedir.
        fleet_size    = fleet_size                              # Mevcut araç sayısı

        # GA Parametreleri
        penalty_value   = 1000    # GA Target Function Penalty Value for Violating the Problem Constraints
        population_size = len(address) * 2      # GA Population Size
        mutation_rate   = 0.10    # GA Mutation Rate
        elite           = 2     # GA Elite Member(s) - Total Number of Best Individual(s) that (is)are Maintained 
        generations     = 200       # GA Number of Generations
    
    ############################################################################

    # response_routes = test_optimization(coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity,vehicle_types, n_depots, route, model, time_window, fleet_size, graph)

    ############################################################################

    # response_routes = multiple_optimization(order_id, coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph)

    ############################################################################

    response_routes = single_optimization(order_id, coordinates, distance_matrix, parameters, velocity, fixed_cost, variable_cost, capacity, population_size, vehicle_types, n_depots, route, model, time_window, fleet_size, mutation_rate, elite, generations, penalty_value, graph)
    
    ############################################################################

    return response_routes