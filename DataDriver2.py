from flask import Flask, app, render_template, request, redirect, url_for
from Conexiondb import *  



application = app

@app.route('/', methods=['GET','POST'])
def inicio():
    return render_template('index.html')
      
      

@app.route('/buscar-conductor', methods=['GET','POST'])
def BuscarConductor():
    if request.method    == "POST":
        search           = request.form['buscar']
        conexion_MySQLdb = conexiondb() 
        cur      = conexion_MySQLdb.cursor(dictionary=True)
        querySQL = cur.execute("SELECT * FROM conductores WHERE nombre='%s' ORDER BY id  DESC" % (search,))
        resultadoBusqueda = cur.fetchone()  
        cur.close() 
        conexion_MySQLdb.close() 
        return render_template('index.html', miData = resultadoBusqueda, busqueda = search)
    return redirect(url_for('inicio'))  
   


@app.errorhandler(404)
def not_found(error):
        return redirect(url_for('inicio'))
    
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)