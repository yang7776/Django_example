# -*- coding: utf-8 -*-
import torch      # 可在 https://pytorch.org/get-started/locally/ 下载
import torchvision
from torchvision import transforms
from PIL import Image
import cv2

names = {'0': 'background', '1': 'person', '2': 'bicycle',
         '3': 'car', '4': 'motorcycle', '5': 'airplane', '6': 'bus', '7': 'train', '8': 'truck', '9': 'boat', '10': 'traffic light',
         '11': 'fire hydrant', '13': 'stop sign', '14': 'parking meter', '15': 'bench',
         '16': 'bird', '17': 'cat', '18': 'dog', '19': 'horse', '20': 'sheep',
         '21': 'cow', '22': 'elephant', '23': 'bear', '24': 'zebra', '25': 'giraffe',
         '27': 'backpack', '28': 'umbrella', '31': 'handbag', '32': 'tie',
         '33': 'suitcase', '34': 'frisbee', '35': 'skis', '36': 'snowboard',
         '37': 'sports ball', '38': 'kite', '39': 'baseball bat',
         '40': 'baseball glove', '41': 'skateboard', '42': 'surfboard',
         '43': 'tennis racket', '44': 'bottle', '46': 'wine glass', '47': 'cup',
         '48': 'fork', '49': 'knife', '50': 'spoon', '51': 'bowl', '52': 'banana',
         '53': 'apple', '54': 'sandwich', '55': 'orange', '56': 'broccoli',
         '57': 'carrot', '58': 'hot dog', '59': 'pizza', '60': 'donut',
         '61': 'cake', '62': 'chair', '63': 'couch', '64': 'potted plant',
         '65': 'bed', '67': 'dining table', '70': 'toilet', '72': 'tv',
         '73': 'laptop', '74': 'mouse', '75': 'remote', '76': 'keyboard',
         '77': 'cell phone', '78': 'microwave', '79': 'oven', '80': 'toaster',
         '81': 'sink', '82': 'refrigerator', '84': 'book', '85': 'clock',
         '86': 'vase', '87': 'scissors', '88': 'teddybear', '89': 'hair drier', '90': 'toothbrush'}
THRESHOLD = 0.8
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True, num_classes=91)
# model.cuda()
model.eval()
transform = transforms.ToTensor()
image = cv2.imread('/home/leidong/下载/111.jpg')
img_copy = image
img_tensor = torch.from_numpy(image / 255).permute(2, 0, 1).float()
x = [img_tensor]
output = model(x)
boxes = output[0]['boxes']
labels = output[0]['labels']
scores = output[0]['scores']
for idx in range(boxes.shape[0]):
    if scores[idx] >= THRESHOLD:
        x1, y1, x2, y2 = boxes[idx][0], boxes[idx][1], boxes[idx][2], boxes[idx][3]
        name = names[str(labels[idx].item())]
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_copy, text=name, org=(x1, y1 + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5, thickness=1, lineType=cv2.LINE_AA, color=(0, 0, 255))

cv2.namedWindow('result', 0)
cv2.imshow('result', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
