# model

datasets files [Dropbox](https://www.dropbox.com/scl/fo/wd9gvzql5w8d2kxg38gi2/AF5AMotHkhLMNTQ9eVyNRPo?rlkey=q89nz18d0w3cstpk6w4dvrlb2&st=82v3fdtu&dl=0)

1200 images (technically 2200 but the mask is not used for training)
- 1000 Training and mask
- 200 validation

> **Note:** The mask images are used to create and document the box coordinates in a text file used for training. Also making this I realized I didn't compress the images folder into a zip file.

**If you want to try and train it yourself**

1. Download the dataset
- using the Dropbox link
- place folder in the `mode/`
**(Optional: adjusting amount of photos)**
- delete contents in `labels/` for both `train/` and `val/`
- go to `mice_training.py` adjust the for loop based on the image names/ training amount
- run `mice_training.py`

2. Train the model 
It will take a bit depending on how many photos you used 
`yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=480`
- task for detecting object
- mode for training/predicting
- model for the base model
- data is my data.yaml config file
- epochs is how many complete passes 
(for small amount of photos 25-50, large amount 50-100)
- img size is the resolution (for this case 480x480)

3. Running the model
- go to `mice_model_tracker.py`
- adjust code if needed
- run `mice_model_tracker.py`

## problems

- once we get the proper videos, we will need to get frames from it and mask the mouse from those frames, OR we find the area of the mouse, calculate a bounding box based on area and emin/emax and document it in labels as a txt file. the txt file should only be:
`<class_id> <x_center> <y_center> <width> <height>`
example: 0, center of bounding box, and bounding box width and height
all normalized with the range between 0-1 
(all the values combined does not need to be equal to 1)

- The training images that I found did not have any walls, and by running the `testfile/mouse.mp4` you can tell it stops tracking once its very close to a wall

