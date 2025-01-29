import datetime


hoy = datetime.datetime.now()   
año = hoy.year
mes = hoy.month

print(f"http://161.131.215.59:8090/wsRentabilidadJs/descargar?ano={año}&mes={mes}&grupo=1&rut=0&sesion=1") 