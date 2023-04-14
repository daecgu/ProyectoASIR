from flask import Flask

# Creamos una instancia Flask que se llama app
app = Flask(__name__)


@app.route("/")
def hola():
    # return "<h1 style='color:blue'> Este test Funciona! </h1>" para la prueba inicial.
    return "<h1 style='color:green'> Funciona gunicorn! </h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
