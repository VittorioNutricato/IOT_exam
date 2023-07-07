import requests
import time
import configparser
import random
import pandas as pd
import class_interface as ci
import ip_url


maxrobot=10      

class Bridge():

    def __init__(self,ip):
        self.ip = ip
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def postdata(self,temperature,pressure,weight_1,weight_2,weight_3,enable,nrobot):
        url = 'http://{}/addinlista/{}/{}/{}/{}/{}/{}/{}'.format(self.ip,nrobot,temperature,pressure,weight_1,weight_2,weight_3,enable)
        x = requests.post(url)

    def get_working_status(self,id):
        url = 'http://{}/working_status/{}'.format(self.ip,id)  #url mio
        #url = 'http://155.185.80.241/lista'  #url vitto
        data = requests.get(url)
        return data.json()

    def get_robot(self,id):
        url = 'http://{}/robot/{}'.format(self.ip,id)  #url mio
        #url = 'http://155.185.80.241/get_weights/{}'  #url vitto
        data = requests.get(url)
        return data.json()

    
    def useDataLoop(self):

        #vado a leggere i componenti e le quantità dei Prodotti dal file Excel
        df_componente = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio1')
        df_componente = df_componente.fillna(0)

        component_vector = ci.parse_componente(df_componente)
        for i in range(len(component_vector)):
            print("\n")
            component_vector[i].stamp()
        print("\n")

        #vado a leggere il peso di ogni materiale
        df_materiale = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio2')
        df_materiale = df_materiale.fillna(0)

        material_vector = ci.parse_materiale(df_materiale)
        for i in range(len(material_vector)):
            print("\n")
            material_vector[i].stamp()
        print("\n")

        while (True):
            
            # CASUALMENTE UN ROBOT (CHE NON STA LAVORANDO) VA FUORI SERVIZIO PER TEMPERATURA FUROI DAL RANGE
            nrobot = random.randint(2,10)
            elenco = self.get_robot(nrobot)

            if elenco.get('working_status') == False:
                if (random.randint(1,100)>90):
                    self.postdata(54.79,pressure,elenco.get('weight_1'),elenco.get('weight_2'),elenco.get('weight_3'),False,nrobot)

            #SORTEGGIO UN NUOVO ROBOT PER POSTARE NUOVI DATI

            nrobot = random.randint(2,10)
            status = self.get_working_status(nrobot) #IF RIESCO A LEGGERE (FARE LA GET) DAL SERVER:
            working_status = status.get('working_status')
                        
            print("robot:", nrobot)


            if (working_status == True): #IF ROBOT STA LAVORANDO AD UN COMPONENTE
                elenco = self.get_robot(nrobot)

                if (random.randint(1,100)>80): # IF PER RALLENTARE LA LAVORAZIONE DEL ROBOT IN MODO CASUALE
                    for i in range(len(component_vector)):
                        if (component_vector[i].componente == elenco.get("lavorazione")): #TROVO LA LISTA DI MATERIALI NECESSARI
                            print("\n")
                            weight_1=round(elenco.get('weight_1')-((component_vector[i].mat_1)*material_vector[0].peso),2)
                            weight_2=round(elenco.get('weight_2')-((component_vector[i].mat_2)*material_vector[1].peso),2)
                            weight_3=round(elenco.get('weight_3')-((component_vector[i].mat_3)*material_vector[2].peso),2)
                            print("record:", elenco.get('temperature'),elenco.get('pressure'),weight_1,weight_2,weight_3,elenco.get("enable"))
                            self.postdata(elenco.get('temperature'),elenco.get('pressure'),weight_1,weight_2,weight_3,elenco.get("enable"),nrobot)
                            
            else:
                elenco = self.get_robot(nrobot)
                print("record:", elenco.get('temperature'),elenco.get('pressure'),elenco.get('weight_1'),elenco.get('weight_2'),elenco.get('weight_3'),elenco.get("enable"))
                self.postdata(round(20.00+random.uniform(-10,10),2),round(1.00+random.uniform(-0.2,0.08),2),elenco.get('weight_1'),elenco.get('weight_2'),elenco.get('weight_3'),True,nrobot)
            
            print("\n")
            time.sleep(1)
            
            
if __name__ == '__main__':
    ip = ip_url.get_ip()
    br=Bridge(ip)
    
    for i in range(maxrobot):
        if (i != 0):
            
            temperature = round(20.00+random.uniform(-10,10),2)
            pressure = round(1.00+random.uniform(-0.2,0.08),2)
            weight_1 = round(10.00+random.uniform(-1.0,30.0),2)
            weight_2 = round(10.00+random.uniform(-1.0,30.0),2)
            weight_3 = round(10.00+random.uniform(-1.0,30.0),2)
            enable = True
            
            if temperature < 5 or temperature > 30:
                enable = False
                
            if pressure  - 1.01325 > 0.07:
                enable = False
                    
            br.postdata(temperature,pressure,weight_1,weight_2,weight_3,enable,i+1)
    
    time.sleep(2)
    br.useDataLoop()