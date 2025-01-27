﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import time
import tracemalloc
import config as cf
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de videos
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    # TODO: modificaciones para medir el tiempo y memoria
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadCategories(catalog)
    loadVideos(catalog)
    
  


    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    addTime(catalog,delta_time,delta_memory,"carga")
    return delta_time, delta_memory



def loadVideos(catalog):
    """
    Carga los videos del archivo.  Por cada video se indica al
    modelo que debe adicionarlo al catalogo.
    """
    videosfile = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)

def loadCategories(catalog):
    """
    Carga todos las categorias del archivo e indica al modelo
    que los adicione al catalogo
    """
    categoriesfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(categoriesfile, encoding='utf-8'), delimiter='\t')
    for category in input_file:
        model.addCategory(catalog, category)

# Funciones de tiempo-model

def addTime(catalog,time,memory, label):
    return model.addTime(catalog,time,memory,label)


# Funciones de validación

def validateCategory(requested_category, catalog):

    return model.validateCategory(requested_category, catalog)


def validateCountry(requested_country, catalog):

    return model.validateCountry(requested_country, catalog)


#Funciones para mostrar la información 

def req1Format(catalog):

    return model.req1Format(catalog)

def req2Format(catalog, days):

    return model.req2Format(catalog, days)

def req3Format(catalog, days):

    return model.req3Format(catalog, days)

def req4Format(catalog, n_sample):

    return model.req4Format(catalog, n_sample)
 #-------------------------------------------------------------------

# Funciones de consulta sobre el catálogo
def videosSize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.videosSize(catalog)


def countriesSize(catalog):
    """
    Numero de paises cargados al catalogo
    """
    return model.countriesSize(catalog)


def categoriesSize(catalog):
    """
    Numero de categorías cargados al catalogo
    """
    return model.categoriesSize(catalog)


# ======================================
# Funciones para ejecutar requerimientos
# ====================================

def execute_req1(catalog, req_category, req_country, n_sample):
    """Ejecuta el requerimiento 1"""
    
    start=start_functions()
    filter_catalog= model.execute_req1(catalog, req_category, req_country, n_sample)
    finish=finish_functions()
    calculus_of_memorytime(catalog, start, finish, "Req1")
    return filter_catalog

def execute_req2(catalog, req_country):
    """Ejecuta el requerimiento 2"""
    start=start_functions()
    filter_catalog=model.execute_req2(catalog, req_country)
    finish=finish_functions()
    calculus_of_memorytime(catalog, start, finish, "Req2")
    return filter_catalog


def execute_req3(catalog, req_category):
    """Ejecuta el requerimiento 3"""
    start=start_functions()
    filter_catalog=model.execute_req3(catalog, req_category)
    finish=finish_functions()
    calculus_of_memorytime(catalog, start, finish, "Req3")
    return  filter_catalog

def execute_req4(catalog, req_country ,req_tag, n_sample):
    """Ejecuta el requerimiento 4"""
    start=start_functions()
    filter_catalog =  model.execute_req4(catalog, req_country ,req_tag, n_sample)
    finish=finish_functions()
    calculus_of_memorytime(catalog, start, finish, "Req4")

    return filter_catalog

# ======================================
# Funciones para medir tiempo y memoria
# ======================================

def start_functions():
    # Funciones de tiempo para las graficas
    delta_time=-1.0
    delta_memory=-1.0
    tracemalloc.start()
    start_time=getTime()
    start_memory=getMemory()
    return  start_time, start_memory

def finish_functions():
    stop_time=getTime()
    stop_memory=getMemory()
    tracemalloc.stop()
    return stop_time, stop_memory

def calculus_of_memorytime(catalog,start:tuple, finish:tuple, label):
    delta_time=finish[0]-start[0]
    delta_memory=deltaMemory(start[1], finish[1])
    
    print(delta_time,delta_memory)
    addTime(catalog,delta_time,delta_memory,label)

    return catalog

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory