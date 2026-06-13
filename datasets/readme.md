# DATASETS WORKFLOW FOR AQUAVISION PROJECT

This folder contains all datasets used by AquaVision project

The structure is designed to support:

- Multiple fish species
- Multiple dataset version
- Multiple annotation version
- Multiple model architecture
- Future production deployment


## Dataset Lifecycle

Raw Data
    ↓
Frame Extraction
    ↓
Processed Images
    ↓
Roboflow / CVAT Annotation
    ↓
YOLO Dataset Export
    ↓
Dataset QA (FiftyOne)
    ↓
YOLO Training
    ↓
Model Evaluation
    ↓
Active Learning
    ↓
Dataset Version Upgrade


## Directory Structure

```text
datasets/

├── koi/
│
│   ├── raw/
│   │
│   │   ├── videos/
│   │   ├── images/
│   │   └── metadata/
│   │
│   ├── processed/
│   │
│   │   ├── frames/
│   │   ├── resized/
│   │   └── filtered/
│   │
│   ├── annotations/
│   │
│   │   ├── cvat/
│   │   ├── roboflow/
│   │   └── exports/
│   │
│   ├── datasets/
│   │
│   │   ├── v1/
│   │   ├── v2/
│   │   └── v3/
│   │
│   └── reports/
│
├── eel/
│
│   ├── raw/
│   ├── processed/
│   ├── annotations/
│   ├── datasets/
│   └── reports/
│
└── common/
```
