#script per leggere dal file in cui è contenuto l indirizzo ip del server (pc acceso a casa mia)


file = open("ip_url.txt", "r")
ip = file.read()
file.close()

def get_ip():
    return ip