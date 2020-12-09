import numpy as np
from PIL import Image
import shutil
import os

GROUND_TRUTH = True


def clear_images():
    shutil.rmtree('./images')
    os.mkdir('./images')

def view_surrounding(video_height, video_width, frame_list:bytearray,index=None):
    int_list = list(frame_list)
    img = np.array(int_list).reshape(video_height,video_width,4)
    img = img[:,:,:3]
    if GROUND_TRUTH:
        image = Image.fromarray(img.astype('uint8'), 'RGB')
        image.save(f"images/screenshot_{index}.png")
    
    result_data_set = []


    for i in range(video_height):
        result_data_set.append([])
        for j in range(video_width):
            r,g,b = img[i][j][0],img[i][j][1],img[i][j][2]
            label = 0
            if r>110 and g>150 and b>225:
                label = 0#sky
            elif r>180 and g > 160  and b>50:
                label = 1#gold barrier
            elif r>30 and g<195 and b<120:
                label = 2#emerald barrier
            else:
                label = 4 #road

            result_data_set[i].append(label)

    return result_data_set
   