from flask import Flask, request, render_template, send_file
import os
from imdb_scrap import IMDbReviewAnalyzer

app = Flask(__name__)

def is_valid_imdb_url(url):
    return url.startswith("https://www.imdb.com/title/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    pelicula = request.form['pelicula']
    if not is_valid_imdb_url(pelicula):
        return render_template('index.html', error="El enlace proporcionado no es válido. Por favor, ingrese un enlace válido de IMDb.")
    
    analyzer = IMDbReviewAnalyzer(pelicula)
    analyzer.analizar_opiniones()
    
    # Asegúrate de que la ruta del archivo sea correcta
    file_path = 'opiniones_pelicula_imdb.csv'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "El archivo no se encontró", 404

if __name__ == '__main__':
    app.run(debug=True)
