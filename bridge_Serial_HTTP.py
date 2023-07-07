import serial
import serial.tools.list_ports
import requests
import time
import configparser
import ip_url

class Bridge():

    def __init__(self,ip):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.setupSerial()
        self.ip = ip


    def setupSerial(self):
        # open serial port
        self.ser = None

        if self.config.get("Serial","UseDescription", fallback=False):
            self.portname = self.config.get("Serial","PortName", fallback="COM1")
        else:
            print("list of available ports: ")
            ports = serial.tools.list_ports.comports()

            for port in ports:
                print (port.device)
                print (port.description)
                if self.config.get("Serial","PortDescription", fallback="arduino").lower() \
                        in port.description.lower():
                    self.portname = port.device

        try:
            if self.portname is not None:
                print ("connecting to " + self.portname)
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None

        #self.ser.open()

        # internal input buffer from serial
        self.inbuffer = []
        

    def postdata(self,elenco):
        ''' if i>0:
            return '''
        url = 'http://{}/addinlista/{}/{}/{}/{}/{}/{}/{}'.format(self.ip,1,elenco[0],elenco[1],elenco[2],elenco[3],elenco[4],elenco[5])
        x = requests.post(url)
        
        
    def get_working_status(self,id):
        url = 'http://{}/working_status/{}'.format(self.ip,id)  #url mio
        #url = 'http://155.185.80.241/lista'  #url vitto
        data = requests.get(url)
        #print(f"Response: {data.json()}")
        return data.json()


    def loop(self):
        # infinite loop for serial managing

        post_status_last_arduino = True
        
        while (True):
            
            #look for a byte from serial
            if not self.ser is None:

                if self.ser.in_waiting>0:
                    # data available from the serial port
                    #lastchar=self.ser.read(1)
                    lastchar=self.ser.read(1)

                    if lastchar==b'\xfe': #EOL
                        print("\nValue received")
                        post_status_last_arduino=self.useData(post_status_last_arduino)
                        self.inbuffer =[]

                    if lastchar!=b'\xff' and lastchar!=b'\xfe':
                        lastchar = lastchar.decode('utf-8') #toglie la 'b'
                        self.inbuffer.append(lastchar)                

                    ''' else:
                        self.inbuffer.append (lastchar)  '''
        
            #aspetto 2 secondi dopo aver inviato un dato
            #time.sleep(1)

    def useData(self,post_status_last_arduino):

        elenco = []
        enable = True
        
        #print("self.inbuffer: ",self.inbuffer)

        string_data = "".join(self.inbuffer)
        #print("string_data: ",string_data)

        stringhe = string_data.split(',')

        for i in range (len(stringhe)):
            if i==0:
                print("Temperature: ",stringhe[i])
                elenco.append(stringhe[i])
                if float(stringhe[i]) < 5 or float(stringhe[i]) > 30:
                    enable = False
            if i==1:
                print("Pressure: ",stringhe[i])
                elenco.append(stringhe[i])
                if (float(stringhe[i])  - 1.01325) > 0.07:
                    enable = False
            if i==2:
                print("Weight_1: ",stringhe[i])
                elenco.append(stringhe[i])  
            if i==3:
                print("Weight_2: ",stringhe[i])
                elenco.append(stringhe[i]) 
            if i==4:
                print("Weight_3: ",stringhe[i])
                elenco.append(stringhe[i])
            if i==5:
                print("post_status: ",stringhe[i])
                if stringhe[i] == "1" :
                    post_status_arduino = True
                else :
                    post_status_arduino = False         
  
        elenco.append(enable)
        
        status = self.get_working_status(1) #IF RIESCO A LEGGERE (FARE LA GET) DAL SERVER:
        working_status = status.get('working_status')
        #print("working_status:", working_status)

        #if (status == "IoT Template Example\nTrue"):
        if (working_status == True):
            if (post_status_arduino != post_status_last_arduino) :
                self.postdata(elenco)
        else :
            self.postdata(elenco)

        print("post_status_last_arduino: ",post_status_last_arduino)
        print("post_status_arduino: ",post_status_arduino)

        return  post_status_arduino

        #------------------------------------------------------------------------------------------

if __name__ == '__main__':
    ip = ip_url.get_ip()
    br=Bridge(ip)
    
    br.loop()