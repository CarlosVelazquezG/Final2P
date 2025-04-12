from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5001"  # URL de tu API FastAPI
TMDB_API_KEY = "9511ead905d790c2a81450ffeb3391eb"

# Función para obtener imágenes de TMDB
def obtener_poster(titulo):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": titulo,
        "language": "es-MX"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200 and response.json()["results"]:
            return f"https://image.tmdb.org/t/p/w500{response.json()['results'][0]['poster_path']}"
    except:
        return None

@app.route('/')
def mostrar_catalogo():
    try:
        # Obtener películas de la API
        response = requests.get(f"{API_URL}/peliculas")
        peliculas = response.json() if response.status_code == 200 else []
        
        # Añadir imágenes desde TMDB
        for pelicula in peliculas:
            pelicula["poster"] = obtener_poster(pelicula["title"])
        
        return render_template("catalogo.html", peliculas=peliculas)
    
    except Exception as e:
        return render_template("error.html", error=f"Error: {str(e)}")

@app.route('/pelicula/<int:id>')
def mostrar_detalle(id):
    try:
        # Obtener película de la API
        response = requests.get(f"{API_URL}/peliculas/{id}")
        if response.status_code != 200:
            return redirect(url_for('mostrar_catalogo'))
        
        pelicula = response.json()
        pelicula["poster"] = obtener_poster(pelicula["title"])
        
        return render_template("detalle.html", pelicula=pelicula)
    
    except:
        return redirect(url_for('mostrar_catalogo'))
    
@app.route('/editar', methods=['GET'])
@app.route('/editar/<int:id>', methods=['GET'])
def mostrar_editor(id=None):
    pelicula = None
    if id:
        # Obtener película existente para editar
        response = requests.get(f"{API_URL}/peliculas/{id}")
        if response.status_code == 200:
            pelicula = response.json()
    
    return render_template("editar.html", pelicula=pelicula)

@app.route('/guardar', methods=['POST'])
@app.route('/guardar/<int:id>', methods=['POST'])
def guardar_pelicula(id=None):
    try:
        datos = {
            "title": request.form["title"],
            "genre": request.form["genre"],
            "year": int(request.form["year"]),
            "clss": request.form["clss"]
        }
        
        # Crear o actualizar
        if id:
            response = requests.put(f"{API_URL}/peliculas/{id}", json=datos)
        else:
            response = requests.post(f"{API_URL}/peliculas", json=datos)
        
        response.raise_for_status()
        return redirect(url_for('mostrar_catalogo'))
    
    except Exception as e:
        return render_template("error.html", error=f"Error al guardar: {str(e)}")
    
@app.route('/eliminar/<int:id>')
def eliminar_pelicula(id):
    try:
        response = requests.delete(f"{API_URL}/peliculas/{id}")
        response.raise_for_status()
    except:
        pass  # Manejar error si es necesario
    return redirect(url_for('mostrar_catalogo'))

if __name__ == "__main__":
    app.run(debug=True)