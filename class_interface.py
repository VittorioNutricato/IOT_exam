#classe Robot, per avere delle copie dei dati robot letti dal server
class Robot():
   
    def __init__(self,robot=0,temperature=0,pressure=0,weight_1=0,weight_2=0,weight_3=0,enable=True,working_status=False,lavorazione=""):
        self.temperature = temperature
        self.pressure = pressure
        self.robot = robot
        self.weight_1 = weight_1
        self.weight_2 = weight_2
        self.weight_3 = weight_3

        self.enable = enable
        self.working_status = working_status
        self.lavorazione = lavorazione
        

    def stamp(self):
        print("robot: ",self.robot)
        print("temperature: ",self.temperature)
        print("pressure: ",self.pressure)
        print("weight_1: ",self.weight_1)
        print("weight_2: ",self.weight_2)
        print("weight_3: ",self.weight_3)

        print("enable: ",self.enable)
        print("working_status: ",self.working_status)
        print("lavorazione: ",self.lavorazione)


class Componente():
    
    def __init__(self,componente,mat_1,mat_2,mat_3):
        self.componente = componente
        self.mat_1 = mat_1
        self.mat_2 = mat_2
        self.mat_3 = mat_3
        
    def stamp(self):
        print("Componente: ",self.componente)
        print("Materiale 1: ",self.mat_1)
        print("Materiale 2: ",self.mat_2)
        print("Materiale 3: ",self.mat_3)

def parse_componente(df):
    
    component_vector = []
    
    for i in range(len(df)):
        componente = df.loc[i, 'Componente']
        materiale_1 = df.loc[i, 'Materiale_1']
        materiale_2 = df.loc[i, 'Materiale_2']
        materiale_3 = df.loc[i, 'Materiale_3']
        component_vector.append(Componente(componente,materiale_1,materiale_2,materiale_3))
    
    return component_vector


#classe materiale, per sapere il peso unitario di ogni materiale, da dile excel
class Materiale():
    
    def __init__(self,descrizione,peso):
        self.descrizione = descrizione
        self.peso = peso
        
    def stamp(self):
        print("Descrizione: ",self.descrizione)       
        print("Peso: ",self.peso)       

def parse_materiale(df):
    
    material_vector = []
    
    for i in range(len(df)):
        descrizione = df.loc[i, 'Descrizione']
        peso = df.loc[i, 'Peso']
        material_vector.append(Materiale(descrizione,peso))
    
    return material_vector


#classe Prodotto, per sapere ogni Prodotto finito come è fabbricato
class Prodotto():
    
    def __init__(self,descrizione,oggetti_comp,oggetti_num):
        self.descrizione = descrizione
        self.componenti = oggetti_comp
        self.num = oggetti_num
                
    def stamp(self): 
        print("Descrizione: ",self.descrizione)       
        for i in range(len(self.componenti)):
            print("Componenti : ",self.componenti[i].componente)                
        print("Quantità : ",self.num)  