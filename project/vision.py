import numpy as np
from PIL import  Image

GROUND_TRUTH = True

def frame_process(frame_list:bytearray,index=None):
    int_list = list(frame_list)
    img = np.array(int_list).reshape((400,800, 4))
    img = img[:,:,:3]
    if GROUND_TRUTH:
        image = Image.fromarray(img.astype('uint8'), 'RGB')
        image.save(f"images/screenshot_{index}.png")
        return
   