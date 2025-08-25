import supervision as sv
import argparse
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

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

polygon_zone_1 = sv.PolygonZone(polygon=POLYGON_1)
polygon_zone_2 = sv.PolygonZone(polygon=POLYGON_2)
box_annotator = sv.BoxAnnotator()

def process(video_file_path):
    frames = sv.get_video_frames_generator(source_path=video_file_path)
    for i, frame in enumerate(frames):

        result = model(frame, device='cpu', verbose=False)[0] #lista do que foi detectado
        detections = sv.Detections.from_ultralytics(result)
        detections_1 = detections[polygon_zone_1.trigger(detections)]
        detections_2 = detections[polygon_zone_2.trigger(detections)]

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

        cv2.imshow("Processed Video", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("t"):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_file_path", required= True, help='Caminho para o arquivo')

    args = parser.parse_args()

    process(args.video_file_path) 