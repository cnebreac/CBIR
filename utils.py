import pandas as pd
import numpy as np

import cv2

def load_images(train: bool = True):
    """
    Loads a dataframe with the image metadata and a list with the images in RGB Format
    """
    if train: path = 'train.csv'
    else: path = 'test.csv'
    images_paths = pd.read_csv(path)
    images = []

    label_map = {'packaged': 0, 'dishes': 1, 'storefronts': 2, 'artwork': 3, 'meme': 4, 'cars': 5, 'landmark': 6, 'illustrations': 7, 'toys': 8, 'apparel': 9, 'furniture': 10}

    for _, row in images_paths.iterrows():
        img = cv2.imread(row['path'])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)
    
    images_paths['label_id'] = images_paths['label'].map(label_map)
    images_paths['image_id'] = images_paths.index
    return images_paths, images

def save_features(features, index, meta, filename):
    """
    Saves the features vector to a csv with the metadata of each one.
    """
    if isinstance(features, list):
        features = np.concatenate(features)

    descs = pd.DataFrame(features)
    descs['image_id'] = index

    descs_save = pd.merge(descs, meta, how = "inner", left_on = "image_id", right_on = "image_id").drop(["train", "image_name", "label", "path"], axis = 1)
    descs_save.to_csv(f"features/{filename}.csv", index = False)

def load_features(path: str):
    df = pd.read_csv(path)
    images_paths = df[['image_id', 'label_id']]
    features = df.drop(['image_id', 'label_id'], axis = 1).values
    return images_paths, features