import requests

def obtener_url_pelicula():
    """
    Solicita al usuario que ingrese la URL de la película en IMDb y la valida.
    """
    while True:
        url = input("Por favor, ingrese el enlace de IMDb de la película que desea analizar: ")
        if validar_url(url):
            return url
        else:
            print("La URL ingresada no es válida. Por favor, inténtelo de nuevo.")

def validar_url(url):
    """
    Valida la URL verificando si devuelve un código de estado HTTP 200 (OK).
    """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False
