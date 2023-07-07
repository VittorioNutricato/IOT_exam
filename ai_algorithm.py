import requests
from flask import render_template, request, jsonify
from urllib.request import urlopen
import pandas as pd
import math
import argparse
from itertools import permutations
import class_interface as ci
import utility as utility
import sys
import requests
from flask import render_template, request, jsonify
from urllib.request import urlopen
import pandas as pd
import math
from itertools import permutations
import class_interface as ci


if __name__ == '__main__':
     
    my_string = sys.argv[2]
    
    if not my_string :

        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("--prodotto", type=str,
            default="p1",
            help="Prodotto che si vuole produrre")
        """ ap.add_argument("--id", type=int, action="store",nargs='*',
                        default=[1,2],
                        help='ID number for Aruco Marker') """

        args = vars(ap.parse_args())
        prodotto = args['prodotto']

    else:
        prodotto = my_string
        

    print("Prodotto richiesto: ",prodotto)       

    data = utility.get_data()
    #print("data_len: ",len(data))
    #print(data[0][0].get('id'))

    #scrivo dati su un file di testo
    f = open("robot.txt", "w")

    #creo i robot con i valori scaricati dal server
    robot_collection=[]

    for i in range(len(data)):
        robot_collection.append(ci.Robot(robot=data[i][0].get('robot'),temperature=data[i][0].get('temperature'),pressure=data[i][0].get('pressure'),weight_1=data[i][0].get('weight_1'),weight_2=data[i][0].get('weight_2'),weight_3=data[i][0].get('weight_3'),enable=data[i][0].get('enable'),working_status=data[i][0].get('working_status'),lavorazione=data[i][0].get('lavorazione')))
        f.write(str(data[i][0].get('robot'))+","+str(data[i][0].get('temperature'))+","+str(data[i][0].get('pressure'))+","+str(data[i][0].get('weight_1'))+","+str(data[i][0].get('weight_2'))+","+str(data[i][0].get('weight_3'))+","+str(data[i][0].get('enable'))+","+str(data[i][0].get('working_status'))+","+str(data[i][0].get('lavorazione'))+'\n')

    f.close()


    #chiamo funzione per prendere la decisione sulla lavorazione
    result = utility.ai_algorithm(prodotto,robot_collection)
    print("result algorithm: ",result)

    f = open("output_lavorazione.txt", "w")
    f.write(result)
    f.close()