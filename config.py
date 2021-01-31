import configparser

config = configparser.ConfigParser()
try:
    config.read('config.ini')
except Exception as inst:
    print(type(inst))

def DBFile():
    return(config['DB']['SQLFile'])

def listen_ip():
    return(config['Server']['listen_ip'])

def listen_port():
    return(config['Server']['listen_port'])


    
          

