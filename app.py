from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

#ROTA PARA PÁGINA INICIAL
@app.route('/')
def index():
    return render_template('index.html')

# ROTA PARA LISTAR CLIENTES
@app.route('/listar_clientes')
def listar_clientes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    return render_template('listar_clientes.html', clientes=clientes)

#ROTA FORMULÁRIO PARA ADIÇÃO DE CLIENTES
@app.route('/adicionar_cliente')
def adicionar_cliente_form():
    return render_template('adicionar_cliente.html')

# ROTA PARA ADICIONAR UM NOVO CLIENTE 'POST'
@app.route('/adicionar_cliente', methods=['GET','POST'])
def adicionar_cliente():
    if request.method == 'POST':
        nome = request.form['Nome']
        cpf = request.form['CPF']
        telefone = request.form['Telefone']
        email = request.form['Email']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO clientes (Nome, CPF, Telefone, Email) VALUES (%s, %s, %s, %s)", (nome, cpf, telefone, email))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('listar_clientes'))

# ROTA PARA ATUALIZAR UM CLIENTE
@app.route('/editar/<int:id_Cliente>', methods=['GET', 'POST'])
def editar_cliente(id_Cliente):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        nome = request.form['Nome']
        cpf = request.form['CPF']
        telefone = request.form['Telefone']
        email = request.form['Email']
        cursor.execute("UPDATE clientes SET Nome = %s, CPF = %s, Telefone = %s, Email = %s WHERE id_Cliente = %s", (nome, cpf, telefone, email, id_Cliente))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('listar_clientes'))
    else:
        cursor.execute("SELECT * FROM clientes WHERE id_Cliente = %s", (id_Cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        return render_template('editar_cliente.html', cliente=cliente)

# ROTA PARA DELETAR UM CLIENTE
@app.route('/deletar/<int:id_Cliente>')
def deletar_cliente(id_Cliente):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_Cliente = %s", (id_Cliente,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('listar_clientes'))

if __name__ == '__main__':
    app.run(debug=True)
