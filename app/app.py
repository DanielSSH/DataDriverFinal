from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
import redis 

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


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
        tu_nombre = request.form['tu_nombre']
        celular = request.form['celular']
        placas = request.form['placas']
        nombre_propietario = request.form['nombre_propietario']
        documento_propietario = request.form['documento_propietario']
        email_propietario = request.form['email_propietario']
        email_conductor = request.form['email_conductor']
        motivo_reporte = request.form['motivo_reporte']
        calificacion = request.form.getlist('calificacion')

        if not nombre or not apellido or not cedula or not licencia:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('registro_conductor'))

        conductor_existente = Conductor.query.filter_by(cedula=cedula).first()
        if conductor_existente:
            flash('La cédula ya está registrada.', 'error')
            return redirect(url_for('registro_conductor'))

        nuevo_conductor = Conductor(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            licencia=licencia,
            tu_nombre=tu_nombre,
            celular=celular,
            placas=placas,
            nombre_propietario=nombre_propietario,
            documento_propietario=documento_propietario,
            email_propietario=email_propietario,
            email_conductor=email_conductor,
            motivo_reporte=motivo_reporte,
            calificacion=','.join(calificacion)
        )

        try:
            db.session.add(nuevo_conductor)
            db.session.commit()
            flash('Conductor registrado con éxito.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el conductor: {str(e)}', 'error')

        print(request.form)

        return redirect(url_for('registro_conductor'))

    return render_template('registro.html')


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

