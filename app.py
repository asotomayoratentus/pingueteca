from flask import Flask, render_template, request
import sqlite3, random

app = Flask(__name__)

def get_random_libro():
    conn = sqlite3.connect('pingueteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM libro")
    ids = [row['id'] for row in cursor.fetchall()]
    if not ids:
        return None
    random_id = random.choice(ids)
    cursor.execute("SELECT * FROM libro WHERE id = ?", (random_id,))
    libro = cursor.fetchone()
    conn.close()
    return libro

def buscar_libros(palabra):
    conn = sqlite3.connect('pingueteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT * FROM libro
        WHERE titulo LIKE ? OR autor LIKE ? OR descripcion LIKE ?
    """
    like = f"%{palabra}%"
    cursor.execute(query, (like, like, like))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def listar_libros_disponibles():
    conn = sqlite3.connect('pingueteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT * FROM libro
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.route('/', methods=['GET', 'POST'])
def index():
    libro_destacado = get_random_libro()
    resultados = []
    filtro = request.args.get('filtro')
    palabra = request.args.get('q')

    if palabra:
        resultados = buscar_libros(palabra)
    elif filtro:
        conn = sqlite3.connect('pingueteca.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libro WHERE genero LIKE ?", (f"%{filtro}%",))
        resultados = cursor.fetchall()
        conn.close()
    return render_template('index.html', libro=libro_destacado, resultados=resultados)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
