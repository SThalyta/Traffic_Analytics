#Separação de zonas (entrada e saída de veículos)
import supervision as sv
import argparse
import cv2
from ultralytics import YOLO
import numpy as np

POLYGON_1 = np.array([
        [4.830161040683962,483.7735849056604],
        [327.8490289652123,353.96226415094344],
        [610.1131799086086,361.50943396226415],
        [563.3207270784198,717.7358490566038],
        [0.30185915389150947,713.2075471698114]
    ], dtype=np.int32)

POLYGON_2 = np.array([
        [1008.6037459463444,381.13207547169816],
        [1277.2829912293632,494.3396226415095],
        [1275.7735572670992,716.2264150943397],
        [733.8867648142689,719.245283018868],
        [655.3961987765331,381.13207547169816]
    ], dtype=np.int32)

CLASSES = [2, 3, 5, 7]
model = YOLO("yolo11n.pt") #model.names retorna o nome e id das classes treinadas
box_annotator = sv.BoxAnnotator()
polygon_zone_1 = sv.PolygonZone(polygon=POLYGON_1)
tracker_1 = sv.ByteTrack(minimum_consecutive_frames=5)
tracker_1.reset()
ids_1 = set()
count_1 = 0

polygon_zone_2 = sv.PolygonZone(polygon=POLYGON_2)
tracker_2 = sv.ByteTrack(minimum_consecutive_frames=4) 
tracker_2.reset()
ids_2 = set()
count_2 = 0

label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK)

def process(video_file_path):
    global count_1
    global count_2
    frames = sv.get_video_frames_generator(source_path=video_file_path)
    for i, frame in enumerate(frames):
        #cv2.imwrite("frame.png", frame)
        #inferência:processo de extrapolação de novos dados
        #por um modelo de aprendizado de máquina (machine learning) treinado.
        result = model(frame, device='cpu', verbose=False)[0] #lista do que foi detectado
        detections = sv.Detections.from_ultralytics(result)
        detections_1 = detections[polygon_zone_1.trigger(detections)] #lista com [True, False], o trigger aciona as deteccoes
        detections_1 = detections_1[np.isin(detections_1.class_id, CLASSES)]
        detections_1 = tracker_1.update_with_detections(detections_1)

        detections_2 = detections[polygon_zone_2.trigger(detections)] #lista com [True, False], o trigger aciona as deteccoes
        detections_2 = detections_2[np.isin(detections_2.class_id, CLASSES)]
        detections_2 = tracker_2.update_with_detections(detections_2)
        
        for tracker_id in detections_1.tracker_id:
            if tracker_id not in ids_1:
                ids_1.add(tracker_id)
                count_1 += 1

        for tracker_id in detections_2.tracker_id:
            if tracker_id not in ids_2:
                ids_2.add(tracker_id)
                count_2 += 1

        labels_1 = [f"#{tracker_id}" for tracker_id in detections_1.tracker_id]
        labels_2 = [f"#{tracker_id}" for tracker_id in detections_2.tracker_id]

        annotated_frame = frame.copy()
        annotated_frame = sv.draw_polygon(
            scene=annotated_frame,
            polygon=POLYGON_1,
            color= sv.Color.BLUE,
            thickness= 2
        )
        annotated_frame = sv.draw_polygon(
            scene=annotated_frame,
            polygon=POLYGON_2,
            color= sv.Color.BLUE,
            thickness= 2
        )
        annotated_frame = box_annotator.annotate(
            scene=annotated_frame,
            detections=detections_1
        )
        annotated_frame = box_annotator.annotate(
            scene=annotated_frame,
            detections=detections_2
        )
        annotated_frame = label_annotator.annotate(
            scene=annotated_frame,
            detections=detections_1,
            labels=labels_1
        )
        annotated_frame = label_annotator.annotate(
            scene=annotated_frame,
            detections=detections_2,
            labels=labels_2
        )
        cv2.putText(
            annotated_frame,
            f"Count_in: {count_1}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2
        )
        cv2.putText(
            annotated_frame,
            f"Count_out: {count_2}",
            (1000, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2
        )
        cv2.imshow("Processed Video", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("t"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_file_path", required= True, help='Caminho para o arquivo')

    args = parser.parse_args()

    process(args.video_file_path) 