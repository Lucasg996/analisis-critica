import os
import re
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd

class IMDbReviewAnalyzer:
    """Clase que se encarga de obtener el HTML de la página de IMDb"""
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def obtener_html(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return None

    def extraer_nombre_pelicula(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('a', itemprop='url')
        if title_tag:
            return title_tag.text.strip()
        return "pelicula_desconocida"

class Sentimiento:
    """Clase para analizar el sentimiento de una opinión"""
    @staticmethod
    def analizar_sentimiento(opinion):
        analysis = TextBlob(opinion)
        if analysis.sentiment.polarity > 0:
            return 'Positiva'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negativa'

class Opiniones(IMDbReviewAnalyzer):
    """Clase para extraer y analizar las opiniones de IMDb"""
    def __init__(self, url):
        super().__init__(url)

    def extraer_opiniones(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.find_all('div', class_='review-container')
        opiniones = []
        for review in reviews:
            username = review.find('span', class_='display-name-link').text.strip()
            opinion_text = review.find('div', class_='text show-more__control').text.strip()
            opiniones.append((username, opinion_text))
        return opiniones

    def analizar_opiniones(self):
        html = self.obtener_html()
        if html:
            opiniones = self.extraer_opiniones(html)
            nombre_pelicula = self.extraer_nombre_pelicula(html)
            self.guardar_en_csv(opiniones, nombre_pelicula)

    def guardar_en_csv(self, opiniones, nombre_pelicula):
        # Sanitizar el nombre de la película para que sea un nombre de archivo válido
        nombre_pelicula = re.sub(r'[\\/*?:"<>|]', "", nombre_pelicula)
        filename = f'{nombre_pelicula}_opiniones.csv'

        # Crear los directorios si no existen
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

        # Generar nuevo nombre si el archivo ya existe
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{extension}"
            counter += 1

        resultados = [(usuario, Sentimiento.analizar_sentimiento(opinion)) for usuario, opinion in opiniones]
        data = {'Usuario': [usuario for usuario, _ in resultados], 'Sentimiento': [sentimiento for _, sentimiento in resultados]}
        df = pd.DataFrame(data)
        df.to_csv(new_filename, index=False)
        print(f"Análisis completado y guardado en {new_filename}")

    
o1 = Opiniones("https://www.imdb.com/title/tt1375666/reviews/?ref_=tt_ql_2")
print(o1.extraer_nombre_pelicula("a"))
