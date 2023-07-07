import requests
from flask import render_template, request, jsonify
from urllib.request import urlopen
import pandas as pd
import math
from itertools import permutations
import class_interface as ci
import ip_url


def backtrack(combination,arrays,used_indexes,array_index):
    if len(combination) == len(arrays):
        # la combinazione ha la stessa lunghezza degli array
        #print("Combinazione trovata: ", combination)
        return True
    else:
        for i in range(len(arrays[array_index])):
            if arrays[array_index][i] and i not in used_indexes:
                used_indexes.add(i)
                combination.append(i)
                if backtrack(combination,arrays,used_indexes,array_index + 1):
                    return True
                combination.pop()
                used_indexes.remove(i)
    return False


def find_combination_true(arrays, target_size):
    for perm in permutations(arrays, target_size):
        found = set()
        for array in perm:
            for i, value in enumerate(array):
                if value and i not in found:
                    found.add(i)
                    break
        if len(found) == target_size:
            return perm
    return None


def get_index_result_array(array_lavorazione_robot,result,num_robot_da_cercare):
    indice_result = []
    for i in range(len(result)):
        for j in range(len(array_lavorazione_robot)):
            if array_lavorazione_robot[j] == result[i] and j not in indice_result:
                indice_result.append(j)
                if len(indice_result) == num_robot_da_cercare:
                    return indice_result
                
                

def postdata_lavorazione(indice_robot,robot,lavoro):
    ip = ip_url.get_ip()
    url = 'http://{}/addinlista_lavorazione/{}/{}/{}/{}/{}/{}/{}'.format(ip,indice_robot,robot.temperature,robot.pressure,robot.weight_1,robot.weight_2,robot.weight_3,lavoro)
    x = requests.post(url)
    #print(url)



def sort_by_trues(vector):
    return sum(vector)


def get_data():
    ''' if i>0:
            return '''
    ip = ip_url.get_ip()
    url = 'http://{}/lista_json'.format(ip)  #url mio
    #url = 'http://155.185.80.241/lista'  #url vitto
    data = requests.get(url)
    return data.json()



def parse_componente(df):
    
    component_vector = []
    
    for i in range(len(df)):
        componente = df.loc[i, 'Componente']
        materiale_1 = df.loc[i, 'Materiale_1']
        materiale_2 = df.loc[i, 'Materiale_2']
        materiale_3 = df.loc[i, 'Materiale_3']
        component_vector.append(ci.Componente(componente,materiale_1,materiale_2,materiale_3))
    
    return component_vector
       
 
def parse_materiale(df):
    
    material_vector = []
    
    for i in range(len(df)):
        descrizione = df.loc[i, 'Descrizione']
        peso = df.loc[i, 'Peso']
        material_vector.append(ci.Materiale(descrizione,peso))
    
    return material_vector
    

def parse_prodotto(df,prodotto_descrizione,componenti):
    
    check_exist = False

    oggetti_comp = []
    oggetti_num = []
    
    num_rows = df.shape[0]
    num_colon = df.shape[1] - 1
            
    for i in range(num_rows):
        comp_ = []
        descrizione = df.loc[i,"Prodotto"]
        for j in range(num_colon):
            comp_.append(df.iloc[i,j+1])

        if descrizione == prodotto_descrizione:
            check_exist = True
            for i in range(len(comp_)):
                if  int(comp_[i]) is not 0:  #verifico che il valore sia diverso da 0.0 
                    oggetti_comp.append(ci.Componente(componenti[i].componente,componenti[i].mat_1,componenti[i].mat_2,componenti[i].mat_3))
                    oggetti_num.append(int(comp_[i]))        
            prodotto_data = ci.Prodotto(descrizione,oggetti_comp,oggetti_num)
    
    if check_exist is False:
        return None
    
    #ritorno solo il prodotto che coincide con la descrizione passata da linea di comando
    return prodotto_data


