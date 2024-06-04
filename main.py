from imdb_scrap import IMDbReviewAnalyzer
from utils import obtener_url_pelicula


def main():
    url = input("Por favor, ingrese el enlace de IMDb de la película que desea analizar: ")
    analyzer = IMDbReviewAnalyzer(url)
    analyzer.analizar_opiniones()

if __name__ == '__main__':
    main()