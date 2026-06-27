
# BYTETRACK TRACKER

## What is ByteTrack?

ByteTrack builds on the same Kalman Filter plus Hungarian algorithm framework as SORT but changes the data association strategy
to use almost every detection box regarless of confidence score.

It runs a two-stage matching: First match high-confidence detections to tracks, then match low-confidence detections to any unmatched tracks using IoU.

This reduces missed tracks and framentation for occluded or weak detections while retaining simplicity and high frame rates.

ByteTrack has set state-of-the-art results on standard MOT benchmarks with real-time performance, because it recovers valid low-score detections instead of discarding them

## How does ByteTrack work?

ByteTrack uses a two-stage match strategy that recovers valid object the detection scored low due to occlusion, blur, or partial visibility

    - [Stage 1] - high confidence matching: Detection with confidence above `high_conf_threshold` are matched to confirmed tracks using IoU-based Hungarian assignment, identical to SORT. Unmatched tracks and unmatched high-confidence detections pass to the next stage.

    - [Stage 2] - low confidence matching: Detection with condidence between `track_activation_threshold` and `high_conf_det_threshold` are matched to the remaining unmatched tracks using IoU. This second pass associates weak detections to already-esdtablished tracks, recovering objects that would otherwise be lost. Detection below `track_activation_threshold` are discarded entirely and never start new tracks.

* Key insight: Discarding low-confidence detection outright loses genuiely valid objects that happen to have a low score in one or a few frames. ByteTrack recaptures these by associating them with tracks that already have an established identify and motion history, rather than treating them as new objects. This produces fewer missed tracks and fewer ID switches with almost no additional computation over SORT

* Key params

| PARAMETERS | PURPOSE | Tunning Guidance |
| --- | --- | --- |
| lost_track_buffer | frames to keep an unmatched track alive before deletion | Higher tolerates longer occusion but risk false re-association. 10-30 for most scenes, up to 60 for every long occlusions |
| track_activation_threshold | minimum detection confidence to use in any match stage | Higher reduces spurious tracks, lower catches weak detections, 0.5 - 0.9 typical |
| minimum_consecutive_frames |  consecutive detection required to confirm a new track | 1 confirms immediately 2-3 filters out single-frame false positives |
| high_conf_det_threshold | confidence threshold separating stage-1 from stage-2 detections | 0.5-0.7 typical. lower sends more detections to stage 1, higher relies more on stage-2 recovery |


## Run on video, webcam, or RTSP stream

Follow-up some code below for each type:

### Video

```
import cv2
import supervision as sv
from rfdetr import RFDETRMedium
from trackers import ByteTrackTracker

tracker = ByteTrackTracker()
model = RFDETRMedium()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

video_capture = cv2.VideoCapture("<RTSP_STREAM_URL>")
if not video_capture.isOpened():
    raise RuntimeError("Failed to open RTSP stream")

while True:
    success, frame_bgr = video_capture.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    detections = model.predict(frame_rgb)
    detections = tracker.update(detections)

    annotated_frame = box_annotator.annotate(frame_bgr, detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame,
        detections,
        labels=detections.tracker_id,
    )

    cv2.imshow("RF-DETR + ByteTrack", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
```

### Webcame

```
import cv2
import supervision as sv
from rfdetr import RFDETRMedium
from trackers import ByteTrackTracker

tracker = ByteTrackTracker()
model = RFDETRMedium()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

video_capture = cv2.VideoCapture("<WEBCAM_INDEX>")
if not video_capture.isOpened():
    raise RuntimeError("Failed to open webcam")

while True:
    success, frame_bgr = video_capture.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    detections = model.predict(frame_rgb)
    detections = tracker.update(detections)

    annotated_frame = box_annotator.annotate(frame_bgr, detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame,
        detections,
        labels=detections.tracker_id,
    )

    cv2.imshow("RF-DETR + ByteTrack", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
```

### RTSP

```
import cv2
import supervision as sv
from rfdetr import RFDETRMedium
from trackers import ByteTrackTracker

tracker = ByteTrackTracker()
model = RFDETRMedium()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

video_capture = cv2.VideoCapture("<RTSP_STREAM_URL>")
if not video_capture.isOpened():
    raise RuntimeError("Failed to open RTSP stream")

while True:
    success, frame_bgr = video_capture.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    detections = model.predict(frame_rgb)
    detections = tracker.update(detections)

    annotated_frame = box_annotator.annotate(frame_bgr, detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame,
        detections,
        labels=detections.tracker_id,
    )

    cv2.imshow("RF-DETR + ByteTrack", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
```


## Reference link

`https://trackers.roboflow.com/develop/trackers/bytetrack/#__tabbed_1_3`