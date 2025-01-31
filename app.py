import base64
import threading

import io
from PIL import Image
from flask import Flask, request, jsonify

from database import save_face_to_db, load_faces_from_db, check_name_exists_in_db
from image_face_recognition import encode_face, recognize_faces
from live_recognition import live_face_recognition, stop_face_recognition

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

@app.route('/add_face', methods=['POST'])
def add_face():
    try:
        print(request.files)
        data = request.get_json()

        name = data['name']
        base64_image = data['image']

        print(f"Name: {name}, Image (first 20 chars): {base64_image[:20]}")

        if check_name_exists_in_db(name):
            return jsonify({"message": "Person already exists"}), 409

        img_data = base64.b64decode(base64_image)

        encoding = encode_face(img_data)
        if encoding is not None:
            save_face_to_db(name, img_data, encoding)
            return jsonify({"message": f"{name} added successfully!"}), 200
        else:
            return jsonify({"message": "No face detected in the image"}), 400

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": f"Error: {str(e)}"}), 500


@app.route("/recognize_image", methods=["POST"])
def recognize_image():
    data = request.get_json()

    if "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    base64_image = data["image"]

    try:
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        known_names, known_encodings = load_faces_from_db()
        matches = recognize_faces(img_byte_arr, known_names, known_encodings)

        return jsonify({"matches": matches})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

face_recognition_running = False
face_recognition_thread = None

def live_face_recognition_util():
    global face_recognition_running
    face_recognition_running = True
    while face_recognition_running:
        print("Running face recognition...")

@app.route('/live_recognition', methods=['GET'])
def face_recognition_control():
    global face_recognition_running

    action = request.args.get("action")

    if action == "start" and not face_recognition_running:
        threading.Thread(target=live_face_recognition, daemon=True).start()
        return jsonify({"message": "Live face recognition started"}), 200

    elif action == "stop":
        stop_face_recognition()
        return jsonify({"message": "Live face recognition stopping"}), 200

    return jsonify({"error": "Invalid or redundant action"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)