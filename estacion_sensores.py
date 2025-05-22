from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime

URL="postgresql://leo:wz0DVDsXFwFjwlH0FS6lg2KMFtzhWcAJ@dpg-d0d4vr95pdvs73f7o8a0-a.oregon-postgres.render.com/pokemones_8bvs"

app= Flask(__name__)

@app.route("/")
def introduccion():
    return(
        "Esta es una api de mi estacion meteorologica"
    )

@app.route("/RecibirDatos", methods=["POST"])
def recibir_datos_sensores():
    data=request.get_json()
    #fecha = data.get("fecha")#la del ESP32
    fecha = datetime.now()#la de mi sevidor
    temp = data.get("Temperatura")
    gas = data.get("Gas")
    luz = data.get("Luz")
    humedad = data.get("Humedad")
    agua = data.get("Agua")
    polvo = data.get("Polvo")


    
    conn = psycopg2.connect(URL)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO Sensores1(fecha,Temperatura,Gas,Luz,Humedad,Agua,Polvo) VALUES (%s,%s,%s,%s,%s,%s,%s)", (fecha,temp,gas,luz,humedad,agua,polvo))
    conn.commit()
    cursor.close()
    conn.close()
    return "Dato Recibido"

if __name__=="__main__":
    app.run()

