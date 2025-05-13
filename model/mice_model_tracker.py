from ultralytics import YOLO
import cv2
import ultralytics
import argparse
import torch
#ultralytics.check()

# ------------------------ photo ------------------------ 
def detect_object_in_photo(modelName,fileName):
    """
    drawing a boundary box of the detected object in a image

    args:
    modelName (str): model name WITHOUT going to the runs/detect and weights folder
    fileName (str): namee of the file in testfiles/ folder

    returns: photo with box annotation of the object
    """
    model = YOLO('runs/detect/' + modelName + '/weights/best.pt')
    photo = model('testfiles/' + fileName)
    for box in photo[0].boxes:
        x1,y1,x2,y2 = box.xyxy[0]
        print(f"bounding box: ({x1}, {y1} to {x2}, {y2})")
        print(f"location of rat: ({(x2+x1)/2}, {(y2+y1)/2})")
    annotated = photo[0].plot()
    cv2.imshow("YOLO", annotated)
    # the esc button is exit
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

# ------------------------ predict ------------------------ 
def predict_labels(modelName, videoName):
    """
    gives boundary box cordinates of each frame of the video based on the model detection
    args:
    modelName (str): model name WITHOUT going to the runs/detect and weights folder
    fileName (str): namee of the file in testfiles/ folder

    returns: a folder of labels txt files of each frame
    """
    model = YOLO('runs/detect/' + modelName + '/weights/best.pt')
    results = model.predict(source='testfiles/' + videoName, imgsz=640, save=True,save_txt=True)
    for result in results:
        xyxy = boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2] format
        boxes = result.boxes
        with open("test.txt", "w") as file:
            for e in xyxy:
                x1, y1, x2, y2 = e
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                file.write(f'Center: ({cx:.2f}, {cy:.2f}) \n')

# ------------------------ video ------------------------ 
def display_annotation_detect_object(modelName, fileName):
    """
    draw a boundary box for each frame and shows confidence 

    args:
    modelName (str): model name WITHOUT going to the runs/detect and weights folder
    fileName (str): namee of the file in testfiles/ folder

    returns: a video of the object having a boundary box in each frame
    """
    model = YOLO('runs/detect/' + modelName + '/weights/best.pt')
    cap = cv2.VideoCapture('testfiles/' + fileName)
    # c is to keep track of the frame #
    c = 0
    # creates and write of file
    with open("coordinates.txt", "w") as f:
        # while there is a frame left in the video
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            results = model(frame)
            boxes = results[0].boxes
            # if boundary box exist, if the x's and y's exist
            if boxes is not None and boxes.xyxy is not None:
                c = 0
                for box in boxes.xyxy.cpu().numpy():
                    #top left, bottom right
                    x1, y1, x2, y2 = box            
                    # dividing both gets center coordinate of the box
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2

                    # frame x-cord y-cord
                    f.write(f"{c} {cx:.2f} {cy:.2f}\n")
                    c+=1
            # shows frame with the boundary box
            annotated_frame = results[0].plot()
            cv2.imshow("test mice", annotated_frame)

            # escape key to exit
            if cv2.waitKey(1) == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

# has to be in testfiles
choice = input("(1) detect_object_in_photo\n(2) detect_object_in_video\n(3) predict_labels\n")

if(choice == "1"):
    # modelName, ImageName
    model = input("modelName: \n(ex: 'GPU/ant-4070s/train10e' or 'CPU/perfect' )\n")
    image = input("image: (in testfile)\n")
    detect_object_in_photo(model,image)
elif(choice == "2"):
    # modelName, videoName
    model = input("modelName: \n(ex: 'GPU/ant-4070s/train10e' or 'CPU/perfect' )\n")
    video = input("video: (in testfile)\n")
    display_annotation_detect_object(model,video)
elif(choice == "3"):
    # modelName, videoName
    model = input("modelName: \n(ex: 'GPU/ant-4070s/train10e' or 'CPU/perfect' )\n")
    video = input("video: (in testfile)\n")
    predict_labels(model,video)

# if you dont like the inputs just comment them out

# yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=640 device=0
# yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source= testfiles/miceproj.mp4 imgsz=640
# yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source= testfiles/miceproj.mp4  save=True save_txt=True
# yolo task=detect mode=train model=runs/detect/train/weights/best.pt data=data.yaml epochs=50 imgsz=640
