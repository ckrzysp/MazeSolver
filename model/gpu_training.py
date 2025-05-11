from ultralytics import YOLO

def train_model():
    model = YOLO("yolov8n.pt")
    model.train(data="data.yaml", epochs=10, imgsz=640, device=0)

if __name__ == "__main__":  # Protect the main entry point
    train_model()