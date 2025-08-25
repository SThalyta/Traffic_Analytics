#Contagem de ids únicos na PolygonZone

import supervision as sv
import argparse
import cv2
from ultralytics import YOLO
import numpy as np

#Zona definida com makesense.ai
POLYGON = np.array([
        [296.15091575766513,393.20754716981133],
        [973.886764814269,387.1698113207547],
        [1277.2829912293632,557.7358490566038],
        [1274.264123304835,714.7169811320755],
        [3.3207270784198117,714.7169811320755],
        [0.30185915389150947,510.94339622641513]
    ], dtype=np.int32)

CLASSES = [2, 3, 5, 7]
model = YOLO("yolo11n.pt") #model.names retorna o nome e id das classes treinadas
box_annotator = sv.BoxAnnotator()
polygon_zone = sv.PolygonZone(polygon=POLYGON)
label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK)
tracker = sv.ByteTrack(minimum_consecutive_frames=3)
tracker.reset()
ids = set()
count = 0

def main(video_file_path):
    global count
    frames = sv.get_video_frames_generator(source_path=video_file_path)
    for i, frame in enumerate(frames):
        #cv2.imwrite("frame.png", frame)
        #inferência:processo de extrapolação de novos dados
        #por um modelo de aprendizado de máquina (machine learning) treinado.
        result = model(frame, device='cpu', verbose=False)[0] #lista do que foi detectado
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[polygon_zone.trigger(detections)] #lista com [True, False], o trigger aciona as deteccoes
        detections = detections[np.isin(detections.class_id, CLASSES)]
        detections = tracker.update_with_detections(detections)
        
        for tracker_id in detections.tracker_id:
            if tracker_id not in ids:
                ids.add(tracker_id)
                count += 1

        labels = [f"#{tracker_id}" for tracker_id in detections.tracker_id]

        annotated_frame = frame.copy()
        annotated_frame = sv.draw_polygon(
            scene=annotated_frame,
            polygon=POLYGON,
            color= sv.Color.BLUE,
            thickness= 2
        )
        annotated_frame = box_annotator.annotate(
            scene=annotated_frame,
            detections=detections
        )
        annotated_frame = label_annotator.annotate(
            scene=annotated_frame,
            detections=detections,
            labels=labels
        )
        cv2.putText(
            annotated_frame,
            f"Count: {count}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )
        cv2.imshow("Processed Video", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("t"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_file_path")

    args = parser.parse_args()

    main(args.video_file_path)