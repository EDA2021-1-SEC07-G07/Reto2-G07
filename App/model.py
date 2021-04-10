"""
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
from DISClib.Algorithms.Sorting import mergesort 
import tracemalloc
import time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    ID videos
    Categoría
    Pais
    Tag

    Retorna el catalogo inicializado.
    """
    catalog = {'categories': None,
               'categoriesIds': None,
               'countries': None,
               'tags': None,
               "times":None}


    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el identificador del video
    """

    """
    Este indice crea un map cuya llave es el país del video
    """
    catalog['countries'] = mp.newMap(17,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCountriesByName)
    """
    Este indice crea un map cuya llave es la categoría 
    """
    catalog['categories'] = mp.newMap(47,
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareCategoryNames)
    """
    Este indice crea un map cuya llave es el Id de la categoría
    """
    catalog['categoriesIds'] = mp.newMap(47,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareCategoryIds)

    """
    Este indice crea un map cuya llave es el tag del video
    """
    catalog['tags'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareTagsByName)
    
    catalog['times']=lt.newList()

    return catalog

def newVideoCategory(name, id):
    """
    Esta estructura crea una relación entre un tag y los libros que han sido
    marcados con dicho tag.  Se guarga el total de libros y una lista con
    dichos libros.
    """
    category = {'name': '',
           'category_id': '',
           'videos': None}
    category['name'] = name
    category['category_id'] = id
    category['videos'] = mp.newMap(34500,
                                maptype='CHAINING',
                                loadfactor=2,
                                comparefunction=compareCategoryNames)

    category['unique_videos'] = mp.newMap(3450,
                                maptype='CHAINING',
                                loadfactor=2,
                                comparefunction=compareCategoryNames)
    
    return category

# Funciones de Tiempo en catalogo de

def addTime(catalog,time,memory, label):
    info={
        "label":label,
        "time":time,
        "memory":memory,
    }
    lt.addLast(catalog['times'], info)
# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de paises, una referencia
    al libro.
    """

    country = video['country'] #Se obtiene el país

    category_id = video['category_id'] #Se obtiene el id de la categoria

    entry = mp.get(catalog["categoriesIds"], category_id)
    category_name = me.getValue(entry)

    addVideoCountry(catalog, country.strip(), video)
    addVideoCategory(catalog, category_name, video)
    

def addVideoCountry(catalog, country, video):
    """
    Esta función adiciona un video a la lista de videos de un mismo país.
    """
    countries = catalog['countries']
    existcountry = mp.contains(countries, country)
    if existcountry:
        entry = mp.get(countries, country)
        data = me.getValue(entry)
    else:
        data = newCountry(country)
        mp.put(countries, country, data)
    lt.addLast(data['videos'], video)


    #Filtro automático por video único de cada país
    if not mp.contains(data["unique_videos"], video["title"]):
        mp.put(data["unique_videos"], video["title"], lt.newList('ARRAY_LIST') )
        
        unique_video_entry = mp.get(data["unique_videos"], video["title"])
        unique_video = me.getValue( unique_video_entry)

        lt.addLast(unique_video, video)
        lt.addLast(unique_video, 1)

    else:
        unique_video_entry = mp.get(data["unique_videos"], video["title"])
        unique_video = me.getValue(unique_video_entry)

        current_days = lt.getElement(unique_video, 2)

        lt.changeInfo(unique_video, 2, current_days + 1)



def addVideoCategory(catalog, category_name, video):
    """
    Esta función adiciona un video a la lista de videos de una misma categoría.
    """
    categories = catalog['categories']
    existcategory = mp.contains(categories, category_name)
    if existcategory:
        entry = mp.get(categories, category_name)
        data = me.getValue(entry)
  
    else:
        data = newCategory(category_name)
        mp.put(categories, category_name, data)
    

    #Filtro automático por pais dentro de cada categoría
    if not mp.contains(data["videos"], video["country"]):
        mp.put(data["videos"], video["country"], lt.newList('ARRAY_LIST'))
        

    country_entry = mp.get(data["videos"], video["country"])
    country_list = me.getValue(country_entry)
    lt.addLast(country_list, video)


    #Filtro automático por video único de cada categoría 
    if not mp.contains(data["unique_videos"], video["title"]):
        mp.put(data["unique_videos"], video["title"], lt.newList('ARRAY_LIST') )
        
        unique_video_entry = mp.get(data["unique_videos"], video["title"])
        unique_video = me.getValue( unique_video_entry)

        lt.addLast(unique_video, video)
        lt.addLast(unique_video, 1)

    else:
        unique_video_entry = mp.get(data["unique_videos"], video["title"])
        unique_video = me.getValue(unique_video_entry)

        current_days = lt.getElement(unique_video, 2)

        lt.changeInfo(unique_video, 2, current_days + 1)





