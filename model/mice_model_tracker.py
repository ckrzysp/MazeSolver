from ultralytics import YOLO
import cv2
#import ultralytics

#ultralytics.check()
#train2 is 50 epoch
#using the weights best
#last is to resume training
model = YOLO("runs/detect/train2/weights/best.pt")


# ------------------------ photo ------------------------ 
photo = model("testfiles/Training_725.png")
for box in photo[0].boxes:
    x1,y1,x2,y2 = box.xyxy[0]
    print(f"bounding box: ({x1}, {y1} to {x2}, {y2})")
    print(f"location of rat: ({(x2+x1)/2}, {(y2+y1)/2})")
annotated = photo[0].plot()
cv2.imshow("YOLO", annotated)
# the esc button is exit
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

# ------------------------ video ------------------------ 
"""
video = "testfiles/mouse.mp4"
# NOTE: its not the greatest video but it will do for now
cap = cv2.VideoCapture(video)

c = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)
    annotated_frame = results[0].plot()

    cv2.imshow("test mice", annotated_frame)
    #escape key to exit
    if cv2.waitKey(1) == 27:
        break
    #c+=1
cap.release()
cv2.destroyAllWindows()
"""