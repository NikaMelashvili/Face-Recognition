import mysql.connector
import pickle

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="main"
    )
    cursor = db.cursor()
    return db, cursor

def save_face_to_db(name, image, encoding):
    db, cursor = get_db_connection()
    encoding_blob = pickle.dumps(encoding)
    cursor.execute("INSERT INTO faces (name, image, encoding) VALUES (%s, %s, %s)",
                   (name, image, encoding_blob))
    db.commit()
    cursor.close()
    db.close()

def load_faces_from_db():
    db, cursor = get_db_connection()
    cursor.execute("SELECT name, encoding FROM faces")
    results = cursor.fetchall()

    known_names = []
    known_encodings = []
    for name, encoding_blob in results:
        known_names.append(name)
        known_encodings.append(pickle.loads(encoding_blob))

    cursor.close()
    db.close()
    return known_names, known_encodings

def check_name_exists_in_db(name):
    db, cursor = get_db_connection()
    try:
        cursor.execute("SELECT 1 FROM faces WHERE name = %s LIMIT 1", (name,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        db.close()

