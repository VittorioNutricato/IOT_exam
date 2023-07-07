from flask import Flask
from config import Config
#from config_flask import Config
from flask import render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import random
from bs4 import BeautifulSoup
import requests
import json
from flask_marshmallow import Marshmallow # new
from flask_restful import Api, Resource # new
import subprocess
import requests
from flask import render_template, request, jsonify
from urllib.request import urlopen
import pandas as pd
import math
import argparse
from itertools import permutations
import class_interface as ci
import ip_url
import utility as utility
import requests
from flask import render_template, request, jsonify
from urllib.request import urlopen
import pandas as pd
import math
from itertools import permutations
import class_interface as ci
import ip_url
import sys

appname = "IOT - server"
app = Flask(appname)
ma = Marshmallow(app) # new
api = Api(app) # new

myconfig = Config
app.config.from_object(myconfig)

# db creation
db = SQLAlchemy(app)

class Robot(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    robot = db.Column('robot', db.Integer)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,  default=datetime.utcnow)
    temperature = db.Column('temperature', db.Integer)
    pressure = db.Column('pressure', db.Integer)
    weight_1 = db.Column('weight_1', db.Integer)
    weight_2 = db.Column('weight_2', db.Integer)
    weight_3 = db.Column('weight_3', db.Integer)
    enable = db.Column('enable', db.Boolean)
    working_status = db.Column('working_status', db.Boolean)
    lavorazione = db.Column('lavorazione', db.String)

   
    def __init__(self,robot,temperature,pressure,weight_1,weight_2,weight_3,enable,working_status,lavorazione):
        self.temperature = temperature
        self.pressure = pressure
        self.weight_1 = weight_1
        self.weight_2 = weight_2
        self.weight_3 = weight_3
        self.robot = robot
        self.timestamp = datetime.now()
        self.enable = enable
        self.working_status = working_status
        self.lavorazione = lavorazione


class RobotSchema(ma.Schema):
    class Meta:
        fields = ("robot", "temperature","pressure","weight_1","weight_2","weight_3","enable","working_status","lavorazione")
        
post_schema = RobotSchema()
posts_schema = RobotSchema(many=True)


@app.errorhandler(404)
def page_not_found(error):
    return 'Errore', 404



#------------------------GET--------------------------------------------------
@app.route("/ai_algorithm")
def ai_algorithm():

    #vado a leggere i componenti e le quantità dei Prodotti dal file Excel
    df_componente = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio1')
    df_componente = df_componente.fillna(0)

    #vado a leggere per il prodotto richiesto, quali sono i componenti richiesti per fabbricarlo
    df_prodotto = pd.read_excel('excel_product\\prodotti.xlsx', sheet_name='Foglio3')
    df_prodotto = df_prodotto.fillna(0)

    componente_data = df_componente.values.tolist()
    product_data = df_prodotto.values.tolist()

    lista = product_data+componente_data
    print("lista: ",lista)
    
    
    return render_template('form.html')
    

@app.route('/esegui_script',  methods=['GET'])
def esegui_script():

    input_string = request.args.get("stringa")
    #la "input_stringa" sarebbe il nostro parametro "p4" da passare

    ''' with open('ai_algorithm.py', 'r') as f:
        codice = f.read()
        exec(codice) '''

    # Esegui lo script Python esterno passando la stringa come argomento
    subprocess.call(["python", "ai_algorithm.py", input_string])
    
    # apre il file in modalità lettura
     #scrivo dati su un file di testo
    f = open("output_lavorazione.txt", "r")
    content = f.read()
    f.close()
    """ with open('output_lavorazione.txt', 'r') as file:
        # legge il contenuto del file
        content = file.read()
        # stampa il contenuto del file
        print("content: ",content) """
    return content
    #return render_template('form.html',message=content)


@app.route('/', methods=['GET'])
def home_page():
    return render_template('main.html')


#ritorna JSON completo del robot richiesto
@app.route('/robot/<robot>/', methods=['GET'])
def get_robot(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0])


#ritorna JSON con il parametro specifico del robot richiesto
@app.route('/temperature/<robot>/', methods=['GET'])
def get_temperature(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    #return jsonify(result[0]['temperature'])
    return jsonify(result[0]['temperature'])

@app.route('/pressure/<robot>/', methods=['GET'])
def get_pressure(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0]['pressure'])

@app.route('/weight_1/<robot>/', methods=['GET'])
def get_weight_1(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0]['weight_1'])

@app.route('/weight_2/<robot>/', methods=['GET'])
def get_weight_2(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0]['weight_2'])

@app.route('/weight_3/<robot>/', methods=['GET'])
def get_weight_3(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0]['weight_3'])

@app.route('/enable/<robot>/', methods=['GET'])
def get_enable(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0]['enable'])

