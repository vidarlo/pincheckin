import configparser

config = configparser.ConfigParser()
try:
    config.read('config.ini')
except Exception as inst:
    print(type(inst))

def DBFile():
    return(config['DB']['SQLFile'])


    
          

