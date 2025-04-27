
# https://www.geeksforgeeks.org/eye-blink-detection-with-opencv-python-and-dlib/

import os
import cv2  # для рендеринга видео
import dlib  # для определения лиц и ориентиров
import imutils
from scipy.spatial import distance as dist		# для вычисления расстояния между ориентирами для глаз
from imutils import face_utils		# для получения идентификаторов ориентиров левого и правого глаз

from build_settings import resource_path


basedir = (os.path.dirname(os.path.dirname(__file__)))  # путь к базовой папке

# Функция, вычисляющая EAR
def calculate_EAR(eye):
    # Вычисление расстояния по вертикали
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])

    # Вычисление расстояния по горизонтали
    x1 = dist.euclidean(eye[0], eye[3])

    # Вычисление EAR
    EAR = (y1 + y2) / x1
    return EAR


blink_thresh = 0.45
succ_frame = 2
count_frame = 0

# Ориентиры для глаз
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

# Инициализация моделей для ориентиров и распознавания лиц
detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor(resource_path(os.path.join(basedir, "Resources", "shape_predictor_68_face_landmarks.dat")))


def show_face_and_eyes(frame):
    face_x = face_y = face_w = face_h = koef_width = left_EAR = right_EAR = 0
    lefteye = righteye = []

    try:
        # Получение длины и ширины кадра
        start_height, start_width, _ = frame.shape
        koef_width = start_width / 640

        frame = imutils.resize(frame, width=640)

        # Преобразование кадра в серую шкалу для передачи в детектор
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Распознание лиц
        faces = detector(img_gray)
        for face in faces:

            # Обнаружение ориентира
            shape = landmark_predict(img_gray, face)

            # Преобразование списка в (x,y) координаты
            shape = face_utils.shape_to_np(shape)

            # Анализ списка ориентиров для извлечения ориентиров левого и правого глаза
            lefteye = shape[L_start: L_end]
            righteye = shape[R_start:R_end]

            # Отображение левого глаза
            for i in lefteye:
                cv2.rectangle(frame, (i[0], i[1]), (i[0] + 1, i[1] + 1), (255, 0, 255), 2)
            # Отображение правого глаза
            for i in righteye:
                cv2.rectangle(frame, (i[0], i[1]), (i[0] + 1, i[1] + 1), (255, 0, 255), 2)

            # Вычисление EAR
            left_EAR = calculate_EAR(lefteye)
            right_EAR = calculate_EAR(righteye)

            (face_x, face_y, face_w, face_h) = face_utils.rect_to_bb(face)  # получаем координаты лица
            cv2.rectangle(frame, (face_x, face_y), (face_x + face_w, face_y + face_h), (255, 255, 255), 2)  # отображаем на кадре лицо
            cv2.putText(frame, "left_EAR: " + str(left_EAR), (30, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, "right_EAR: " + str(right_EAR), (30, 130), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

        # cv2.imshow("person", frame)
        # cv2.waitKey(0)

    except Exception as e:
        print(e)

    face_x = int(face_x*koef_width)
    face_y = int(face_y*koef_width)
    face_w = int(face_w*koef_width)
    face_h = int(face_h*koef_width)
    for i in range(len(lefteye)):
        lefteye[i][0] *= koef_width
        lefteye[i][1] *= koef_width
    for i in range(len(righteye)):
        righteye[i][0] *= koef_width
        righteye[i][1] *= koef_width

    return face_x, face_y, face_w, face_h, lefteye, righteye, left_EAR, right_EAR
