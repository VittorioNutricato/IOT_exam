import serial
import serial.tools.list_ports
import configparser
import requests
import time
import ip_url

class Bridge():

    def __init__(self,ip):
        self.config = configparser.ConfigParser()
        self.config.read('config_attuatore.ini')
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

    def get_working_status(self,id):
            url = 'http://{}/working_status/{}'.format(self.ip,id)  #url mio
            #url = 'http://155.185.80.241/lista'  #url vitto
            data = requests.get(url)
            #print(f"Response: {data.json()}")
            return data.json()
    
    def usedata(self,last_working_status):
        
        time.sleep(1)
        new_status = self.get_working_status(1) #IF RIESCO A LEGGERE (FARE LA GET) DAL SERVER:
        new_working_status = new_status.get('working_status')
        
        if (new_working_status == True) and (last_working_status == False):
            return True
        else:
            return False


    def loop(self):
            
            while (True):
                
                status = self.get_working_status(1) #IF RIESCO A LEGGERE (FARE LA GET) DAL SERVER:
                working_status = status.get('working_status')

                status_change=self.usedata(working_status)
                #print("status_change:", status_change)
            
                if (status_change == True):
                    self.ser.write(1)
                    print("inviato")

if __name__ == '__main__':
    ip = ip_url.get_ip()
    br=Bridge(ip)
    br.loop()