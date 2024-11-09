Proyecto Individual Nº1: Machine Learning Operations (MLOps)
Descripción del Problema y Rol
Asumiendo el rol de un MLOps Engineer, desarrollaste un sistema de recomendación de películas en una start-up de servicios de streaming, partiendo de datos en un formato inmaduro y sin procesos automatizados. Con un enfoque ágil, creaste un MVP (Minimum Viable Product) que incluyó desde la limpieza de datos hasta el deployment de la API.

Pipeline de Transformaciones y Limpieza de Datos
Desanidación y Normalización: Extraí campos anidados como belongs_to_collection y production_companies y los uní al dataset principal para facilitar las consultas.
Tratamiento de Nulos: Completé valores faltantes de revenue y budget con 0 y eliminé registros sin fecha de lanzamiento (release_date).
Formato y Extracción de Fechas: Estandaricé las fechas al formato AAAA-mm-dd y creé una columna adicional release_year para indicar el año de estreno.
Cálculo de Retorno de Inversión: Agregué una columna return calculando revenue/budget, asignando 0 cuando no había datos disponibles.
Optimización del Dataset: Eliminé columnas irrelevantes (video, imdb_id, adult, original_title, poster_path, homepage), optimizando el dataset para consultas rápidas.
Desarrollo de API con FastAPI
Construí la API utilizando FastAPI, donde cada endpoint realiza una consulta específica en el dataset limpio:

cantidad_filmaciones_mes(mes): Devuelve la cantidad de películas estrenadas en el mes dado.
cantidad_filmaciones_dia(dia): Muestra el número de películas estrenadas en un día específico.
score_titulo(titulo): Proporciona el score y año de estreno de una película.
votos_titulo(titulo): Muestra el total de votos y su promedio (solo si supera las 2000 valoraciones).
get_actor(nombre_actor): Devuelve la cantidad de películas, éxito y retorno promedio de un actor.
get_director(nombre_director): Proporciona detalles de éxito, retorno y lista de películas para un director.
Exploratory Data Analysis (EDA)
Para entender mejor los datos, realicé un análisis exploratorio (EDA), identificando outliers, patrones y tendencias. Utilicé visualizaciones como una nube de palabras que destaca términos comunes en los títulos de las películas, aportando ideas útiles para el modelo de recomendación.

Desarrollo del Sistema de Recomendación
Creé el sistema de recomendación en función de la similitud de puntuación entre películas. Implementé una función recomendacion(titulo) que, al recibir un título, devuelve una lista de las 5 películas más similares en orden de relevancia.

Deployment
La API fue desplegada usando Render (o Railway), permitiendo que cualquier usuario o departamento consuma los datos y recomendaciones directamente desde la web.

Video Demostrativo https://www.youtube.com/watch?v=TfQvQ4QVwS0
Para ilustrar el funcionamiento, realicé un video de 7 minutos que muestra el uso de cada endpoint en la API, junto a una breve explicación del modelo de recomendación.

Este proyecto refleja el proceso completo de MLOps, desde el tratamiento de datos hasta el deployment de un modelo funcional en un entorno de producción.
