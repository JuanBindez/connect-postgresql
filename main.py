from flask import Flask, jsonify, request, render_template, redirect, url_for
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
@app.route("/postgre_verify")
def postgre_verify():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"PostgreSQL Version": db_version})
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

@app.route("/")
def home():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("view_users.html", users=users)
    else:
        return jsonify({"error": "Falha ao conectar ao banco de dados"}), 500


@app.route("/add_user_form")
def add_user_form():
    return render_template('add_user.html')

@app.route("/add_user_form", methods=["POST"])
def add_user():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        name = request.form['name']
        email = request.form['email']
        
        try:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
                (name, email)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('home'))
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": f"Erro ao adicionar usuário: {e}"}), 400
    else:
        return jsonify({"error": "Falha ao conectar ao banco de dados"}), 500

@app.route("/delete_user/<int:user_id>", methods=["GET"])
def delete_user(user_id):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            if cur.rowcount > 0:
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('home'))
            else:
                cur.close()
                conn.close()
                return jsonify({"message": "Usuário não encontrado"}), 404
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": f"Erro ao deletar usuário: {e}"}), 400
    else:
        return jsonify({"error": "Falha ao conectar ao banco de dados"}), 500

if __name__ == "__main__":
    app.run(debug=True)
