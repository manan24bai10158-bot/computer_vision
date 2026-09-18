# YOLO Object Detection

A small computer-vision project that detects common objects with a pretrained
Ultralytics YOLO model. No training or dataset preparation is required. The
model uses the standard COCO classes, such as `person`, `car`, `dog`, and
`bottle`.

## Setup

From this folder, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The first run downloads `yolo11n.pt` automatically from Ultralytics.

## Run detection

Detect objects in an image:

```powershell
python detect.py --source path\to\image.jpg
```

Detect objects in a video:

```powershell
python detect.py --source path\to\video.mp4 --no-view
```

Use a webcam (press `q` in the preview window to stop):

```powershell
python detect.py --source 0
```

Results are written to `runs\detections`. Adjust the confidence threshold with
`--confidence 0.5`. A different pretrained model can be selected with
`--model`, for example `yolo11s.pt` for a larger model.

## Project structure

```text
yolo_object_detection/
|-- detect.py
|-- requirements.txt
|-- README.md
|-- runs/                 # created automatically after detection
```
