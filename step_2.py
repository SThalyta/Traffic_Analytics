import supervision as sv
import argparse
import cv2
from ultralytics import YOLO

#definição do modelo
model = YOLO("yolo11n.pt")
box_annotator = sv.BoxAnnotator()

def process(video_file_path):
    frames = sv.get_video_frames_generator(source_path=video_file_path)
    for i, frame in enumerate(frames):

        #cv2.imwrite("frame.png", frame)
        result = model(frame, device='cpu', verbose=False)[0] #lista do que foi detectado
        detections = sv.Detections.from_ultralytics(result)

        annotated_frame = frame.copy()
        annotated_frame = box_annotator.annotate(
            scene=annotated_frame,
            detections=detections
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