#devo trovare quale lavorazione può fare questo robot
def search_robot_work(materiali,prodotto):
        
    #controllo per ogni prodotto, quale è in grado di produrre il robot
    lavori_disponibili = []
    for i in range(len(prodotto.componenti)):
        mat_1 = prodotto.componenti[i].mat_1
        mat_2 = prodotto.componenti[i].mat_2
        mat_3 = prodotto.componenti[i].mat_3
    
        """vic: abbiamo supposto che ogni componente è fatto da al massimo 3 materiali?"""

        #print("\n",mat_1,mat_2,mat_3)
        if materiali[0] >= mat_1 and materiali[1] >= mat_2 and materiali[2] >= mat_3:
            lavori_disponibili.append(True)
        else:
            lavori_disponibili.append(False)
    
    #print("Lavori disponibili: ", lavori_disponibili)
    return lavori_disponibili
        


#verifico se un robot non è in grado di fare nessun componente/lavorazione che bisogna effettuare
def check_robot_comp(vector_robot):
    
    count_false = 0
    
    for i in range(len(vector_robot)):
        if vector_robot[i] == False:
            count_false += 1
            
    if count_false == len(vector_robot):
        return False
    
    return True


#funzione che mi cerca il robot che ha più "True" al suo interno, ovvero quello che è in grado di fare più lavorazioni possibili
def search_best_True(robot_vector):
    max_count = 0
    current_count = 0 
       
    for i in range(len(robot_vector)):
        for j in range(4):
            if robot_vector[i][j] == True:
                current_count += 1

        #aggiorno il max
        if current_count > max_count:
            max_count = current_count
            indice_robot = i

    return robot_vector[indice_robot], indice_robot



def check_robot_doppia_lavorazione(arr):
    # Crea un dizionario vuoto per tenere traccia delle occorrenze
    count = {}
    # Itera attraverso ogni elemento dell'array
    for i in arr:
        # Se l'elemento è già nel dizionario, aumenta il suo conteggio di 1
        if i in count:
            count[i] += 1
        # Altrimenti, aggiungilo al dizionario con un conteggio di 1
        else:
            count[i] = 1
    common_elements = []
    # Itera attraverso il dizionario e aggiungi gli elementi che compaiono più di una volta alla lista
    for i in count:
        if count[i] > 1:
            common_elements.append(i)
            
    return common_elements




