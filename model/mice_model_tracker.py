from ultralytics import YOLO
import cv2
import ultralytics
import argparse
import torch
#ultralytics.check()

model = YOLO("runs/detect/i1000e25/weights/best.pt")

# ------------------------ photo ------------------------ 
# photo = model("testfiles/Training_725.png")
# for box in photo[0].boxes:
#     x1,y1,x2,y2 = box.xyxy[0]
#     print(f"bounding box: ({x1}, {y1} to {x2}, {y2})")
#     print(f"location of rat: ({(x2+x1)/2}, {(y2+y1)/2})")
# annotated = photo[0].plot()
# cv2.imshow("YOLO", annotated)
# # the esc button is exit
# if cv2.waitKey(0) == 27:
#     cv2.destroyAllWindows()

# ------------------------ predict ------------------------ 

# cap = cv2.VideoCapture("testfiles/miceproj.mp4")
# results = model.predict(source='testfiles/miceproj.mp4', imgsz=640, save=True,save_txt=True)
# for result in results:
#     xyxy = boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2] format
#     boxes = result.boxes
#     with open("test.txt", "w") as file:
#         for e in xyxy:
#             x1, y1, x2, y2 = e
#             cx = (x1 + x2) / 2
#             cy = (y1 + y2) / 2
#             file.write(f'Center: ({cx:.2f}, {cy:.2f}) \n')

# ------------------------ video ------------------------ 

cap = cv2.VideoCapture("./data/in/miceproj.mp4")
frame = 0
c = 0
with open("coordinates.txt", "w") as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        boxes = results[0].boxes

        if boxes is not None and boxes.xyxy is not None:
            c = 0
            for box in boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                # frame x-cord y-cord
                f.write(f"{c} {cx:.2f} {cy:.2f}\n")
                c+=1

        annotated_frame = results[0].plot()
        cv2.imshow("test mice", annotated_frame)

        #escape key to exit
        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()

# yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=640 device=0
# yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source= testfiles/miceproj.mp4 imgsz=640
# yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source= testfiles/miceproj.mp4  save=True save_txt=True
# yolo task=detect mode=train model=runs/detect/train/weights/best.pt data=data.yaml epochs=50 imgsz=640

#predict folder, gives labels from a video 
#train 1 is the most recent train with only blue background mouse
#manual labeling 100 photos
#perfect is train 1 + all prediction of the blue video 50 epoch
#train clean slate, 1000 10 epoch

# old is the old datasets
# next train will be all of the datasets combined

# 1k images 800 training / 200 validation
#train epoch 10
#train 2 epoch 25
#train 3 epoch 50