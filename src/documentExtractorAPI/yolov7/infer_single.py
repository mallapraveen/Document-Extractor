import torch
from PIL import Image

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords

from tesseract import ocr_cropped_image
from transformer import transformer_ocr


def infer_yolov7(model_path, image, labels, typ, transformerOcr):

    with torch.no_grad():
        im = Image.fromarray(image)
        image_path = f'./yolov7/runs/detect/exp/{typ}.jpg'
        im.save(f'./yolov7/runs/detect/exp/{typ}.jpg')
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        half = device.type != 'cpu'  # half precision only supported on CUDA
        # Load model
        model = attempt_load(model_path, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        imgsz = 640
        imgsz = check_img_size(imgsz, s=stride)  # check img_size
        if half:
            model.half()  # to FP16

        dataset = LoadImages(image_path, img_size=imgsz, stride=stride)

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            pred = model(img, augment=False)[0]
            pred = non_max_suppression(pred, 0.25, 0.45)
            for i, det in enumerate(pred):
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)
                if len(det):
                    if typ == 'aadhar':
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                        boxes = [i[:4] for i in det.tolist() if i[5] != 4]
                        pred_classes = [i[5] for i in det.tolist() if i[5] != 4]
                        scores = [i[4] for i in det.tolist() if i[5] != 4]
                    else:
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                        boxes = [i[:4] for i in det.tolist()]
                        pred_classes = [i[5] for i in det.tolist()]
                        scores = [i[4] for i in det.tolist()]

            rm_dup = {}
            for i in range(len(pred_classes)):
                if pred_classes[i] in rm_dup and rm_dup[pred_classes[i]]['score'] < scores[i]:
                    rm_dup[pred_classes[i]] = dict(score=scores[i], box=boxes[i])
                elif pred_classes[i] not in rm_dup:
                    rm_dup[pred_classes[i]] = dict(score=scores[i], box=boxes[i])

            boxes, pred_classes, scores = [], [], []
            for k, v in rm_dup.items():
                pred_classes.append(k)
                scores.append(v['score'])
                boxes.append(v['box'])

            if not transformerOcr:
                load = ocr_cropped_image(im0, boxes, pred_classes, scores, labels)
            else:
                load = transformer_ocr(im0, boxes, pred_classes, scores, labels)

        return load