#algoritmo di intelligenza artificiale per prendere la decisione sulla lavorazione da fare su ogni robot
def ai_algorithm(prodotto_descrizione,robot_collection_all):
        

    #rimuovo robot che non soddisfano le condizioni di lavoro (enable=False)
    robot_collection = []
    for i in range(len(robot_collection_all)):
        #if robot_collection[indice].enable == False:
        if robot_collection_all[i].enable == True and robot_collection_all[i].working_status == False:
            # deleting the list item at the given index using the del keyword
            robot_collection.append(robot_collection_all[i])


    #stampo i robot che sono disponibili a lavorare
    print("\n\n\nI robot che sono disponibili per lavorare sono ",len(robot_collection))
    for i in range(len(robot_collection)):
        print("\n")
        robot_collection[i].stamp()


    #vado a leggere i componenti e le quantità dei Prodotti dal file Excel
    df_componente = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio1')
    df_componente = df_componente.fillna(0)
    #print('\n')
    #print(df_componente)

    component_vector = parse_componente(df_componente)
    """ for i in range(len(component_vector)):
        #print("\n")
        component_vector[i].stamp() """
        
    
    #vado a leggere il peso di ogni materiale
    df_materiale = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio2')
    df_materiale = df_materiale.fillna(0)
    #print('\n')
    #print(df_materiale)

    material_vector = parse_materiale(df_materiale)
    """ for i in range(len(material_vector)):
        print("\n")
        material_vector[i].stamp() """
        

    #vado a leggere per il prodotto richiesto, quali sono i componenti richiesti per fabbricarlo
    df_prodotto = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio3')
    df_prodotto = df_prodotto.fillna(0)
    """ print('\n')
    print(df_prodotto) """
    
    product_data = parse_prodotto(df_prodotto,prodotto_descrizione,component_vector)
    if product_data is None:
        print("\nERRORE: Prodotto non trovato nella lista di lavorazioni disponibili!\n")
        return
    print('\n')
    product_data.stamp()
          
    #per ogni robot (tra quelli a disposizione trovati sopra), mi vado a calcolare la quantità di ogni Materiale a loro disposizione
    #sapendo il peso specifico letto da Excel e il peso totale delle bilance
    
    robot_material = []
    
    for i in range(len(robot_collection)):
        mat_disp_robot = []
        mat_disp_1 = math.floor(robot_collection[i].weight_1 / material_vector[0].peso)
        mat_disp_2 = math.floor(robot_collection[i].weight_2 / material_vector[1].peso)
        mat_disp_3 = math.floor(robot_collection[i].weight_3 / material_vector[2].peso)
        
        mat_disp_robot.append(mat_disp_1)
        mat_disp_robot.append(mat_disp_2)
        mat_disp_robot.append(mat_disp_3)
        
        robot_material.append(mat_disp_robot)
    
        
    """ print("\nDisponibilità di ogni materiale per ogni robot: ")
    for i in range(len(robot_material)):
        print("Robot %i" %i , robot_material[i]) """
        
    
    #in base a quale prodotto devo fabbricare, per ogni componente, vado a vedere quale robot è in grado di fabbricarlo
    array_lavorazione_robot = []
    for i in range(len(robot_material)):
        array_lavorazione_robot.append(search_robot_work(robot_material[i],product_data))

    #ordino il vettore in base al numero di "True", dal robot che ne ha più a chi ne ha meno
    ''' array_lavorazione_robot = sorted(array_lavorazione_robot, key=sort_by_trues, reverse=True)
    print("array_lavorazione_robot:  \n")
    for i in range(len(array_lavorazione_robot)):
        print(array_lavorazione_robot[i]) '''


    
    result = find_combination_true(array_lavorazione_robot, 4)
    string_return = ""

    if result is not None:
        #print("Combinazione trovata:", result)
        print("\nCombinazione trovata")
        string_return = "Combinazione trovata"
    else:
        print("Nessuna combinazione trovata")
        string_return = "Nessuna combinazione trovata"
        return string_return

    #mi ricavo gli indici di questi array trovati come risultato (faccio confronto uno ad uno con gli altri)
    num_robot_da_cercare = 4
    indice_result = get_index_result_array(array_lavorazione_robot,result,num_robot_da_cercare)
    #print("i robot che devono lavorare sono: ",indice_result)

    # Algoritmo di Backtrack

    combination = []
    used_indexes = set()
    arrays = []

    for i in range(len(indice_result)):
        arrays.append(array_lavorazione_robot[indice_result[i]])
        #print("array_lavorazione_robot[indice_result[i]]: ",array_lavorazione_robot[indice_result[i]])

    backtrack(combination, arrays, used_indexes, 0)
    #print("used_indexes :",used_indexes)

    #presa la decisione, devo rimandare sul database l'informazione di quale 'lavorazione' ogni robot deve effettuare
    #(invio dati tramite una POST)
    for i in range(len(combination)):
        indice_comp_to_do = combination[i]
        #print("componente da fare: ",product_data.componenti[indice_comp_to_do].componente)
        #print("indice_result[i]: ",indice_result[i])
        print("Robot {} --> {}".format(robot_collection[indice_result[i]].robot ,product_data.componenti[indice_comp_to_do].componente))
        #postdata_lavorazione(indice_result[i]+1,robot_collection[indice_result[i]],product_data.componenti[indice_comp_to_do].componente)
        postdata_lavorazione(robot_collection[indice_result[i]].robot,robot_collection[indice_result[i]],product_data.componenti[indice_comp_to_do].componente)
       
    return string_return
