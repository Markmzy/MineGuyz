import numpy as np
from PIL import Image
import shutil
import os
import torch
from torchvision.models.segmentation import segmentation
import torchvision.transforms as transforms
import  matplotlib.pyplot as plt
import time

GROUND_TRUTH = True

class Cfg:
    lr = 0.0001
    workers = 2
    batchSize = 2
    imageSize = 64
    n_epoch = 100
    beta1 = 0.5
    seed = 0
    cuda = True
    start_epo = 0
    pretrain = True
    nd_kpts = 6

cfg = Cfg()
device = torch.device("cpu")

class Eyes:
    def __init__(self):
        self.net = segmentation.deeplabv3_resnet50(num_classes=5).to(device)
        self.net.train()
        self.net.eval()
        if cfg.pretrain:
            self.net.load_state_dict(torch.load("./juypter_notebooks/saved_weights/vision_parameters.wts"))
    def get_result(self,img):
        return torch.argmax(self.net(img.to(device))['out'], dim=1)

def img_preprocessing(img,dep,eyes,device,size=(256,256)):
    img = img.resize(size)
    dep = dep.resize(size)
    transform1 = transforms.Compose([transforms.ToTensor()])
    tensor_img = transform1(img).reshape((1,3,size[0],size[1]))
    seg_img = eyes.get_result(tensor_img).reshape((1,1,size[0],size[1])).float()
    seg_img_show = seg_img[0][0].cpu().numpy()
    plt.clf()
    plt.imshow(seg_img_show)
    plt.draw()
    plt.pause(0.001)
    dep_img = transform1(dep).reshape((1,1,size[0],size[1]))
    result_tensor = torch.cat((tensor_img.to(device), dep_img.to(device)), 1)
    result_tensor = torch.cat((result_tensor, seg_img), 1)
    return result_tensor

def frame_process(frame_list:bytearray,video_width,video_height,size=(256,256)):
    int_list = list(frame_list)
    img_o = np.array(int_list).reshape((video_width,video_height,4))
    img = img_o[:,:,:3]
    depth = img_o[:,:,-1].reshape((256,-1))
    image = Image.fromarray(img.astype('uint8'), 'RGB').resize(size)
    depth = Image.fromarray(depth.astype('uint8'), 'L').resize(size)
    return image,depth

def get_img(world_state,agent_obj,eyes,device,video_width,video_height):
    img,dep = frame_process(world_state.video_frames[0].pixels,video_width,video_height)
    input_img = img_preprocessing(img,dep,eyes,device).to(device)
    return input_img

def clear_images():
    shutil.rmtree('./images')
    os.mkdir('./images')

def view_surrounding(video_height, video_width, frame_list:bytearray,index=None,size=(256,256)):
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
   