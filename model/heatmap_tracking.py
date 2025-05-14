from ultralytics import YOLO
import cv2
import ultralytics
import argparse
import torch
import numpy
#ultralytics.check()

model = YOLO("runs/detect/i1000e25/weights/best.pt")

# Path failure if second dot is not included in the beginning
cap = cv2.VideoCapture("../data/in/miceproj.mp4")
frame = 0
c = 0
coord = []
with open("coordinates.txt", "w") as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        boxes = results[0].boxes

        if boxes is not None and boxes.xyxy is not None:
            c = 0
            annotated_frame = results[0].plot()
            for box in boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                # Appending coordinates
                coord.append(int(cx))
                coord.append(int(cy))

                # Since plots are refresheed every frame, previous coordinates are stored and replotted
                i = 0
                while i < len(coord):
                    x = coord[i]
                    y = coord[i+1]
                    cv2.circle(annotated_frame, (x,y), 2, (0,0,0),-1)
                    i += 2

                # frame x-cord y-cord
                f.write(f"{c} {cx:.2f} {cy:.2f}\n")
                c+=1
        else:
            annotated_frame = frame

        cv2.imshow("test mice", annotated_frame)

        #escape key to exit
        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()
