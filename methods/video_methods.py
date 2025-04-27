
import cv2


# Получение из входного видео необходимое кол-во кадров
def get_frames(video, fps):
    print("Получаем из входного видео необходимое кол-во кадров")

    # Укажите путь к видео
    video_path = video

    # Загрузка видео
    video = cv2.VideoCapture(video_path)

    # Переменная для отслеживания номера кадра
    frame_count = 0
    frames = []
    while True:
        # Чтение кадра
        ret, frame = video.read()

        # Проверка, удалось ли прочитать кадр
        if not ret:
            break

        # Обработка каждого fps-ного кадра
        if frame_count % fps == 0:
            # Сохранение кадра на компьютере
            # cv2.imwrite(f'frames/frame{frame_count}.jpg', frame)
            frames.append(frame)

        # Увеличение счетчика кадров
        frame_count += 1

    # Освобождение ресурсов
    video.release()
    cv2.destroyAllWindows()

    return frames


# Получение видео из входных кадров
def get_video(frames, fps, name_video, path_video):
    height, width, _ = frames[0].shape
    frame_size = (width, height)

    out = cv2.VideoWriter(
        path_video + name_video,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        frame_size
    )
    for frame in frames:
        out.write(frame)
    out.release()

    print(f"Итоговое видео \"{name_video}\" успешно сохранено по пути \"{path_video}\"")
