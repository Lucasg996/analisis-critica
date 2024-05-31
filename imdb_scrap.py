import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd

class IMDbReviewAnalyzer:
    def __init__(self, url):
        """
        Inicializa el objeto IMDbReviewAnalyzer con la URL de la película en IMDb.
        """
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def obtener_html(self):
        """
        Obtiene el HTML de la página de opiniones de la película en IMDb.
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  
            return response.content
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return None

    def extraer_opiniones(self, html):
        """
        Extrae las opiniones de la página HTML y devuelve una lista de tuplas que contienen el nombre de usuario y la opinión.
        """
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.find_all('div', class_='review-container')
        opiniones = []
        for review in reviews:
            username = review.find('span', class_='display-name-link').text.strip()
            opinion_text = review.find('div', class_='text show-more__control').text.strip()
            opiniones.append((username, opinion_text))
        return opiniones

    def analizar_sentimiento(self, opinion):
        """
        Analiza el sentimiento de una opinión utilizando TextBlob y devuelve 'Positiva', 'Neutral' o 'Negativa'.
        """
        analysis = TextBlob(opinion)
        if analysis.sentiment.polarity > 0:
            return 'Positiva'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negativa'

    def guardar_en_csv(self, opiniones, filename='opiniones_pelicula_imdb.csv'):
        """
        Analiza las opiniones y guarda los resultados en un archivo CSV con el nombre de usuario y el sentimiento de la opinión.
        """
        resultados = [(usuario, self.analizar_sentimiento(opinion)) for usuario, opinion in opiniones]
        data = {'Usuario': [usuario for usuario, _ in resultados], 'Sentimiento': [sentimiento for _, sentimiento in resultados]}
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Análisis completado y guardado en {filename}")

    def analizar_opiniones(self):
        """
        Realiza todo el proceso de análisis de opiniones.
        """
        html = self.obtener_html()
        if html:
            opiniones = self.extraer_opiniones(html)
            self.guardar_en_csv(opiniones)

def main():
    url = input("Por favor, ingrese el enlace de IMDb de la película que desea analizar: ")
    analyzer = IMDbReviewAnalyzer(url)
    analyzer.analizar_opiniones()

if __name__ == '__main__':
    main()
