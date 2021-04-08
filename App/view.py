"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

# ===================================
# Funciones de inicializacion
# ===================================


def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en el catalogo
    """
    return controller.loadData(catalog)

#Funciones para solicitar información al usuario

def request_category(catalog):

    """Le pregunta al usuario bajo que categoría desea filtrar los algoritmos."""

    requested_category = input("Ingrese el nombre de la categoria con la que desea filtrar sus datos: ")
    requested_category = " " + requested_category

    if not controller.validateCategory(requested_category, catalog):
        
        print("La categoría ingresada no existe. Intente de nuevo.")
        return request_category(catalog)

    return requested_category


def request_country(catalog):

    """Le pregunta al usuario bajo que país desea filtrar los algoritmos."""

    requested_country = input("Ingrese el nombre del país con el que desea filtrar sus datos: ")

    if not controller.validateCountry(requested_country, catalog):
            
            print("El país ingresado no existe. Intente de nuevo.")
            return request_country(catalog)

    return requested_country


def request_nsample():

    """Le pregunta al usuario respecto al tamaño de la muestra sobre la que se desea aplicar una función."""

    n_sample = input("Ingrese el tamaño de la muestra sobre la que desea indagar (recuerde que este no debe exceder la cantidad de videos en el catálogo): ")
    
    try:
        n_sample = int(n_sample) 

    except Exception:
        print("No ha ingresado un valor numérico. Intentelo de nuevo.")
        return request_nsample()

    return n_sample

#Funciones para ejecutar requerimientos

def execute_req1(catalog, req_category, req_country, n_sample):
    """Ejecuta el requerimiento 1"""
    return controller.execute_req1(catalog, req_category, req_country, n_sample)

def execute_req2(catalog, req_country):
    """Ejecuta el requerimiento 2"""
    return controller.execute_req2(catalog, req_country)



#Funciones para imprimir requerimientos

def req1Print(catalog):
    
    print(controller.req1Format(catalog))

def req2Print(catalog, days):
    
    print(controller.req2Format(catalog, days))

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Videos tendencia con más views (país y categoría)")
    print("4- Video que ha permanecido más dias en tendencia (país)")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:

        print("Cargando información de los archivos ....")
        catalog = initCatalog()

    elif int(inputs[0]) == 2:

        print("Cargando información de los archivos ....")
        answer = loadData(catalog)

        print('Videos cargados: ' + str(controller.videosSize(catalog)))
        print('Paises cargados: ' + str(controller.countriesSize(catalog)))
        print('Categorias cargadas: ' + str(controller.categoriesSize(catalog)))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")

    
    elif int(inputs[0]) == 3:

        req_category = request_category(catalog)
        req_country = request_country(catalog)
        n_sample = request_nsample()
        
        req1_catalog = execute_req1(catalog, req_category, req_country, n_sample)
        
        req1Print(req1_catalog)

    elif int(inputs[0]) == 4:

        req_country = request_country(catalog)

        req2_catalog = execute_req2(catalog, req_country)

        req2Print(req2_catalog[0], req2_catalog[1])

    else:
        sys.exit(0)

sys.exit(0)
