__author__ = 'Arnol'

import datetime as dt

ahora = dt.datetime.now()
ahora = (str(ahora))
print ahora

ahora = dt.datetime.strptime(ahora, "%Y-%m-%d %H:%M:%S.%f")

dif = dt.timedelta(seconds=3600*3 + 60*4)

new_time = ahora - dif
print new_time

