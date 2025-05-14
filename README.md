## Survival of the Mice

We developed a model that uses the YOLOv8n object detection algorithm to track mice in a maze. The project initially aimed to analyze mouse behavior in experimental setups. However, due to limitations in behavioral label quality and complexity in modeling nuanced actions, we pivoted to focus on evaluating the performance of the detection model itself. This included assessing model accuracy, training efficiency, and the impact of dataset size and augmentation on performance. Our approach highlights the practicality and limitations of lightweight CNN models like YOLOv8n in constrained research settings.

## Model
[dataset: soon](https://github.com/ckrzysp/MazeSolver/tree/main/model)

- 1000 images 
  - 800 Training
  - 200 validation

A Computer Vision project that can identify mice and track them while avoiding obstacles in a maze!

## Requirements
- Python 3.8 - 3.10
  (11 and 12 have worked but are **not recommended**)

## Tools and Technologies
- OpenCV
- PyTorch (with CUDA support)
- Ultralytics Library
- YOLOv8n
- LabelStudio
- FFMPEG
- Matplotlib
- Pandas

## Steps

### 1. Download the requirements

- In `MazeSolver/` go to your terminal and enter  
`pip install -r requirements.txt`

### If you have a nvidia graphics card
- `pip uninstall torch torchvision`
- `pip install -r cuda-requirements.txt`
- if torchaudio does not install, thats fine

### 2. Download the dataset
- place folder in the `mode/`
- make sure you have txt files in `label/`

### 3. Train the model
- It will take a bit depending on how many photos you used and computer performance
- (CPU)
  - `yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=480`
- (GPU)
  - `yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=480 device=0`
    - task for detecting object
    - mode for training/predicting
    - model for the base model
    - data is my data.yaml config file
    - epochs is how many complete passes (for small amount of photos 25-50, large amount 50-100)
    - img size is the resolution (for this case 480x480)
    - device is what hardware is using, 0 is GPU, "CPU" is CPU

**Note:** if the yolo command is not working even after installing requirements and reopening your code editor. Go to the file gpu_training.py and adjust if needed

### 4. Running the model
- go to `mice_model_tracker.py` and adjust if needed
- run `mice_model_tracker.py`
