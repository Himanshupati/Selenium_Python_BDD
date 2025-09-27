import pyodbc
from cryptography.fernet import Fernet
from utils.config_loader import PropertiesReader
import configparser

def readconfig(keyelement):
    config = configparser.ConfigParser()
    config.read('config//config.properties')
    if config.has_option('DATABASE_DETAILS', keyelement):
        return config.get('DATABASE_DETAILS', keyelement)
    else:
        raise KeyError(f"The Key '{keyelement}' doesn't exist in the config file")

def create_dbconnection():
    config_reader = PropertiesReader("config\\config.properties")
    database = config_reader.get_section('DATABASE_DETAILS')
    server = database.get_key('DATABASE_NAME')
    database = database.get_key('DATABASE_NAME')
    username = database.get_key('DATABASE_USERNAME')
    key = database.get_key('KEY')
    encrypted = database.get_key('DATABASE_PASSWORD')

    # server = readconfig('DATABASE_SERVER')
    # database = readconfig('DATABASE_NAME')
    # username = readconfig('DATABASE_USERNAME')
    # key = readconfig('KEY')
    # encrypted = readconfig('DATABASE_PASSWORD')

    password = str(decrypt_data(key, encrypted), 'utf8')
    pass
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'Trusted_connection = yes;'
        'UID=' + username + ';'
        'PWD=' + password
    )
    conn = cnxn.cursor()
    return cnxn

def insertintodb(scenario_name, result, start_timestamp, end_timestamp, duration, manualexecutiontime, application, projectid, environment, prod_version):
    cnxn = create_dbconnection()
    conn = cnxn.cursor()
    count = conn.execute("""
        INSERT INTO [Selenium_DB].[dbo].[Selenium_PY_Executiondetails] 
        (testcaseName,result,startTime,endTime,duration, projectID,applicationName,environment,manualExecutionTime,prod_version)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """, scenario_name, result, start_timestamp, end_timestamp, duration, projectid, application, environment, manualexecutiontime, prod_version).rowcount
    cnxn.commit()

def decrypt_data(key, data):
    crypter = Fernet(key)
    decrypted_msg = crypter.decrypt(data)
    return decrypted_msg
