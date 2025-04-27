import cv2
import os
import copy
from ultralytics import YOLO

from methods.face_and_eyes_methods import show_face_and_eyes
from methods.video_methods import get_frames
from build_settings import resource_path


basedir = (os.path.dirname(os.path.dirname(__file__)))  # путь к базовой папке

# Используем YOLOv9m как быструю модель для детекции объектов
model = YOLO(resource_path(os.path.join(basedir, "Resources", "yolov9m.pt")))  # можно заменить на другие версии
# Определение классов, которые будут иметь приоритет при поиске по изображению
classes_to_look_for = ["person", "cell phone"]  # поиск человека и мобильного телефона
# Индексы классов в COCO: person = 0, cell phone = 67
classes_indices = [0, 67]

frame_now = None
count_involve_students = 0
count_distracte_students = 0
count_ignore_students = 0
count_cell_phone = 0


def start_image_object_detection(frame, parameters_recognition):
    """
    Обрабатывает кадр и выполняет детекцию объектов
    :параметр frame: входной кадр
    :параметр parameters_recognition: параметры распознавания
    :возвращает: обработанный кадр с выделенными объектами
    """
    try:
        # Применение детекции объектов YOLO к кадру
        frame = apply_yolo_object_detection(frame, parameters_recognition)
        return frame
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Ошибка при обработке кадра: {e}")
        return frame


def apply_yolo_object_detection(image_to_process, parameters_recognition):
    """
    Распознавание и определение координат объектов на изображении
    :параметр image_to_process: исходное изображение
    :параметр parameters_recognition: параметры распознавания
    :возвращает: изображение с отмеченными объектами
    """
    global count_involve_students, count_distracte_students, count_ignore_students, count_cell_phone

    # Сброс счетчиков для текущего кадра
    count_involve_students = 0
    count_distracte_students = 0
    count_ignore_students = 0
    count_cell_phone = 0

    # Используем модель YOLO для обнаружения объектов
    # Указываем только нужные классы и устанавливаем порог уверенности
    results = model.predict(
        image_to_process,
        classes=classes_indices,  # Только person и cell phone
        conf=0.3,  # Порог уверенности 0.3
        verbose=False  # Отключаем вывод в консоль
    )

    # Обработка результатов
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Получаем класс
            cls = int(box.cls[0])
            class_name = model.names[cls]

            # Получаем координаты
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Преобразуем в numpy и убедимся, что не на GPU
            x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)  # Преобразуем в xywh

            # Рисуем объект
            image_to_process = draw_object_bounding_box(
                image_to_process,
                class_name,
                [x, y, w, h],
                parameters_recognition
            )

    return image_to_process


