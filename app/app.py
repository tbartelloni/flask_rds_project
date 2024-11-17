
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configuration: Replace with your RDS credentials
DB_HOST = os.getenv("DB_HOST", "your-rds-instance-url")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "your_database_name")
DB_USER = os.getenv("DB_USER", "your_username")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")

# Establish a database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Simple route to check the connection
@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# Example route to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s) RETURNING id;", (name,))
    item_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"id": item_id, "name": name}), 201

# Example route to get an item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items WHERE id = %s;", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if item:
        return jsonify({"id": item[0], "name": item[1]}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

# Example route to update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data.get('name')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = %s WHERE id = %s;", (name, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"id": item_id, "name": name}), 200

# Example route to delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
