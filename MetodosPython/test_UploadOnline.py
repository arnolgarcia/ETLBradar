__author__ = 'Arnol'


import os
from osgeo import ogr,osr
import datetime as dt
import time as tm


def GetDataTest(filename):
    datos = []
    with open(filename) as infile:
        infile.seek(0)
        for line in infile:
            Line=line.split("\t")
            # Agregar columnas y reemplazar "," por "."
            col0 = Line[0].replace(",",".") # new_id_grilla
            col1 = Line[1].replace(",",".") # new_x
            col2 = Line[2].replace(",",".") # new_y
            col3 = Line[3].replace(",",".") # fecha
            col4 = Line[4].replace(",",".") # desplazamiento
            col5 = Line[5].replace(",",".") # desplazamiento_acumulado
            col6 = Line[6].replace(",",".") # velocidad
            # En caso que la deformacion sea nula (-9999) dejarlo como 'None'
            #if float(col4)==-9999:
            #    col4=None
            datos.append([col0, col1, col2, col3, col4, col5, col6])
    infile.close()
    return datos
#Fin de la funcion GetDataTest


def LoadDataBySQLwithSleep(connStr, table, datos, sleeptime): #TODO: dejar solo una conexion y no abrir/cerrar a cada crato
    codeError = 0
    # Probar la conexion
    try:
        conn = ogr.Open(connStr)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de conectarse a la BD " + " :" + str(e)
        return codeError
    # Leer archivo y cargarlo en BD
    nombretabla = table.split(".")
    StrEsquema = nombretabla[0].lower()
    StrTabla =nombretabla[1].lower()
    try:
        sql = 'INSERT INTO "%s"."%s" ("new_id_grilla", "new_x","new_y","fecha", "desplazamiento", "desplazamiento_acumulado", "velocidad") VALUES '%(StrEsquema, StrTabla)
        N = len(datos)
        fecha_ante = str(datos[0][3])
        fecha_ante = "'" + str(dt.datetime.strptime(fecha_ante, "%d-%m-%Y %H:%M:%S")) + "'"
        newfecha = str(dt.datetime.now())
        for i in range(N):
            # Set the attributes using the values from the data
            new_id_grilla = str(datos[i][0])
            new_x = str(datos[i][1])
            new_y = str(datos[i][2])
            fecha = str(datos[i][3])
            fecha = "'" + str(dt.datetime.strptime(fecha, "%d-%m-%Y %H:%M:%S")) + "'" #TODO: modificacion especifica
            desplazamiento = str(datos[i][4])
            desplazamiento_acumulado = str(datos[i][5])
            velocidad = str(datos[i][6])
            sqlAux = "(%s,%s,%s,'%s',%s,%s,%s),"%(new_id_grilla, new_x, new_y, newfecha, desplazamiento, desplazamiento_acumulado, velocidad)
            if(fecha_ante != fecha):
                sql = sql[0:-1]
                conn.ExecuteSQL(sql)
                print 'Query ejecutada para la fecha %s'%(fecha_ante)
                sql = 'INSERT INTO "%s"."%s" ("new_id_grilla", "new_x","new_y","fecha", "desplazamiento", "desplazamiento_acumulado", "velocidad") VALUES '%(StrEsquema, StrTabla)
                fecha_ante = fecha
                tm.sleep(sleeptime)
                newfecha = str(dt.datetime.now())
            sql = sql + sqlAux
        # Ejecutar el sql completo
        sql = sql[0:-1]
        conn.ExecuteSQL(sql)
        print '%d registros cargados exitosamente'%(N)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de cargar los datos en la tabla " + table + " :" + str(e)
    conn.Destroy()
    return codeError
#Fin de la funcion LoadDataBySQLwithSleep()