def draw_object_bounding_box(final_image, class_name, box, parameters_recognition):
    """
    Рисование границ объектов и определение статуса слушателя
    :параметр final_image: исходное изображение
    :параметр class_name: имя класса
    :параметр box: координаты области вокруг объекта [x, y, w, h]
    :параметр parameters_recognition: параметры распознавания
    :return: изображение с отмеченными объектами
    """
    global frame_now
    global count_involve_students
    global count_distracte_students
    global count_ignore_students
    global count_cell_phone

    x, y, w, h = box

    # Проверяем границы изображения
    h_img, w_img = frame_now.shape[:2]
    x = max(0, x)
    y = max(0, y)
    w = min(w, w_img - x)
    h = min(h, h_img - y)

    # Проверка валидности региона
    if w <= 0 or h <= 0:
        return final_image

    # Инициализация переменных для статуса слушателя
    face_w, face_h = 0, 0
    lefteye, righteye = [], []
    left_EAR, right_EAR = 0, 0

    # Получение характеристик человека
    if class_name == "person":
        try:
            region = frame_now[y:y + h, x:x + w]
            if region.size > 0:  # Проверка на пустой регион
                (face_x, face_y, face_w, face_h, lefteye, righteye, left_EAR, right_EAR) = show_face_and_eyes(region)

                if parameters_recognition["show_face"]:
                    # Выделение лица человека
                    if face_w != 0 and face_h != 0:
                        start = (x + face_x, y + face_y)
                        end = (x + face_x + face_w, y + face_y + face_h)
                        color = (255, 255, 255)
                        width = 2
                        final_image = cv2.rectangle(final_image, start, end, color, width)

                if parameters_recognition["show_eyes"]:
                    # Выделение левого глаза человека
                    if len(lefteye) > 0:
                        for i in lefteye:
                            start = (x + i[0], y + i[1])
                            end = (x + i[0] + 1, y + i[1] + 1)
                            color = (255, 0, 255)
                            width = 2
                            final_image = cv2.rectangle(final_image, start, end, color, width)

                    # Выделение правого глаза человека
                    if len(righteye) > 0:
                        for i in righteye:
                            start = (x + i[0], y + i[1])
                            end = (x + i[0] + 1, y + i[1] + 1)
                            color = (255, 0, 255)
                            width = 2
                            final_image = cv2.rectangle(final_image, start, end, color, width)
        except Exception as e:
            print(f"Ошибка при обработке лица/глаз: {e}")

    # Выделение силуэта человека или мобильного телефона
    start = (x, y)
    end = (x + w, y + h)

    if class_name == "person":
        status_student = get_status_student(face_w, face_h, lefteye, righteye, left_EAR, right_EAR)

        if status_student == "INVOLVE":
            color = (0, 255, 0)
            count_involve_students += 1
        elif status_student == "DISTRACTE":
            color = (0, 255, 255)
            count_distracte_students += 1
        elif status_student == "IGNORE":
            color = (0, 0, 255)
            count_ignore_students += 1

        width = 2

    elif class_name == "cell phone":
        color = (255, 0, 0)
        width = 5
        count_cell_phone += 1

    # Рисуем прямоугольник вокруг объекта, если соответствующий параметр включен
    if (parameters_recognition["show_students"] and class_name == "person") or (
            parameters_recognition["show_cell_phone"] and class_name == "cell phone"):
        final_image = cv2.rectangle(final_image, start, end, color, width)

    return final_image


def get_status_student(face_w, face_h, lefteye, righteye, left_EAR, right_EAR):
    """
    Определяет статус слушателя на основе наличия и характеристик лица, и глаз
    :параметр face_w: ширина лица
    :параметр face_h: высота лица
    :параметр lefteye: координаты левого глаза
    :параметр righteye: координаты правого глаза
    :параметр left_EAR: соотношение открытости левого глаза
    :параметр right_EAR: соотношение открытости правого глаза
    :return: статус студента (INVOLVE, DISTRACTE, IGNORE)
    """
    status_student = "INVOLVE"  # ВОВЛЕЧЁН

    if len(lefteye) == 0 or len(righteye) == 0 or left_EAR < 0.4 or right_EAR < 0.4:
        status_student = "DISTRACTE"  # ОТВЛЕКАЕТСЯ

    if face_h == 0 or face_w == 0:
        status_student = "IGNORE"  # ИГНОРИРУЕТ

    return status_student


def start_recognition(input_video_path, need_fps, GUI_signals, parameters_recognition):
    """
    Выполняет распознавание объектов в видео и отправляет результаты через GUI сигналы
    :параметр input_video_path: путь к входному видео
    :параметр need_fps: желаемая частота кадров
    :параметр GUI_signals: сигналы для обновления GUI
    :параметр parameters_recognition: параметры распознавания
    """
    global frame_now
    global count_involve_students
    global count_distracte_students
    global count_ignore_students
    global count_cell_phone

    # Получаем кадры из видео
    input_frames = get_frames(input_video_path, need_fps)
    total_frames = len(input_frames)

    for i in range(total_frames):
        # Сохраняем текущий кадр
        frame_now = copy.deepcopy(input_frames[i])

        # Обработка кадра
        output_frame = start_image_object_detection(frame_now, parameters_recognition)

        # Отправка результатов через GUI сигналы
        GUI_signals["add_results_signal"].emit(count_involve_students, count_distracte_students, count_ignore_students,
                                               count_cell_phone)
        GUI_signals["add_frame_signal"].emit(output_frame)
        GUI_signals["update_progress_signal"].emit(i + 1, total_frames)

        print(f"Обработано {i + 1}/{total_frames} кадров")