@app.route('/working_status/<robot>/', methods=['GET'])
def get_working_status(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    #return jsonify(result[0]['working_status'])
    return jsonify(working_status=result[0]['working_status'])


@app.route('/lavorazione/<robot>/', methods=['GET'])
def get_lavorazione(robot):
    
    elenco=Robot.query.filter_by(robot=robot).order_by(Robot.timestamp.desc()).limit(1).all()
    result = posts_schema.dump(elenco)
    return jsonify(result[0]['lavorazione'])

@app.route('/lista_completa', methods=['GET'])
def stampalista_all():
    #elenco=Robot.query.all() #ritorna tutti gli oggetti presenti nel db di tipo "Robot"
    elenco=Robot.query.order_by(Robot.id.desc()).all()   #limita la visualizzazione a gli ultimi 2 record registrati
    return render_template('lista_completa.html', lista=elenco)

@app.route('/lista', methods=['GET'])
def stampalista():
    #elenco=Robot.query.all() #ritorna tutti gli oggetti presenti nel db di tipo "Robot"

    elenco1=Robot.query.filter_by(robot="1").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco2=Robot.query.filter_by(robot="2").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco3=Robot.query.filter_by(robot="3").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco4=Robot.query.filter_by(robot="4").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco5=Robot.query.filter_by(robot="5").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco6=Robot.query.filter_by(robot="6").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco7=Robot.query.filter_by(robot="7").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco8=Robot.query.filter_by(robot="8").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco9=Robot.query.filter_by(robot="9").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco10=Robot.query.filter_by(robot="10").order_by(Robot.timestamp.desc()).limit(1).all()

    return render_template('lista_completa.html', lista=elenco1+elenco2+elenco3+elenco4+elenco5+elenco6+elenco7+elenco8+elenco9+elenco10)


@app.route('/lista_json', methods=['GET'])
def stampalista_json():
    #elenco=Robot.query.all() #ritorna tutti gli oggetti presenti nel db di tipo "Robot"

    elenco1=Robot.query.filter_by(robot="1").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco2=Robot.query.filter_by(robot="2").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco3=Robot.query.filter_by(robot="3").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco4=Robot.query.filter_by(robot="4").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco5=Robot.query.filter_by(robot="5").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco6=Robot.query.filter_by(robot="6").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco7=Robot.query.filter_by(robot="7").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco8=Robot.query.filter_by(robot="8").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco9=Robot.query.filter_by(robot="9").order_by(Robot.timestamp.desc()).limit(1).all()
    elenco10=Robot.query.filter_by(robot="10").order_by(Robot.timestamp.desc()).limit(1).all()

    result = []
    result.append(posts_schema.dump(elenco1))
    result.append(posts_schema.dump(elenco2))
    result.append(posts_schema.dump(elenco3))
    result.append(posts_schema.dump(elenco4))
    result.append(posts_schema.dump(elenco5))
    result.append(posts_schema.dump(elenco6))
    result.append(posts_schema.dump(elenco7))
    result.append(posts_schema.dump(elenco8))
    result.append(posts_schema.dump(elenco9))
    result.append(posts_schema.dump(elenco10))
    
    #return result
    return jsonify(result)


#PAGINE/TEMPLATE PER VISUALIZZARE SOLO QUEL ROBOT

@app.route('/robot1', methods=['GET'])
def stamparobot_1():

    elenco=Robot.query.filter_by(robot="1").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista1.html', lista=elenco)


@app.route('/robot2', methods=['GET'])
def stamparobot_2():

    elenco=Robot.query.filter_by(robot="2").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista2.html', lista=elenco)


@app.route('/robot3', methods=['GET'])
def stamparobot_3():

    elenco=Robot.query.filter_by(robot="3").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista3.html', lista=elenco)


@app.route('/robot4', methods=['GET'])
def stamparobot_4():

    elenco=Robot.query.filter_by(robot="4").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista4.html', lista=elenco)


@app.route('/robot5', methods=['GET'])
def stamparobot_5():

    elenco=Robot.query.filter_by(robot="5").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista5.html', lista=elenco)


@app.route('/robot6', methods=['GET'])
def stamparobot_6():

    elenco=Robot.query.filter_by(robot="6").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista6.html', lista=elenco)


@app.route('/robot7', methods=['GET'])
def stamparobot_7():

    elenco=Robot.query.filter_by(robot="7").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista7.html', lista=elenco)


@app.route('/robot8', methods=['GET'])
def stamparobot_8():

    elenco=Robot.query.filter_by(robot="8").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista8.html', lista=elenco)


@app.route('/robot9', methods=['GET'])
def stamparobot_9():

    elenco=Robot.query.filter_by(robot="9").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista9.html', lista=elenco)


@app.route('/robot10', methods=['GET'])
def stamparobot_10():

    elenco=Robot.query.filter_by(robot="10").order_by(Robot.timestamp.desc()).limit(1).all()
    return render_template('lista10.html', lista=elenco)


#--------------------------------------------------------------------------------------------------

    
    
#------------------------POST-----------------------------------------------------------------
    
@app.route('/addinlista/<robot>/<temperature>/<pressure>/<weight_1>/<weight_2>/<weight_3>/<enable>', methods=['POST'])
def addinlista(robot,temperature,pressure,weight_1,weight_2,weight_3,enable,lavorazione=""):
    
    if enable == "True":
        my_posts = Robot(robot,temperature,pressure,weight_1,weight_2,weight_3,True,False,lavorazione)
    else:
        my_posts = Robot(robot,temperature,pressure,weight_1,weight_2,weight_3,False,False,lavorazione)
    db.session.add(my_posts)
    db.session.commit()
 
    return post_schema.jsonify(my_posts)


@app.route('/addinlista_lavorazione/<robot>/<temperature>/<pressure>/<weight_1>/<weight_2>/<weight_3>/<lavorazione>', methods=['POST'])
def addinlista_lavorazione(robot,temperature,pressure,weight_1,weight_2,weight_3,lavorazione,enable=True,working_status=True):

    my_posts = Robot(robot,temperature,pressure,weight_1,weight_2,weight_3,enable,working_status,lavorazione)
    db.session.add(my_posts)
    db.session.commit()
 
    return post_schema.jsonify(my_posts)

#--------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    if True:  # first time (?)
        with app.app_context():
            db.create_all()

    port = 80
    interface = '0.0.0.0'
    app.run(host=interface,port=port)