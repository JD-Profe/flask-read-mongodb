from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar la app
app = Flask(__name__)

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["sample_mflix"]
collection = db["movies"]

@app.route("/")
def index():
    # Paginación
    page = int(request.args.get("page", 1))
    per_page = 10
    skip = (page - 1) * per_page

    # Leer los documentos
    movies = collection.find({}, {"title": 1, "year": 1, "plot": 1, "_id": 0}).skip(skip).limit(per_page)

    # Convertimos el cursor en lista
    movie_list = list(movies)

    return render_template("index.html", movies=movie_list, current_page=page)

if __name__ == "__main__":
    app.run(debug=True)
