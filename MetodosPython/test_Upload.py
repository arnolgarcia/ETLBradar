__author__ = 'Arnol'

import LoadBradar as lb
import datetime


GlobalValues = {}
GlobalValues['host'] = "" + "152.231.85.227"
GlobalValues['port'] = "" + "5433"
GlobalValues['dbname'] = "" + "geoalert_bradar"
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = "" + "Admin321" #"admin"




GlobalValues['connString'] = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" %(GlobalValues['host'],
                                                                                  GlobalValues['port'],
                                                                                  GlobalValues['dbname'],
                                                                                  GlobalValues['user'],
                                                                                  GlobalValues['password'])

connStr = GlobalValues['connString']
#path = "C:/Users/Arnol/Desktop/Datos Bradar/data_files/processed"
path = "C:/Users/Arnol/GitHub/ETLBradar/MetodosPython/data_test"
tabla = "radar_bradar.uploaded_data"
radar = 1

ini_time = datetime.datetime.now()
lb.LoadDataBradar(path, connStr, tabla, radar)
end_time = datetime.datetime.now()
print end_time - ini_time
