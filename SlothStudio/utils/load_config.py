
import os
import yaml
from pathlib import Path

def _get_root_dir():

    return Path(os.getenv("ROOT_DIR", ".")).resolve()

def _load_yml_file(file_path):

    if not file_path.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")
    
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


{
'source':{
    'type': 'youtube', 
    'items': ['https://www.youtube.com/watch?v=AbI--MaIh-k&t=4812s']
    },
'model': {
    'type': 'trained', 
    'path': '/home/dacduong/git/AquaVision/runs/detect/train-3/weights/best.pt'
    },
'tracking': {
    'enabled': True, 
    'tracker': 'ByteTrack'
    },
'detection': {
    'confidence': 0.5, 
    'iou': 0.55, 
    'image_size': 1280, 
    'fp16': True, 
    'max_detection': 300
    },
'output': {
    'save_video': True, 
    'save_frames': True
    },
'runtime': {
    'device': 'CPU'
    }
}

{
'source': {
    'type': 'youtube',
    'items': ['https://www.youtube.com/watch?v=AbI--MaIh-k&t=4812s']
    },
'model': {
    'type': 'pretrained',
    'version': 'YOLO26',
    'size': 'm'
    },
'tracking': {
    'enabled': True,
    'tracker': 'ByteTrack'
    },
'detection': {
    'confidence': 0.5,
    'iou': 0.55,
    'image_size': 1280,
    'fp16': True,
    'max_detection': 300
    },
'output': {
    'save_video': True,
    'save_frames': True
    },
'runtime': {
    'device': 'CPU'
    }
}