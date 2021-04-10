import matplotlib.pyplot as plt
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp


def print_execution_time(catalog):

    
    times=catalog["times"]
    iterator=lt.iterator(times)
    fig1 = plt.figure("Tiempo y memoria de ejecución distintos procesos")
    fig1.subplots_adjust(hspace=0.7, wspace=0.7)


    list_names=[]#t.newList()
    list_times=[]#lt.newList()
    list_memory=[]#lt.newList()

    for info in iterator:
        label=info["label"]
        time=info["time"]
        memory=info["memory"]

        list_names.append(label)
        list_times.append(time)
        list_memory.append(memory)

    # TODO arreglar con lt
    """
    lt.addLast(list_names,label)
    lt.addLast(list_times,time)
    lt.addLast(list_memory,memory)   


    iterator1=lt.iterator(list_names)
    iterator2=lt.iterator(list_times)
    iterator3=lt.iterator(list_memory)

    tupla_names=(i for i in iterator1)
    tupla_times=(i for i in iterator2)
    tupla_memory=(i for i in iterator3)"""

    width=0.35 #tamaño barra 
    ax = fig1.add_subplot(1, 2, 1)
    ax.bar(list_names,list_times,width)
    ax.set_xlabel("s")
    ax.set_ylabel("Time")
    ax.set_title("Times of execution")
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
    # Pintar los ejes pasando por (0,0)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xticks(list_names)
    ax.legend()

    ax = fig1.add_subplot(1, 2, 2)
    ax.bar(list_names,list_memory,width)
    ax.set_xlabel("kb")
    ax.set_ylabel("Memory")
    ax.set_title("Memory of execution")
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
    # Pintar los ejes pasando por (0,0)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.legend()
    ax.set_xticks(list_names)


  
  



        

    plt.show()




lista={'first': {'info': {'label': 'Tiempo-memoria de carga', 'time': 35719.8498, 'memory': 1156026.3369140625}, 'next': None}, 'last': {'info': {'label': 'Tiempo-memoria de carga', 'time': 35719.8498, 'memory': 1156026.3369140625}, 'next': None}, 'size': 1, 'key': None, 'type': 'SINGLE_LINKED', 'cmpfunction': None}





def secund(times):
    iterator=lt.iterator(times)
    fig1 = plt.figure("Tiempo y memoria de ejecución distintos procesos")
    fig1.subplots_adjust(hspace=0.7, wspace=0.7)


    list_names=[]#t.newList()
    list_times=[]#lt.newList()
    list_memory=[]#lt.newList()

    for info in iterator:
        label=info["label"]
        time=info["time"]
        memory=info["memory"]

        list_names.append(label)
        list_times.append(time)
        list_memory.append(memory)

    # TODO arreglar con lt
    """
    lt.addLast(list_names,label)
    lt.addLast(list_times,time)
    lt.addLast(list_memory,memory)   


    iterator1=lt.iterator(list_names)
    iterator2=lt.iterator(list_times)
    iterator3=lt.iterator(list_memory)

    tupla_names=(i for i in iterator1)
    tupla_times=(i for i in iterator2)
    tupla_memory=(i for i in iterator3)"""

    width=0.35 #tamaño barra 
    ax = fig1.add_subplot(1, 2, 1)
    ax.bar(list_names,list_times,width)
    ax.set_xlabel("s")
    ax.set_ylabel("Time")
    ax.set_title("Times of execution")
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
    # Pintar los ejes pasando por (0,0)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xticks(list_names)
    ax.legend()


    # segundo subplot 

    ax = fig1.add_subplot(1, 2, 2)
    ax.bar(list_names,list_memory,width)
    ax.set_xlabel("kb")
    ax.set_ylabel("Memory")
    ax.set_title("Memory of execution")
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
    # Pintar los ejes pasando por (0,0)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.legend()
    ax.set_xticks(list_names)


  
  



        

    plt.show()

#secund(lista)