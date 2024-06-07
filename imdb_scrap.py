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
        self.soup = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    # Metodo para parsear el HTML
    def obtener_html(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')  # Asignar la instancia de BeautifulSoup a self.soup
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            self.soup = None

    def extraer_nombre_pelicula(self):
        title_tag = self.soup.find('a', itemprop='url')
        return title_tag.text.strip() if title_tag else "pelicula_desconocida"

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
    """Clase para extraer, analizar y guardar las opiniones de IMDb"""
    def __init__(self, url):
        super().__init__(url)

    # Metodo para extraer las opiniones del HTML
    def extraer_opiniones(self):
        reviews = self.soup.find_all('div', class_='review-container')
        opiniones = []
        for review in reviews:
            username = review.find('span', class_='display-name-link').text.strip()
            opinion_text = review.find('div', class_='text show-more__control').text.strip()
            opiniones.append((username, opinion_text))
        return opiniones

    def analizar_opiniones(self):
        self.obtener_html()  # Obtener y parsear el HTML
        if self.soup:
            opiniones = self.extraer_opiniones()
            nombre_pelicula = self.extraer_nombre_pelicula()
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