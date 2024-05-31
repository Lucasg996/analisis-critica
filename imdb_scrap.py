import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd

def obtener_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.content
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return None

def extraer_opiniones(html):
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.find_all('div', class_='text show-more__control')
    opiniones = [review.get_text(strip=True) for review in reviews]
    return opiniones

def analizar_sentimiento(opinion):
    analysis = TextBlob(opinion)
    if analysis.sentiment.polarity > 0:
        return 'Positiva'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negativa'

def guardar_en_csv(resultados, filename='opiniones_pelicula_imdb.csv'):
    # Generar nombres de usuario ficticios o identificadores únicos
    nombres_usuarios = [f'Usuario {i+1}' for i in range(len(resultados))]
    
    # Crear un DataFrame con los nombres de usuario y los resultados del análisis de sentimiento
    data = {'Usuario': nombres_usuarios, 'Sentimiento': resultados}
    df = pd.DataFrame(data)
    
    # Guardar solo el nombre de usuario y el sentimiento en el archivo CSV
    df.to_csv(filename, columns=['Usuario', 'Sentimiento'], index=False)
    print(f"Análisis completado y guardado en {filename}")

def main():
    imdb_link = input("Por favor, ingrese el enlace de IMDb de la película que desea analizar: ")
    html = obtener_html(imdb_link)
    if html:
        opiniones = extraer_opiniones(html)
        resultados = [analizar_sentimiento(opinion) for opinion in opiniones]
        guardar_en_csv(resultados)

if __name__ == '__main__':
    main()
