from ultralytics import YOLO
import os
import cv2

# This whole file essentially is testing and using the mask images to create boundary boxes locations (txt file) for training

def mask_to_yolo_box(mask_path,img_width,img_height):
    """
    Converting the mask from the datasets to YOLO box, allowing us to get the bounding box to localize the mice

    args:
    mask_path (str): grayscale mask image, object is gray and background is black
    img_width (int): the width of the image
    img_height (int): the height of the image

    returns: box annotations text file
    """
    #loads mask image
    mask = cv2.imread(mask_path,cv2.IMREAD_GRAYSCALE)

    #find the outlines of the mask
    #RETR_EXTERNAL - returns outer contour 
    #CHAIN_APPROX_SIMPLE - simplify the contours
    contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #stores boundaries of an object (txt file)
    annotations = []

    for c in contours:
        #grabbing values
        x,y,w,h = cv2.boundingRect(c)

        #normalize
        x_center = (x+w/2)/img_width
        y_center = (y+h/2)/img_height

        norm_w = w/img_width
        norm_h = h/img_height

        annotations.append(f"0 {x_center} {y_center} {norm_w} {norm_h}")

    return annotations

# ------------------------ testing ------------------------ 
# def draw_yolo_bounding_box(img_path,label_path):
#     """
#     drawing the annotations(boundaing box) around the mouse on a copy image (temporary)

#     args:
#     img_path (str): the grayscale image
#     label_path (str): the annotations text file 
    
#     return: a copy image with boundary box
#     """
#     image = cv2.imread(img_path)
#     image_copy = image.copy()
#     h,w = image.shape[:2]
#     #open label file (should be Class_id x_center y_center width height)
#     with open(label_path,'r') as f:
#         for line in f.readlines():
#             p = line.strip().split()
#             id = int(p[0])
#             #convert normalized values into pixel values
#             x_center = float(p[1]) * w
#             y_center = float(p[2]) * h
#             box_width = float(p[3]) * w
#             box_height = float(p[4]) * h
#             #calculate corners of bounding box
#             x1 = int(x_center - box_width / 2) - 5
#             y1 = int(y_center - box_height / 2) - 5
#             x2 = int(x_center + box_width / 2) + 5
#             y2 = int(y_center + box_height / 2) + 5

#             #draw bounding box on image
#             cv2.rectangle(image_copy,(x1,y1),(x2,y2),(255,255,255),2)
#             cv2.imshow('image with bounding box', image_copy)
#             #gets rid of displayed image
#             # waits for 3 seconds
#             cv2.waitKey(3000)
#             cv2.destroyAllWindows


# ------------------------ converting information into txt ------------------------ 
# train folder
for i in range(1,1001):
    m = f'datasets/train/masks/Training_{i}.png'
    img_path = f'datasets/train/images/Training_{i}.png'
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    annotations = mask_to_yolo_box(m,w,h)
    with open(f'datasets/train/labels/Training_{i}.txt',"w") as f:
        for ann in annotations:
            f.write(ann + "\n")
# val folder
for i in range(1001,1201):
    m = f'datasets/val/masks/Training_{i}.png'
    img_path = f'datasets/val/images/Training_{i}.png'
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    annotations = mask_to_yolo_box(m,w,h)
    with open(f'datasets/val/labels/Training_{i}.txt',"w") as f:
        for ann in annotations:
            f.write(ann + "\n")

#draw_yolo_bounding_box("datasets/val/images/Training_100.png","datasets/val/labels/image_100.txt")
# 0 0.4427083333333333 0.21979166666666666 0.13125 0.18541666666666667

# ------------------------ code ------------------------ 
# yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=480
#task for detecting object
#mode for training/predicting
#model for the base model
#data is my data.yaml config file
#epochs is how many complete passes
#img size is the resolution (for this case 480x480)