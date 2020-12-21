---
layout: page
title: Final
permalink: /final/
---

<br />
### Summary 

#### The goal is for an agent to participate and guide itself to reach the mini-games finish line in a free-for-all struggle. The mini-game generated is designed with vibrant aesthetics consisting of multiple courses with an added complexity. Each course has distinguished obstacles and a unique set of actions to be utilized by the agent to achieve the optimal result. The agent has access to four controls or actions: move forward, move left, move right, and jump. The map begins with the agent encountering overwhelming stacked blocks with associated negative reinforcement given if the agent touches it. The map follows with additional stages containing a bridge over water, a massive staircase, and colossal cubes that block the right side of the path. These obstacles within each course are generated randomly upon the beginning of each episode.  All the obstacles and the surrounding glass guarding the entire field have a negative reinforcement that is small, numerically speaking, relative to the positive reinforcement of the redstone block at the end map. By touching the redstone, which represents the finish line, the agent receives a substantial reinforcement. This results in the agent learning that the best outcome is to reach the finish line by encountering the least number of obstacles on the courses, ultimately maximizing the reward. There are two embedded factors within the agent's goal; initially, the agent needs to learn to reach the finish line at any cost and then learn to acquire far more quickly than the previous iterations. 


#### The problem is not particularly trivial to solve using greedy or brute force algorithms or some form of scripted method because the map is complex, but additionally, the obstacles are generated randomly, making it impossible to use a discrete algorithm to solve such a stochastic problem. AI/ML algorithms are beneficial in this specific context since it can learn and improve from experience over time. This allows the agent to take more practical actions in less predictable dynamic environments. Utilizing a reinforcement learning algorithm provides the agent a framework or language to model the game's complex system as generically as possible. Moreover, using computer vision techniques such as depth map and segmentation provides the agent with pattern recognition ability to distinguish between a set of phenomenons or things within the game. 

<br />

### Approaches

<br />

#### Segmenation

#### Image segmentation was done for the first part of the stage to aid in computer vision and help the agent in avoiding the blocks and barriers. Training data was provided to a residual neural network by first generating dozens of images using the malmo screen capture API. Then these images were looped over pixel by pixel to segment for training purposes based upon the range of their RGB values. The sky was classified based upon if the pixel had an R value in the range (110, inf+), G value in the range (150, +in), and B value in the range (225, inf+). Barriers were either gold or green so they were classified Gold based on if they had R values in the range of (120, 210), G values in the range of (100,210), and B values in the range of (20,100), or Green based on if they had R values in the range of (15, 120), G values in the range of (80,205), and B values in the range of (25,210). Everything else was classified background. 

```python

for i in range(video_height):
        result_data_set.append([])
        for j in range(video_width):
            r,g,b = img[i][j][0],img[i][j][1],img[i][j][2]
            label = 0
            if r>110 and g>150 and b>225:   
                label = 0
            elif (r>120 and r<210 and g>100 and g<210 and b>20 and b<100) or (r>15 and r<120 and g>80 and g<205 and b>25 and b<210):
                label = 1
            else:
                label = 2 

            result_data_set[i].append(label)
```

<p align="center">
  <img src="assets/images/plot0.png" />
</p>

<p align="center">
  <img src="assets/images/plot1.png" />
</p>

<p align="center">
  <img src="assets/images/plot3.png" />
</p>
These images and manual labels for them were saved locally in our images folder. We then imported these images and labels using numpy, and split them into training and validation data with an 80/20 split. Here we then fed the training data into a residual neural network from pytorch which we would then train to automatically segment inputted images from the agent during gameplay for the barrier blocks.

#### Residual Net Breakdown
<p align="center">
  <img src="assets/images/residualnet.png" />
</p>
<br />

### Evaluation
#### Todo

<br />
### Resources Used

#### The resources utilized so far have been using Malmo’s API to simulate the environment and Pytroch for creating tensors, neural networks, and optimizers. Certain functionalities from assignment that were useful were derived for this project. The following resources were used to develop implementations or to develop ideas.


1. [Policy Gradient Reinforcement Learning in Pytorch](https://medium.com/@ts1829/policy-gradient-reinforcement-learning-in-pytorch-df1383ea0baf)
2. [Building a DQN in Pytorch](https://blog.gofynd.com/building-a-deep-q-network-in-pytorch-fa1086aa5435)
3. [Pytorch Reinforcement Learning](https://github.com/bentrevett/pytorch-rl)
4. [How does the Bellman equation work in Deep RL](https://towardsdatascience.com/residual-network-implementing-resnet-a7da63c7b278)
5. [Residual Neural Nets in Pytorch](https://towardsdatascience.com/residual-network-implementing-resnet-a7da63c7b278)
6. [Pytorch and Image Segmentation](https://www.learnopencv.com/pytorch-for-beginners-semantic-segmentation-using-torchvision/)
7. [Depth Maps in Python](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html)

