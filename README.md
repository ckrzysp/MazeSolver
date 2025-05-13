## Survival of the Mice

## Model
[dataset: soon](https://github.com/ckrzysp/MazeSolver/tree/main/model)

- 1000 images 
  - 800 Training
  - 200 validation

## Requirements
- Python 3.8 - 3.10
  (11 and 12 have worked but are **not recommended**)

## Steps

### 1. Download the requirements
- In 'MazeSolver/' go to your terminal and enter
'pip install -r requirements.txt'

**(Optional: If you have a nvidia graphics card)**
'pip uninstall torch torchvision'
'pip install -r cuda-requirements.txt'
- if torchaudio does not install, thats fine

### 2. Download the dataset
- place folder in the `mode/`

**(Optional: adjusting amount of photos)**
- delete contents in `labels/` for both `train/` and `val/`
- go to `mice_training.py` adjust the for loop based on the image names/ training amount
- run `mice_training.py`

### 3. Train the model
- It will take a bit depending on how many photos you used and computer performance
(CPU)
`yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=480`
(GPU)
`yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=25 imgsz=480 device=0`
- task for detecting object
- mode for training/predicting
- model for the base model
- data is my data.yaml config file
- epochs is how many complete passes 
(for small amount of photos 25-50, large amount 50-100)
- img size is the resolution (for this case 480x480)
- device is what hardware is using, 0 is GPU, "CPU" is CPU
# NOTE: if the yolo command is not working even after installing requirements and reopening your code editor. Go to the file gpu_training.py and adjust if needed
### 4. Running the model
- go to `mice_model_tracker.py` and adjust if needed
- run `mice_model_tracker.py`

## problems

- Heatmap