def addCategory(catalog, category):
    """
    Adiciona un tag a la tabla de tags dentro del catalogo y se
    actualiza el indice de identificadores del tag.
    """
    newcat = newVideoCategory(category['name'], category['id'])
    mp.put(catalog['categories'], category['name'], newcat)
    mp.put(catalog['categoriesIds'], category['id'], category['name'])
   
# Funciones para creacion de datos
def newCountry(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    country = {'name': "",
              "videos": None}
    country['name'] = name
    country['videos'] = lt.newList('ARRAY_LIST')
    country['unique_videos'] = mp.newMap(3450,
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareCategoryNames)
    return country

def newCategory(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    category = {'name': "",
              "videos": None}
    category['name'] = name
    category['videos'] = mp.newMap(34500,
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareCategoryNames)
    return category


# Funciones de consulta

def videosSize(catalog):
    """
    Número de videos en el catago
    """
    return lt.size(catalog['videos'])


def countriesSize(catalog):
    """
    Numero de paises en el catalogo
    """
    return mp.size(catalog['countries'])


def categoriesSize(catalog):
    """
    Numero de categorías en el catalogo
    """
    return mp.size(catalog['categories'])



# Funciones utilizadas para comparar elementos dentro de una lista

def compareVideoIds(id1, id2):
    """
    Compara dos ids de dos videos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMapVideoIds(id, entry):
    """
    Compara dos ids de videos, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareCountriesByName(keyname, country):
    """
    Compara dos nombres de país. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(country)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareCategoriesByName(keyname, category_name):
    """
    Compara dos nombres de categoria. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(category_name)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareCategoryNames(name, category):
    catentry = me.getKey(category)
    if (name == catentry):
        return 0
    elif (name > catentry):
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

def compareTagsByName(keyname, tag):
    """
    Compara dos tags de país. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(tag)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los 'views' de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return (float(video1['views']) > float(video2['views']))

def cmpVideosByDays(video1, video2):
    """
    Devuelve verdadero (True) si los 'views' de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor de dias en la posición 0 
    video2: informacion del segundo video que incluye su valor de dias en la posición 0 
    """
    return float(lt.lastElement(video1)) > float(lt.lastElement(video2))


def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los 'LIKES' de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'LIKES'
    video2: informacion del segundo video que incluye su valor 'LIKES'
    """
    return (float(video1["likes"]) > float(video2["likes"]))

# Funciones de ordenamiento
def sortVideos(catalog, size, cmpFunction):
    """Función que organiza una lista mediante Merge Sort. 

    Parametros:
        catalog: Catalogo a organizar
        size: Tamaño del sub-catalogo que será organizado
        cmpFunction: Nombre de la función de comparación a utilizar."""


    if cmpFunction == "sortByViews":
        sub_list = lt.subList(catalog, 1, size)
        sub_list = sub_list.copy()
        start_time = time.process_time()
        sorted_list = mergesort.sort(sub_list, cmpVideosByViews)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        return elapsed_time_mseg, sorted_list

    elif cmpFunction == "sortByDays":
        sub_list = lt.subList(catalog, 1, size)
        sub_list = sub_list.copy()
        start_time = time.process_time()
        sorted_list = mergesort.sort(sub_list, cmpVideosByDays)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        return elapsed_time_mseg, sorted_list

    elif cmpFunction == "sortByLikes":

        sub_list = lt.subList(catalog, 1, size)
        sub_list = sub_list.copy()
        start_time = time.process_time()
        sorted_list = mergesort.sort(sub_list, cmpVideosByLikes)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        return elapsed_time_mseg, sorted_list    

#Funciones de validación 
def validateCategory(requested_category, catalog):

    valid = False

    if mp.contains(catalog["categories"], requested_category):

        valid = True

    return valid


def validateCountry(requested_country, catalog):

    valid = False

    if mp.contains(catalog["countries"], requested_country):

        valid = True

    return valid

def validateNSample(n_sample, catalog):

    if int(n_sample) > lt.size(catalog):
            
        print("El número de muestra ha superado el tamaño de la lista, se procederá con la cantidad máxima de videos dentro del catálogo: {}".format(lt.size(catalog)))

        n_sample = lt.size(catalog)-1

    return n_sample



#Funciones para ejecutar requerimientos

def execute_req1(catalog, req_category, req_country, n_sample):
    """Ejecuta el requerimiento 1"""
    



    filter_category_entry = mp.get(catalog["categories"], req_category)

    filter_category = me.getValue(filter_category_entry)

    filter_country_entry = mp.get(filter_category["videos"], req_country)

    filter_country = me.getValue(filter_country_entry)

    sorted_catalog = sortVideos(filter_country, lt.size(filter_country), "sortByViews")[1]

    n_sample = validateNSample(n_sample, sorted_catalog)

    filter_nsample = lt.subList(sorted_catalog, 1, n_sample)

    return filter_nsample 


def execute_req2(catalog, req_country):
    """Ejecuta el requerimiento 2"""
    

    filter_country_entry = mp.get(catalog["countries"], req_country)

    filter_country_map = me.getValue(filter_country_entry)["unique_videos"]

    filter_country = mp.valueSet(filter_country_map)

    sorted_catalog = sortVideos(filter_country, lt.size(filter_country), "sortByDays")[1]


    filter_first_element = lt.subList(sorted_catalog, 1, 1)


    filter_first_item = lt.getElement(filter_first_element,1)

    filter_first_video = lt.getElement(filter_first_item,1)
    filter_first_day = lt.getElement(filter_first_item,2)

    return (filter_first_video, filter_first_day)

def execute_req3(catalog, req_category):
    """Ejecuta el requerimiento 2"""
    

    filter_category_entry = mp.get(catalog["categories"], req_category)

    filter_category_map = me.getValue(filter_category_entry)["unique_videos"]

    filter_category = mp.valueSet(filter_category_map)

    sorted_catalog = sortVideos(filter_category, lt.size(filter_category), "sortByDays")[1]

    filter_first_element = lt.subList(sorted_catalog, 1, 1)


    filter_first_item = lt.getElement(filter_first_element,1)
    filter_first_video = lt.getElement(filter_first_item,1)
    filter_first_day = lt.getElement(filter_first_item,2)

    return (filter_first_video, filter_first_day)



def execute_req4(catalog, req_country ,req_tag, n_sample):
    """Ejecuta el requerimiento 4"""
    

    filter_country_entry = mp.get(catalog["countries"], req_country)

    filter_country = me.getValue(filter_country_entry)["videos"]

    filter_tag = filterTag(filter_country, req_tag)

    sorted_catalog = sortVideos(filter_tag, lt.size(filter_tag), "sortByLikes")[1]

    n_sample = validateNSample(n_sample, sorted_catalog)

    filter_nsample = lt.subList(sorted_catalog, 1, n_sample)

    return (filter_nsample)


#Funciones de filtrado
def filterTag(catalog, tag):
    """Filtra el catalogo obteniendo uno reducido en el que solo se incluyan los videos que
       contengan el tag especificado."""

    filter_tags = lt.newList("ARRAY_LIST")

    for video in lt.iterator(catalog):

        video_tags=video["tags"]
        
        if tag in video_tags:
            lt.addLast(filter_tags, video)
               
    return filter_tags




#Funciones para mostrar los requerimientos

def req1Format(video_list):

    """Función encargada de darle un formato a la información del requerimiento 1."""

    count = 0
    text = ""

    for video in lt.iterator(video_list):

        count += 1

        a="trending_date"
        b="title"
        c = "channel_title"
        d = "publish_time"
        e = "views"
        f = "likes"
        g = "dislikes"
        
        #TODO CAMBIAR A ARRAYLIST DICCIONARIO
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
        text+=upper+"|{}|\n".format(("VIDEO "+str(count)).center(max_size+16))+upper
        #size_var=max_size+17

        for j in range(len(categories)):
            a=str(names_categories[j]).center(15)
            b=str(categories[j]).center(max_size)
            value="|{}|{}|\n".format(a,b)
            text+=value
            text+=upper                    
        text+="\n"*5

    return text


def req2Format(video, dias):

    """Función netamente de la view encargada de imprimir los datos del requerimiento 2."""
    i=0
    text = ""
    
    a = "title"
    b = "channel_title"
    c = "country"
    d = "Días"
    names_categories=[a,b,c,d]
    title=video[a]
    channel_title=video[b]
    country=video[c]
    
    #TODO CAMBIAR A ARRAYLIST DICCIONARIO
    categories=[title,channel_title,country,dias]
    max_size=80 #tamaño de impresion 
    upper="-"*(max_size+18)+"\n"
    text += upper+"|{}|\n".format(("VIDEO "+str(i+1)).center(max_size+16))+upper

    for j in range(len(categories)):
        a=str(names_categories[j]).center(15)
        b=str(categories[j]).center(max_size)
        value="|{}|{}|\n".format(a,b)
        text+=value
        text+=upper                    
    text+="\n"*3
    i+=1

    return text

def req3Format(video, dias):

    """Función netamente de la view encargada de imprimir los datos del requerimiento 2."""
    i=0
    text = ""
    
    a = "title"
    b = "channel_title"
    c = "category_id"
    d = "Días"
    names_categories=[a,b,c,d]
    title=video[a]
    channel_title=video[b]
    category=video[c]
    
    #TODO CAMBIAR A ARRAYLIST DICCIONARIO
    categories=[title,channel_title,category,dias]
    max_size=80 #tamaño de impresion 
    upper="-"*(max_size+18)+"\n"
    text += upper+"|{}|\n".format(("VIDEO "+str(i+1)).center(max_size+16))+upper

    for j in range(len(categories)):
        a=str(names_categories[j]).center(15)
        b=str(categories[j]).center(max_size)
        value="|{}|{}|\n".format(a,b)
        text+=value
        text+=upper                    
    text+="\n"*3
    i+=1

    return text

def req4Format(list_videos, n_sample):
  
    text = ""

    if lt.size(list_videos) >= 1:
        for i in range(n_sample):
            a = "title"
            b= "channel_title"
            c = "publish_time"
            d="views"
            e = "likes"
            f = "dislikes"
            g="tags"

            names_categories=[a,b,c,d,e,f,g]
            video = lt.getElement(list_videos, i+1)

            title=video[a]
            cannel_title=video[b]
            publish_time= video[c]
            views=video[d]
            likes= video[e]
            dislikes=video[f]
            tags=video[g]


            categories=[title,cannel_title,publish_time, views,likes,dislikes,tags]
            max_size=70

            upper="-"*(max_size+18)+"\n"
            text += upper+"|{}|\n".format(("VIDEO "+str(i+1)).center(max_size+16))+upper
            size_var=max_size+17

            for j in range(len(categories)):
                if j<len(categories)-1:
                    a=str(names_categories[j]).center(15)
                    b=str(categories[j]).center(max_size)
                    value="|{}|{}|\n".format(a,b)
                else:
                    a=str(names_categories[j]).center(size_var-1)
                    value="|{}|\n".format(a)
                    value+=upper
                    categorie=categories[j]
                    
                    tam=len(categorie)//size_var
                    pos=0
                    for k in range(tam+1):
                        final=pos+size_var
                        try:
                            slide=categorie[pos:final]
                        except:
                            slide=categorie[pos:len(cannel_title)-1]
                            slide=slide.center(size_var)
                        value+="|{}|\n".format(slide)
                        
                        pos+=size_var

                    b=str(categories[j]).ljust(max_size)
                    
                text+=value
                text+=upper

            text+="\n"*5

    return text

