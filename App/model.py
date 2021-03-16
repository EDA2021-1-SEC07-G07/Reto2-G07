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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(list_type = "ARRAY_LIST"):
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    videos
    category_id
    country

    Retorna el catalogo inicializado.
    """

    catalog = {'videos': None,
            'category_id': None}


    """
    Esta lista contiene todo los videos encontrados
    en los archivos de carga.  Estos videos no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('SINGLE_LINKED', compareVideoIds)

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los videos de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el identificador del videos
    """
    catalog['category_id'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCategoryIds)

    return catalog


# Funciones para agregar informacion al catalogo
def addVideo(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos.
    """
    lt.addLast(catalog['videos'], video)
    #mp.put(catalog['category_id'], video['category_id'], video)


def addCategoryId(catalog, category_id, video):
    """
    Esta función adiciona un video a la lista de videos
    relacionados a una categoría.
    """
    categories_ids = catalog['category_id']
    existcategory = mp.contains(categories_ids, category_id)
    
    if existcategory:
        entry = mp.get(categories_ids, category_id)
        category_data = me.getValue(entry)
    else:
        category_data = newCategory(category_id)
        mp.put(categories_ids, category_id, category_data)
    lt.addLast(category_data['videos'], video)
    totvideos = lt.size(category_data['videos'])

    category_data["size"] = totvideos

# Funciones para creacion de datos

def newCategory(category_id):
    """
    Crea una nueva estructura para modelar las categorias.
    """
    category = {'category_id': "",
              "videos": None,
              "size": 0}

    category['category_id'] = category_id
    category['videos'] = lt.newList('SINGLE_LINKED', compareCategoryIds)
    return category

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareVideoIds(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1



def compareCategoryIds(id, category):
    catentry = me.getKey(category)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return 0


# Funciones de ordenamiento
