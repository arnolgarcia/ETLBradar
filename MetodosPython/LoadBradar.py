__author__ = 'Arnol'


import os
from osgeo import ogr,osr
import datetime as dt

def LoadDataBradar(path,connStr, tabla, rad_id):
    ficheros = os.listdir(path)
    k=1
    N = len(ficheros)
    for fichero in ficheros:
        # testing del loop
        print "Cargando archivo (%s/%s) %s... "%(str(k), str(N), str(fichero)),
        # metodo
        (nombreFichero, extension) = os.path.splitext(fichero)
        fecha = nombreFichero[13:23]
        hora = nombreFichero[25:33].replace("_",":")
        fechahora = str(fecha) + " " +str(hora)
        #TODO: aqui se ajusta la fecha dado el correo de Karlus, esto se debe dejar parmetrizado despues
        fechahora = dt.datetime.strptime(fechahora, "%Y-%m-%d %H:%M:%S")
        dif = dt.timedelta(seconds=3600*3 + 60*4) # se resta 3hr y 4min
        new_fechahora = str(fechahora - dif)
        # Obtener datos como un arreglo
        datos = GetData(path + "/" + fichero)
        # Cargar datos a la BD
        LoadDataBySQL(connStr, tabla, datos, rad_id, new_fechahora)
        k = k +1
#Fin de la funcion LoadDataBradar()


def GetData(filename):
    datos = []
    with open(filename) as infile:
        infile.seek(0)
        for line in infile:
            Line=line.split("\t")
            # Agregar columnas (este, norte, altura, deformacion) y reemplazar "," por "."
            col1=Line[0].replace(",",".")
            col2=Line[1].replace(",",".")
            col3=Line[2].replace(",",".")
            col4=Line[3].replace(",",".")
            # En caso que la deformacion sea nula (-9999) dejarlo como 'None'
            if float(col4)==-9999:
                col4=None
            datos.append([col1, col2, col3, col4])
    infile.close()
    return datos
#Fin de la funcion DatosPerfil


def LoadDataBySQL(connStr, table, datos, rad_id, fh): #TODO: dejar solo una conexion y no abrir/cerrar a cada crato
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
        sql = 'INSERT INTO "%s"."%s" ("radar_id", "fecha","este","norte", "altura", "desplazamiento") VALUES '%(StrEsquema, StrTabla)
        N = len(datos)
        for i in range(N):
            # Set the attributes using the values from the data
            este = str(datos[i][0])
            norte = str(datos[i][1])
            altura = str(datos[i][2])
            desp = str(datos[i][3])
            if desp == 'None':
                desp = "NULL"
            sqlAux = "(%s,'%s',%s,%s,%s,%s),"%(rad_id, fh, este, norte, altura, desp)
            sql = sql + sqlAux
        # Ejecutar el sql completo
        sql = sql[0:-1]
        conn.ExecuteSQL(sql)
        print '%d registros cargados exitosamente'%(N)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de cargar los datos en la tabla " + table + " :" + str(e)
    return codeError
#Fin de la funcion LoadDataBySQL()

