import psycopg2

URL="postgresql://leo:wz0DVDsXFwFjwlH0FS6lg2KMFtzhWcAJ@dpg-d0d4vr95pdvs73f7o8a0-a.oregon-postgres.render.com/pokemones_8bvs"

conn = psycopg2.connect(URL)
cursor=conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Sensores1;")
cursor.execute("DROP TABLE IF EXISTS Actuadores;")

cursor.execute("""CREATE TABLE IF NOT EXISTS Sensores1 (
               id SERIAL PRIMARY KEY,
               fecha TIMESTAMP,
               Temperatura NUMERIC,
               Gas NUMERIC,
               Luz NUMERIC,
               Humedad NUMERIC,
               Agua NUMERIC,
               Polvo NUMERIC)"""
               )

cursor.execute("""CREATE TABLE IF NOT EXISTS Actuadores (
               id SERIAL PRIMARY KEY,
               Motor1 BOOLEAN)"""
               )
cursor.execute("""INSERT INTO Actuadores (Motor1) VALUES (FALSE);"""
               )

conn.commit()
cursor.close()
conn.close()