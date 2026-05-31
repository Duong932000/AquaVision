# AquaVision -- AI-powered Fish Tracking and Monitoring Platform for Aquaculture


## Overview

AquaVision is an end-to-end computer vision platform designed for aquaculture environments

The project focuses on real-time fish detectin, tracking, monitoring, and behavioral analytics using IP cameras and AI models

The long-term vision is build a production-ready intelligent system for fish farms and RAS (Recirculating Aquaculture System)


## Objectives

- Real-time fish detection in tank of RAS

- Multi-object fish tracking

- Fish analysis

- Biomass estimation

- Feeding behavior monitoring

- Health and anomaly detection

- Farm intelligent dashboard

- Multi-camera IP deployment ()


## System Architecture

```text
IP Camera (RTSP)
        │
        ▼
 YOLO11 Detection
        │
        ▼
 ByteTrack Tracking
        │
        ▼
Trajectory Database
        │
        ▼
Fish Analytics
        │
        ▼
Dashboard & Alerts
```


## Technology Stack

### Computer Vision

- Ultralytics YOLO (v8/v11)

- OpenCV

### Multi-Object Tracking (MOT)

ByteTrack

### Dataset & Annotation

- Roboflow

- Label Studio

### Backend

- Python 3.11+

- FastAPI

### Dashboard

- Python Desktop App

- Web: #TODO

### Database

PostgreSQL

### Experiment Ttacking

MLflow

### Containerization

- Docker
- K8s


## Roadmap

Read more detail in `./ROADMAP.md`


## Author and Maintainer

Nguyen Dac Duong
