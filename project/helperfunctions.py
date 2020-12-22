class Vision:
    def __init__(self):
        self.net = segmentation.deeplabv3_resnet50(num_classes=5).to(device)
        self.net.train()
        self.net.eval()
        if vision.trained:
            self.net.load_state_dict(torch.load("./juypter_notebooks/saved_weights/vision_parameters.wts"))
    def get_result(self,img):
        return torch.argmax(self.net(img.to(device))['out'], dim=1)

def imgPreproces(img,dep,eyes,device,size=(512,512)):
    depth = dep.resize(size)
    image = img.resize(size)
   
    transform = transforms.Compose([transforms.ToTensor()])
    tensor = transform1(img).reshape((1,3,size[0],size[1]))
    segmented = eyes.get_result(tensor_img).reshape((1,1,size[0],size[1])).float()
    
    tensor_result = torch.cat((tensor_img.to(device), dep_img.to(device)), 1)
    tensor_result = torch.cat((result_tensor, seg_img), 1)
    return tensor_result

def processFrame(frame_list:bytearray,video_width,video_height,size=(512,512)):
    list = list(frame_list)
    imgOne = np.array(int_list).reshape((video_width,video_height,4))
    imgTwo = imgOne[:,:,:3]
    depth = imgOne[:,:,-1].reshape((512,-1))
    return image,depth

def get_img(world_state,frame,agent_obj,eyes,device,video_width,video_height):
    img,dep = frame_process(frame,video_width,video_height)
    input_img = img_preprocessing(img,dep,eyes,device).to(device)
    return input_img