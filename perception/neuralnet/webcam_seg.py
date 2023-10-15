import ultralytics
import cv2
import numpy as np

from perception.webcam.webcam_read import CVCamera

# Video
cam = CVCamera()
model = ultralytics.YOLO('./perception/neuralnet/weight/yolov8x-seg.pt')

# Everythind detection
# while cam.capture.isOpened():
#     success, frame = cam.capture.read()
#     if success:
#         results = model(frame)
#         annotated_frame = results[0].plot()
#         cv2.imshow("YOLOv8 Inference", annotated_frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         break
# capture.release()
# cv2.destroyAllWindows()


# Everything mask only
# while cam.capture.isOpened():
#     success, img = cam.capture.read()
#     imgShow = np.ones_like(img)
#     imgMask = np.zeros((img.shape[0], img.shape[1]))
#     result = model(img, stream=True, conf=0.5)
#     for r in result:
#         boxes = r.boxes
#         masks = r.masks
#         for bi, box in enumerate(boxes):
#             classes_number = int(box.cls[0].item())
#             classes_name = model.names[classes_number]
#             print(f"class name ={classes_name}, index = {bi}")
#             eachMask = masks.masks[bi, :, :].cpu().numpy()
#             eachMask = eachMask.reshape(eachMask.shape[0], eachMask.shape[1])
#             imgMask = imgMask + eachMask
#         imgshow = np.where(imgMask[..., None], img, 0)
#         cv2.imshow("Everything mask only", imgshow)
#         cv2.waitKey(1)


# Apple mask only
while cam.capture.isOpened():
    success, img = cam.capture.read()
    imgShow = np.ones_like(img)
    imgMask = np.zeros((img.shape[0], img.shape[1]))
    result = model(img, stream=True, conf=0.5)
    for r in result:
        boxes = r.boxes
        masks = r.masks
        for bi, box in enumerate(boxes):
            classes_number = int(box.cls[0].item())
            classes_name = model.names[classes_number]
            if classes_name == "apple":
                appleMask = masks.masks[bi, :, :].cpu().numpy()
                appleMask = appleMask.reshape(appleMask.shape[0], appleMask.shape[1])
                imgMask = imgMask + appleMask
    imgshow = np.where(imgMask[..., None], img, 0)
    cv2.imshow("Apple mask only", imgshow)
    cv2.waitKey(0)