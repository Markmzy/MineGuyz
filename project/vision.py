import numpy as np
from PIL import Image
import shutil
import os
import torch
from torchvision.models.segmentation import segmentation
import torchvision.transforms as transforms
import  matplotlib.pyplot as plt
import time

device = torch.device("cpu")

def clear_images():
    shutil.rmtree('./images')
    os.mkdir('./images')

def view_surrounding(video_height, video_width, frame_list:bytearray,index=None,size=(512,512)):
    int_list = list(frame_list)
    img = np.array(int_list).reshape(video_height,video_width,4)
    img = img[:,:,:3]
    
    if GROUND_TRUTH:
        image = Image.fromarray(img.astype('uint8'), 'RGB').resize(size)
        image.save(f"images/screenshot_{index}.png")
    
    result_data_set = []

    for i in range(video_height):
        result_data_set.append([])
        for j in range(video_width):
            r,g,b = img[i][j][0],img[i][j][1],img[i][j][2]
            label = 0
            if r>110 and g>150 and b>225:   
                label = 0#sky
            elif (r>120 and r<210 and g>100 and g<210 and b>20 and b<100) or (r>15 and r<120 and g>80 and g<205 and b>25 and b<210):
                label = 1#gold barrier
            else:
                label = 4 #road

            result_data_set[i].append(label)

    return result_data_set
   