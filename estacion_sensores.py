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



@app.route("/verDatos")
def ver_datos():
    conn = psycopg2.connect(URL)
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM Sensores1")
    datos = cursor.fetchall()
    conn.close()
    return jsonify([{"Id": x[0], "Fecha": x[1], "Temperatura": x[2],
                     "Gas": x[3], "Luz": x[4], "Humedad": x[5],
                     "Agua": x[6], "Polvo": x[7]} for x in datos])



@app.route("/estadoMotor")
def estado_motor():
    conn = psycopg2.connect(URL)
    cursor = conn.cursor()
    cursor.execute("SELECT Motor1 FROM Actuadores WHERE id = 1")
    estado = cursor.fetchone()
    conn.close()
    return jsonify({"Motor1": estado[0]})

@app.route("/moverMotor", methods=["POST"])
def mover_motor():
    conn = psycopg2.connect(URL)
    cursor = conn.cursor()
    cursor.execute("SELECT Motor1 FROM Actuadores WHERE id = 1")
    estado_actual = cursor.fetchone()[0]
    nuevo_estado = not estado_actual
    cursor.execute("UPDATE Actuadores SET Motor1 = %s WHERE id = 1", (nuevo_estado,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Motor cambiado a {int(nuevo_estado)}", "Motor1": nuevo_estado})

if __name__=="__main__":
    app.run()

