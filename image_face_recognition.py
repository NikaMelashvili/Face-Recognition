import face_recognition as fr
from io import BytesIO

def encode_face(image_data):
    image = fr.load_image_file(BytesIO(image_data))
    encodings = fr.face_encodings(image)
    return encodings[0] if encodings else None

def recognize_faces(image_data, known_names, known_encodings):
    image = fr.load_image_file(BytesIO(image_data))
    encodings = fr.face_encodings(image)

    matches = []
    for encoding in encodings:
        face_distances = fr.face_distance(known_encodings, encoding)
        best_match_index = min(range(len(face_distances)), key=face_distances.__getitem__)

        if face_distances[best_match_index] < 0.6:
            matches.append(known_names[best_match_index])
        else:
            matches.append("Unknown")

    return matches