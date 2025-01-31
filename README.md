# Running the model

### first we need to install the following in an order
1) [Python](https://apps.microsoft.com/detail/9pnrbtzxmb4z?hl=en-us&gl=US)
2) [cmake](https://cmake.org/)
3) [Visual Studio for C++](https://visualstudio.microsoft.com/vs/features/cplusplus/)

Make sure that Python and cmake are set correctly as environment variables.

After installing everything we run this command to install face_recognition library and double-check the other libraries as well:
```
pip install dlib face_recognition
```

also run this: 
```
pip install git+https://github.com/ageitgey/face_recognition_models opencv-python numpy mysql-connector-python flask
```

There's a bug where the app asks for the face_modules after already installing them. in that case run:
```
pip install setuptools
```

### Requirements:
Flask==2.3.2
mysql-connector-python==8.0.33
face-recognition==1.3.0
numpy==1.24.3
opencv-python==4.7.0.72
Pillow==9.5.0

### Necessary SQL:
```genericsql
CREATE TABLE IF NOT EXISTS faces (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(255),
          image BLOB,
          encoding BLOB
      )
```