# Project Report

## YOLO Object Detection Using Ultralytics

### Abstract

This project implements a command-line computer-vision application for detecting
common objects in images, videos, and webcam streams. It uses a pretrained
Ultralytics YOLO model and does not include model training, dataset preparation,
or custom-class development. The application accepts a source and optional
inference settings, performs object detection, saves annotated results, and
prints a short detection summary for each processed item.

### 1. Introduction

Object detection is a computer-vision task that identifies objects in visual
data and locates them with bounding boxes. This project provides a small,
reusable interface for running pretrained YOLO inference without requiring the
user to build a training dataset or write model-inference code manually.

The implementation is intended for demonstrations, experiments, and basic
offline or webcam-based detection. The default model is `yolo11n.pt`, a small
Ultralytics YOLO model. The README identifies the model's standard COCO-style
classes with examples including `person`, `car`, `dog`, and `bottle`.

### 2. Objectives

The project has the following objectives:

- Accept an image path, video path, or webcam index from the command line.
- Load a pretrained Ultralytics YOLO model.
- Detect objects using a configurable confidence threshold.
- Save annotated images or videos to a predictable output directory.
- Optionally display a live preview during inference.
- Report whether objects were detected for each processed result.

### 3. Scope and Limitations

The project performs inference only. It does not train or fine-tune a model,
prepare or label datasets, calculate accuracy or other evaluation metrics, or
provide a graphical user interface. Detection classes are determined by the
selected pretrained model. Results depend on the model, input quality,
confidence threshold, hardware, and the objects visible in the source.

The webcam workflow is designed to be stopped from the preview window by
pressing `q`, as described in the README. The `--no-view` option disables the
preview, which is useful for video processing or environments without display
support.

### 4. Technologies and Dependencies

| Component | Purpose |
|---|---|
| Python | Runs the application and command-line interface |
| Ultralytics (`>=8.3.0`) | Loads the YOLO model and performs prediction |
| OpenCV (`>=4.8.0`) | Provides the computer-vision runtime used by the detection stack |
| YOLO model file | Supplies pretrained object-detection weights |

Dependencies are listed in `requirements.txt`. On first use, Ultralytics
automatically downloads the selected pretrained model when it is not already
available locally.

### 5. System Design

The application is contained in `detect.py` and follows this execution flow:

1. Build the command-line argument parser.
2. Read the required source and optional model, output, confidence, and display
   settings.
3. Convert a numeric source such as `0` into a webcam index; treat other
   values as file paths.
4. Validate that confidence is between `0` and `1` and that file sources exist.
5. Create the output directory if it does not exist.
6. Load the selected YOLO model.
7. Run `model.predict` with annotated saving enabled and streaming enabled.
8. Print a detection message for each result.
9. Print the final result directory.

The core prediction call uses the following settings:

- `conf=args.confidence`
- `project=args.output`
- `name="detections"`
- `exist_ok=True`
- `save=True`
- `show=not args.no_view`
- `stream=True`

Therefore, the normal output location is `runs/detections` when the default
output setting is used.

### 6. Implementation Details

#### Source handling

The `parse_source` function interprets a string containing only digits as a
webcam index. For example, `0` becomes integer `0`, which selects the default
camera. Any other source value remains a string and is treated as an input file
path.

#### Argument validation

The `--confidence` value must be within the inclusive range from `0` to `1`.
When the source is a file path, the program checks that the path exists before
loading the model. Invalid confidence values raise `ValueError`, and missing
source files raise `FileNotFoundError`.

#### Detection and reporting

The program iterates over streamed prediction results. For each result, it
checks whether bounding boxes exist and whether at least one box is present. It
then prints either the number of detected objects and the result path or a
message stating that no objects were detected.

### 7. Installation and Execution

From the project directory, create and activate the virtual environment and
install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Example commands:

```powershell
# Image detection
python detect.py --source path\to\image.jpg

# Video detection without opening a preview window
python detect.py --source path\to\video.mp4 --no-view

# Webcam detection
python detect.py --source 0

# Use a custom confidence threshold
python detect.py --source path\to\image.jpg --confidence 0.5

# Select another compatible pretrained model
python detect.py --source path\to\image.jpg --model yolo11s.pt
```

Annotated output is saved under `runs\detections` by default. The output root
can be changed with `--output`.

### 8. Command-Line Interface

| Argument | Required | Default | Description |
|---|---:|---|---|
| `--source` | Yes | None | Image path, video path, or webcam index |
| `--model` | No | `yolo11n.pt` | Ultralytics model name or local `.pt` file |
| `--output` | No | `runs` | Root folder for annotated results |
| `--confidence` | No | `0.25` | Minimum confidence from `0` to `1` |
| `--no-view` | No | Disabled | Save results without opening a preview window |

### 9. Output

The program creates the configured output directory and writes annotated
results in the `detections` subdirectory. During processing, the console shows
whether objects were found in each result. After processing, it prints the
location of the annotated results.

### 10. Testing and Verification

The implementation can be verified with the following checks:

- Run `python detect.py --help` to verify the command-line interface.
- Run with a confidence value below `0` or above `1` to verify validation.
- Run with a nonexistent file source to verify input-file validation.
- Run with a valid image to verify annotated output and detection reporting.
- Run with a valid video and `--no-view` to verify non-interactive processing.
- Run with webcam source `0` to verify camera input when a camera is available.

The project does not currently include automated unit tests or a labeled test
dataset, so quantitative precision, recall, mAP, and runtime benchmarks are
not provided by the repository.

### 11. Conclusion

This project delivers a concise and practical interface for pretrained YOLO
object detection. Its main strengths are simple setup, support for multiple
input types, configurable confidence and model selection, automatic result
saving, and clear console feedback. Its intentionally small scope makes it a
useful foundation for future additions such as batch processing, class
filtering, performance benchmarking, custom training, or a graphical user
interface.

### 12. Project Structure

```text
yolo_object_detection/
|-- detect.py
|-- requirements.txt
|-- README.md
|-- PROJECT_REPORT.md
|-- runs/                 # created automatically after detection
```