from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Zonapets12345*'
app.config['MYSQL_DB'] = 'dbdatadriver'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/resultado_busqueda', methods=['GET', 'POST'])
def consultar_conductor():
    conductor = None
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        
        if cedula:
            try:
                cursor = mysql.connection.cursor(DictCursor)
                cursor.execute("SELECT * FROM conductores WHERE cedula = %s", (cedula,))
                conductor = cursor.fetchone()  
                cursor.close()
            except Exception as ex:
                print(f"Error: {ex}")
                return redirect(url_for('index'))  # Redirigir en caso de error para evitar que el usuario vea un error en bruto
    print(conductor)
    return render_template('resultado_busqueda.html', conductor=conductor)


@app.route('/registro', methods=['GET', 'POST'])
def registro_conductor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        licencia = request.form['licencia']

        if not nombre or not apellido or not cedula or not licencia:
            Flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('registro_conductor'))

        conductor_existente = Conductor.query.filter_by(cedula=cedula).first()
        if conductor_existente:
            Flash('La cédula ya está registrada.', 'error')
            return redirect(url_for('registro_conductor'))

        nuevo_conductor = Conductor(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            licencia=licencia
        )

        try:
            db.session.add(nuevo_conductor)
            db.session.commit()
            flash('Conductor registrado con éxito.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el conductor: {str(e)}', 'error')

       
        return redirect(url_for('registro.html'))

    return render_template('registro.html')


@app.before_request
def before_request():
    print("Antes de la petición...")

@app.after_request
def after_request(response):
    print("Después de la petición...")
    return response

@app.route('/')
def index():
    cursos = ['PHP', 'Python', 'Java', 'Kotlin', 'Dart', 'JavaScript']
    data = {
        'titulo': 'DATA DRIVER',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_conductores': len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

@app.route('/conductores')
def listar_conductores():
    data = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT cedula, nombres, apellidos, licencia FROM conductores"
        cursor.execute(sql)
        conductores = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data['conductores'] = [dict(zip(columns, row)) for row in conductores]
        data['mensaje'] = 'Éxito'
        cursor.close()
    except Exception as ex:
        print(f"Error: {ex}")
        data['mensaje'] = 'Error'
    print(data)
    return jsonify(data)

@app.route('/query_string')
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"

def pagina_no_encontrada(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,port=5000)

