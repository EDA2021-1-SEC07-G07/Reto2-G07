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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Cargar información de los videos en el catálogo")
    print("2- Videos en tendencia con más likes (Categoría)")

def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)


def filterCategory(catalog):
    """Le pregunta al usuario bajo que categoría desea filtrar los algoritmos."""


    selected_category = input("Ingrese el nombre de la categoria con la que desea filtrar sus datos: ")
    selected_category = " "+ selected_category

    if mp.contains(catalog["category_id"], selected_category):

            return selected_category

    print("Este no es el nombre de una categoría existente. Intente de nuevo.")
    return filterCategory(catalog)

def sortVideos(catalog, size, cmpFunction):
    """
    Organiza los videos mediante Merge Sort
    """
    return controller.sortVideos(catalog, size, cmpFunction)

def askSampleList(catalog, size):
    """Le pregunta al usuario respecto al tamaño de la muestra sobre la que se desea aplicar una función."""

    n_sample = input("Ingrese el tamaño de la muestra sobre la que desea indagar (recuerde que este no debe exceder la cantidad de videos en el catálogo): ")
    try:
        if int(n_sample) > int(size):
            
            print("El número de muestra ha superado el tamaño de la lista, se procederá con la cantidad máxima de videos dentro del catálogo: {}".format(lt.size(catalog['videos'])))

            n_sample = size-1
            
        return int(n_sample)


    except Exception:
        return askSampleList(catalog, size)


def printResultsReq1(video_list, n_sample, size):
    """Función netamente de la view encargada de imprimir los datos del requerimiento 1."""
    
    if size > n_sample:
        for i in range(n_sample):
            a="trending_date"
            b="title"
            c = "channel_title"
            d = "publish_time"
            e = "views"
            f = "likes"
            g = "dislikes"
            
            
            video = lt.getElement(video_list, i+1)
            names_categories=[a,b,c,d,e,f,g]

            trending_date=video[a]
            title=video[b]
            cannel_title=video[c]
            publish_time= video[d]
            views=video[e]
            likes= video[f]
            dislikes=video[g]



            categories=[trending_date,title,cannel_title,publish_time, views,likes,dislikes]
            max_size=80 #tamaño de impresion 
            upper="-"*(max_size+18)+"\n"
            text=upper+"|{}|\n".format(("VIDEO "+str(i+1)).center(max_size+16))+upper
            #size_var=max_size+17

            for j in range(len(categories)):
                a=str(names_categories[j]).center(15)
                b=str(categories[j]).center(max_size)
                value="|{}|{}|\n".format(a,b)
                text+=value
                text+=upper                    
            text+="\n"*5
            print(text)

def MainMenu():
    """Menu Principal de la aplicación."""

    try:
        while True:
            printMenu()
            inputs = input('Seleccione una opción para continuar\n')
            if int(inputs[0]) == 1:

                print("Cargando información de los archivos ....\n") 
                catalog = initCatalog()
                loadData(catalog)

                print("Catalogo cargado exitosamente!")


            elif int(inputs[0]) == 2:
                
                selected_category = filterCategory(catalog)
                videos_by_category = catalog["category_id"]

                selected_category_dict = mp.get(videos_by_category, selected_category)
                selected_info = me.getValue(selected_category_dict)

                sorted_videos = sortVideos(selected_info, selected_info["size"], "sortByLikes")
                
                
                n_sample = askSampleList(selected_info, selected_info["size"])


                printResultsReq1(sorted_videos[1], n_sample, selected_info["size"])

            elif int(inputs[0]) == 0:


            
                sys.exit(0)

    except Exception:
        print("No ha cargado la base de datos. Intentelo de nuevo.")
        MainMenu()
    sys.exit(0)


MainMenu()