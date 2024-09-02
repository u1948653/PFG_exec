import cv2
import numpy as np
import keras
from collections import deque
import json
import os
import sys


# Verificar que se pasaron argumentos
if len(sys.argv) > 1:
    # sys.argv es una lista donde el primer elemento es el nombre del script
    model_path = sys.argv[1]
else:
    raise Exception("No se ha indicado que modelo utilizar.")

# Cargar el modelo entrenado
model = keras.models.load_model(model_path)

# Definir las dimensiones de entrada esperadas por el modelo
frame_width, frame_height = 128, 128  # Tamaño esperado por el modelo
num_frames = 30  # Número de frames en el buffer

# Buffer para almacenar los frames
frame_buffer = deque(maxlen=num_frames)

# Cargar el diccionario de gestos desde el archivo JSON
try:
    with open(os.path.join(__file__,"..",'encodedTimDataset.json'), 'r', encoding='utf-8-sig') as f:
        gesture_dict = json.load(f)
except FileNotFoundError:
    raise Exception("El archivo gestures.json no se encontró.")
except json.JSONDecodeError:
    raise Exception("Error al decodificar el archivo JSON.")

# Crear un mapeo de índices a etiquetas de gestos
gesture_map = {np.argmax(encoding): gesture for gesture, encoding in gesture_dict.items()}

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

# Obtener la resolución del video
original_width, original_height = int(cap.get(3)), int(cap.get(4))

# Variables para suavizado de predicciones
prediction_buffer = deque(maxlen=10)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el frame a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Redimensionar el frame al tamaño esperado por el modelo
    resized_frame = cv2.resize(gray_frame, (frame_width, frame_height))

    # Normalizar el frame
    normalized_frame = resized_frame.astype('float32')  # / 255.0

    # Añadir una dimensión para los canales (necesario para que coincida con la entrada esperada)
    normalized_frame = np.expand_dims(normalized_frame, axis=-1)

    # Añadir el frame al buffer
    frame_buffer.append(normalized_frame)

    # Hacer predicción solo si el buffer está lleno
    if len(frame_buffer) == num_frames:
        # Convertir el buffer a un array numpy
        frames_array = np.array(frame_buffer)

        # Añadir dimensión de batch
        frames_array = np.expand_dims(frames_array, axis=0)  # Shape: (1, 30, 128, 128, 1)

        # Hacer predicción
        prediction = model.predict(frames_array, verbose=0)

        # Obtener el índice de la clase predicha
        predicted_index = np.argmax(prediction, axis=1)[0]

        # Añadir la predicción al buffer de predicciones
        prediction_buffer.append(predicted_index)

        # Obtener el gesto correspondiente
        predicted_gesture = gesture_map.get(predicted_index, "IGNORE")

        if np.array(prediction)[0][predicted_index] > 0.85:
            # Mostrar la predicción en el marco de video
            cv2.putText(frame, f'Gesto: {predicted_gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                        cv2.LINE_AA)

    # Mostrar el video en tiempo real
    cv2.imshow('Video en tiempo real', frame)
    k = cv2.waitKey(1)
    # Romper el bucle con la tecla 'q'
    if k & 0xFF == ord('q'):
        break

# Liberar los recursos de la cámara y el escritor de video, y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
