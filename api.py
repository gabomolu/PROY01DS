#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from fastapi import FastAPI
import pandas as pd
import calendar
from threading import Thread
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Carga del dataset
file_path = r'movies_dataset_procesado_reducido.csv'
data = pd.read_csv(file_path)

# Convertir las fechas a formato datetime para consultas precisas
data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')

# Instancia de la aplicación
app = FastAPI()

# Función auxiliar para convertir nombres de meses al formato adecuado en español
def mes_a_numero(mes):
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    return meses.get(mes.lower())

# Función auxiliar para convertir nombres de días de la semana en español al inglés
def dia_a_numero(dia):
    dias = {
        'lunes': 'Monday', 'martes': 'Tuesday', 'miércoles': 'Wednesday',
        'jueves': 'Thursday', 'viernes': 'Friday', 'sábado': 'Saturday', 'domingo': 'Sunday'
    }
    return dias.get(dia.lower())

# Función para contar la cantidad de filmaciones por mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    numero_mes = mes_a_numero(mes)
    if numero_mes:
        count = data[data['release_date'].dt.month == numero_mes].shape[0]
        return {"mensaje": f"{count} películas fueron estrenadas en el mes de {mes.capitalize()}"}
    else:
        return {"error": "Mes no válido"}

# Función para contar la cantidad de filmaciones por día
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dia_ingles = dia_a_numero(dia)
    if dia_ingles:
        count = data[data['release_date'].dt.day_name(locale='en') == dia_ingles].shape[0]
        return {"mensaje": f"{count} películas fueron estrenadas en el día {dia.capitalize()}"}
    else:
        return {"error": "Día no válido"}

# Función para obtener el score de una película por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    film = data[data['title'].str.lower() == titulo.lower()]
    if not film.empty:
        film = film.iloc[0]
        return {"mensaje": f"La película {film['title']} fue estrenada en el año {film['release_year']} con un score/popularidad de {film['popularity']}"}
    else:
        return {"error": "Película no encontrada"}

# Función para obtener la cantidad de votos de una película
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    film = data[data['title'].str.lower() == titulo.lower()]
    if not film.empty:
        film = film.iloc[0]
        if film['vote_count'] >= 2000:
            return {"mensaje": f"La película {film['title']} fue estrenada en el año {film['release_year']}. Cuenta con un total de {film['vote_count']} valoraciones, con un promedio de {film['vote_average']}"}
        else:
            return {"mensaje": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    else:
        return {"error": "Película no encontrada"}

# Función para obtener datos de un actor
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    peliculas_actor = data[data['actor'].str.contains(nombre_actor, na=False, case=False)]
    if not peliculas_actor.empty:
        cantidad = len(peliculas_actor)
        retorno_total = peliculas_actor['return'].sum()
        retorno_promedio = retorno_total / cantidad
        return {"mensaje": f"El actor {nombre_actor} ha participado en {cantidad} filmaciones. Ha conseguido un retorno total de {retorno_total:.2f} con un promedio de {retorno_promedio:.2f} por filmación"}
    else:
        return {"error": "Actor no encontrado"}

# Función para obtener datos de un director
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    peliculas_director = data[data['director'].str.lower() == nombre_director.lower()]
    if not peliculas_director.empty:
        resultado = []
        for _, pelicula in peliculas_director.iterrows():
            resultado.append({
                "titulo": pelicula['title'],
                "fecha_lanzamiento": pelicula['release_date'],
                "retorno": pelicula['return'],
                "costo": pelicula['budget'],
                "ganancia": pelicula['revenue'] - pelicula['budget']
            })
        return {"mensaje": resultado}
    else:
        return {"error": "Director no encontrado"}

# Crear la matriz TF-IDF usando el título de las películas para la recomendación
data['title'] = data['title'].fillna('').str.lower()
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['title'])
title_to_index = pd.Series(data.index, index=data['title']).to_dict()

# Función de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    titulo = titulo.lower()
    if titulo not in title_to_index:
        return {"error": "Película no encontrada"}

    idx = title_to_index[titulo]
    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    sim_indices = sim_scores.argsort()[::-1][1:6]
    recommended_titles = data['title'].iloc[sim_indices].tolist()
    
    return {"recomendaciones": recommended_titles}

# Correr la API en un hilo separado
def run_app():
    uvicorn.run(app, host="127.0.0.1", port=8001)

# Iniciar la API en un hilo
thread = Thread(target=run_app)
thread.start()

