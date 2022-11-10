import torch
import numpy as np
from constants import config
import cv2
from transformers import ViTFeatureExtractor
from transformers import ViTModel
import torch.nn as nn


class ViTForImageClassification(nn.Module):
    def __init__(self, num_labels=3):
        super(ViTForImageClassification, self).__init__()
        self.vit = ViTModel.from_pretrained(config.vit_transformer_path)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.vit.config.hidden_size, num_labels)
        self.num_labels = num_labels

    def forward(self, pixel_values, labels):
        outputs = self.vit(pixel_values=pixel_values)
        output = self.dropout(outputs.last_hidden_state[:, 0])
        logits = self.classifier(output)

        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
        if loss is not None:
            return logits, loss.item()
        else:
            return logits, None


def classify(image):
    labels = {0: 'aadhar', 1: 'cheque', 2: 'pan', 3: 'passbook'}
    with torch.no_grad():
        feature_extractor = ViTFeatureExtractor.from_pretrained(config.vit_transformer_path)
        model = ViTForImageClassification(4)
        model.load_state_dict(torch.load(config.vit_transformer_model, map_location=torch.device('cpu')))
        model.eval()
        inputs = torch.from_numpy(image)
        inputs = torch.tensor(np.stack(feature_extractor(inputs)['pixel_values'], axis=0))
        target = torch.tensor([0])
        prediction, loss = model(inputs, target)
        predicted_class = np.argmax(prediction.cpu())
        probs = nn.functional.softmax(prediction, dim=1).squeeze()
        pos = np.argmax(probs)
        return labels[predicted_class.item()], probs[pos.item()].item()*100
