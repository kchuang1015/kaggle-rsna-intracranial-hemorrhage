import os
import pickle
import random

import pandas as pd
import numpy as np
import torch
import cv2
import pydicom

from .. import factory
from ..utils.logger import log
from ...utils import mappings, misc


def apply_window_policy(dicom, image, row, policy):
    if policy == 1:
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.apply_window(image, 40, 80) # brain
        image2 = misc.apply_window(image, 80, 200) # subdural
        image3 = misc.apply_window(image, row.WindowCenter, row.WindowWidth)
        image1 = (image1 - 0) / 80
        image2 = (image2 - (-20)) / 200
        image3 = (image3 - image3.min()) / (image3.max()-image3.min())
        image = np.array([
            image1 - image1.mean(),
            image2 - image2.mean(),
            image3 - image3.mean(),
        ]).transpose(1,2,0)
    elif policy == 2:
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.apply_window(image, 40, 80) # brain
        image2 = misc.apply_window(image, 80, 200) # subdural
        image3 = misc.apply_window(image, 40, 380) # soft tissues
        image1 = (image1 - 0) / 80
        image2 = (image2 - (-20)) / 200
        image3 = (image3 - (-150)) / 380
        image = np.array([
            image1 - image1.mean(),
            image2 - image2.mean(),
            image3 - image3.mean(),
        ]).transpose(1,2,0)
    elif policy == 3: # Brain + Subdural + Raw image
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.apply_window(image, 40, 80) # brain
        image2 = misc.apply_window(image, 80, 200) # subdural
        image3 = image # raw 
        image1 = (image1 - 0) / 80
        image2 = (image2 - (-20)) / 200
        image3 = (image3 / 8192)
        image = np.array([
            image1 - image1.mean(),
            image2 - image2.mean(),
            image3 - image3.mean(),
        ]).transpose(1,2,0)
    elif policy == 4: #Sigmoid (Brain + Subdural + Bone) Windowing
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.sigmoid_window_Normaliztion(image, 40, 80) # brain
        image2 = misc.sigmoid_window_Normaliztion(image, 80, 200) # subdural
        image3 = misc.sigmoid_window_Normaliztion(image, 600, 2000) # bone
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 5: #Sigmoid (Brain + Subdural + Bone) Windowing without normalization
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.sigmoid_window(image, 40, 80) # brain
        image2 = misc.sigmoid_window(image, 80, 200) # subdural
        image3 = misc.sigmoid_window(image, 600, 2000) # bone
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 6: #Sigmoid (Brain + Subdural + raw) Windowing without normalization
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.sigmoid_window(image, 40, 80) # brain
        image2 = misc.sigmoid_window(image, 80, 200) # subdural
        image3 = misc.sigmoid_window(image, 0, 8192) # raw
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 7: #Sigmoid (multi-channel) Windowing without normalization
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.sigmoid_window(image, 0, 2048) 
        image2 = misc.sigmoid_window(image, 1024, 2048)
        image3 = misc.sigmoid_window(image, 2048, 2048) 
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 8: #Sigmoid (Brain + Subdural + soft tissues) Windowing without normalization
        image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image1 = misc.sigmoid_window(image, 40, 80) # brain
        image2 = misc.sigmoid_window(image, 80, 200) # subdural
        image3 = misc.sigmoid_window(image, 40, 380) # soft tissues
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 9: # max-min image normalization
        image = misc.rescale_image_normalization(image, row.RescaleSlope, row.RescaleIntercept)
        image = np.array([
            image,
            image,
            image,
        ]).transpose(1,2,0)
    elif policy == 10: # max-min image normalization, z-score, sigmoid
        image1 = misc.rescale_image_normalization(image, row.RescaleSlope, row.RescaleIntercept)
        image2 = (image - image.mean()) / image.std()
        image3 = 1.0 / (1.0 + np.power(np.e, -1.0 * image2))
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 11: # max-min image normalization, z-score, sigmoid (~soft tissues)
        image1 = misc.rescale_image_normalization(image, row.RescaleSlope, row.RescaleIntercept)
        image2 = (image - image.mean()) / image.std()
        image3 = misc.sigmoid_window(image, 40, 380) # soft tissues
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)
    elif policy == 12: # Data clean (WP12), max-min image normalization, z-score, sigmoid (~soft tissues)
        if (dicom.BitsStored == 12) and (dicom.PixelRepresentation == 0) and (int(dicom.RescaleIntercept) > -100):
            misc.correct_dcm(dicom)        
        image1 = misc.rescale_image_normalization(image, dicom.RescaleSlope, dicom.RescaleIntercept)
        image = misc.rescale_image(image, dicom.RescaleSlope, dicom.RescaleIntercept)
        image2 = (image - image.mean()) / image.std()
        image3 = misc.sigmoid_window(image, 40, 380) # soft tissues
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0)    
    elif policy == 13: # Data clean (8), max-min image normalization, z-score, sigmoid (~soft tissues)
        if (dicom.BitsStored == 12) and (dicom.PixelRepresentation == 0) and (int(dicom.RescaleIntercept) > -100):
            misc.correct_dcm(dicom)        
        image = misc.rescale_image(image, dicom.RescaleSlope, dicom.RescaleIntercept)
        image1 = misc.sigmoid_window(image, 40, 80) # brain
        image2 = misc.sigmoid_window(image, 80, 200) # subdural
        image3 = misc.sigmoid_window(image, 40, 380) # soft tissues
        image = np.array([
            image1,
            image2,
            image3,
        ]).transpose(1,2,0) 
    else:
        raise

    return image


def apply_dataset_policy(df, policy):
    if policy == 'all':
        pass
    elif policy == 'pos==neg':
        df_positive = df[df.labels != '']
        df_negative = df[df.labels == '']
        df_sampled = df_negative.sample(len(df_positive))
        df = pd.concat([df_positive, df_sampled], sort=False)
    else:
        raise
    log('applied dataset_policy %s (%d records)' % (policy, len(df)))

    return df


class CustomDataset(torch.utils.data.Dataset):

    def __init__(self, cfg, folds):
        self.cfg = cfg

        log(f'dataset_policy: {self.cfg.dataset_policy}')
        log(f'window_policy: {self.cfg.window_policy}')

        self.transforms = factory.get_transforms(self.cfg)
        with open(cfg.annotations, 'rb') as f:
            self.df = pickle.load(f)

        if folds:
            self.df = self.df[self.df.fold.isin(folds)]
            log('read dataset (%d records)' % len(self.df))

        self.df = apply_dataset_policy(self.df, self.cfg.dataset_policy)
        #self.df = self.df.sample(560)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        path = '%s/%s.dcm' % (self.cfg.imgdir, row.ID)

        dicom = pydicom.dcmread(path)
        image = dicom.pixel_array
        #image = misc.rescale_image(image, row.RescaleSlope, row.RescaleIntercept)
        image = apply_window_policy(dicom, image, row, self.cfg.window_policy)

        image = self.transforms(image=image)['image']

        target = np.array([0.0] * len(mappings.label_to_num))
        for label in row.labels.split():
            cls = mappings.label_to_num[label]
            target[cls] = 1.0

        if hasattr(self.cfg, 'spread_diagnosis'):
            for label in row.LeftLabel.split() + row.RightLabel.split():
                cls = mappings.label_to_num[label]
                target[cls] += self.cfg.propagate_diagnosis
        target = np.clip(target, 0.0, 1.0)

        return image, torch.FloatTensor(target), row.ID
