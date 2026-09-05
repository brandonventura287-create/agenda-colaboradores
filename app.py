from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

ARCHIVO = "colaboradores.txt"


def calcular_edad(fecha_nacimiento):
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()

    edad = hoy.year - fecha_nacimiento.year

    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad


def cargar_colaboradores():
    colaboradores = []

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if linea:
                    datos = linea.split("|")

                    colaborador = {
                        "nombre": datos[0],
                        "apellido": datos[1],
                        "fecha_nacimiento": datos[2],
                        "dia": datos[3]
                    }

                    colaborador["edad"] = calcular_edad(
                        colaborador["fecha_nacimiento"]
                    )

                    colaboradores.append(colaborador)

    except FileNotFoundError:
        pass

    return colaboradores


def resumen_por_dia():
    colaboradores = cargar_colaboradores()

    resumen = {
        "Lunes": 0,
        "Martes": 0,
        "Miércoles": 0,
        "Jueves": 0,
        "Viernes": 0,
        "Sábado": 0,
        "Domingo": 0
    }

    for colaborador in colaboradores:
        dia = colaborador["dia"]

        if dia in resumen:
            resumen[dia] += 1

    return resumen


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    dia = request.form["dia"]

    with open(ARCHIVO, "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{nombre}|{apellido}|{fecha_nacimiento}|{dia}\n"
        )

    return redirect(url_for("colaboradores"))


@app.route("/colaboradores")
def colaboradores():
    lista = cargar_colaboradores()

    return render_template(
        "colaboradores.html",
        colaboradores=lista
    )


@app.route("/resumen")
def resumen():
    datos = resumen_por_dia()

    return render_template(
        "resumen.html",
        resumen=datos
    )


if __name__ == "__main__":
    app.run(debug=True)