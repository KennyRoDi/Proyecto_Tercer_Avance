from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():

    participantes = obtener_participantes()
    apartados = obtener_apartados()
    comentarios = obtener_comentarios()

    return render_template ('Index.html', participantes = participantes, apartados = apartados, comentarios = comentarios)

def obtener_participantes():

    # Aquí es donde obtienes los participantes generados por el código Python
    return ["Participante 1", "Participante 2", "Participante 3"]

def obtener_apartados():

    # Aquí es donde obtienes los apartados y sus puntos generados por el código Python
    return [
        {
            'nombre': 'Apartado 1',
            'puntos': ["Punto 1", "Punto 2", "Punto 3"]
        },
        {
            'nombre': 'Apartado 2',
            'puntos': ["Punto 1", "Punto 2"]
        },
        {
            'nombre': 'Apartado 3',
            'puntos': []
        }
    ]

def obtener_comentarios():

    # Aquí es donde obtienes los comentarios generados por el código Python
    return ["Comentario 1", "Comentario 2"]

if __name__ == '__main__':
    app.run()