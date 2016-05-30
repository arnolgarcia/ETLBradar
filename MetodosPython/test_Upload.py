__author__ = 'Arnol'

import LoadBradar as lb
import datetime
import test_UploadOnline as test


GlobalValues = {}
GlobalValues['host'] = "" + "152.231.85.227"
GlobalValues['port'] = "" + "5433"
GlobalValues['dbname'] = "" + "geoalert_testing"
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = "" + "Admin321" #"admin"




GlobalValues['connString'] = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" %(GlobalValues['host'],
                                                                                  GlobalValues['port'],
                                                                                  GlobalValues['dbname'],
                                                                                  GlobalValues['user'],
                                                                                  GlobalValues['password'])

#connStr = GlobalValues['connString']
#path = "C:/Users/Arnol/Desktop/Datos Bradar/data_files/processed"
#path = "C:/Users/Arnol/GitHub/ETLBradar/MetodosPython/data_test"
#tabla = "radar_bradar.uploaded_data"
#radar = 1

"""
ini_time = datetime.datetime.now()
lb.LoadDataBradar(path, connStr, tabla, radar)
end_time = datetime.datetime.now()
print end_time - ini_time
"""

ini_time = datetime.datetime.now()

filen = "C:\Users\Arnol\GitHub\ETLBradar\MetodosPython\data_radar_timeseries_sample100m.txt"
connStr = GlobalValues['connString']
tabla = "radar_bradar.data_radar_timeseries_test_online"

datos = test.GetDataTest(filen)
datos = sorted(datos, key = lambda tup: tup[3])
print("Datos leidos...")
test.LoadDataBySQLwithSleep(connStr, tabla, datos, 10)

end_time = datetime.datetime.now()
print end_time - ini_time
