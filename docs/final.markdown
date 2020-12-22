---
layout: page
title: Final
permalink: /final/
---

## **Video**

Todo

<br />

## **Project Summary** 

#### The goal is for an agent to participate and guide itself to reach the mini-games finish line in a free-for-all struggle. The mini-game generated is designed with vibrant aesthetics consisting of multiple courses with an added complexity. Each course has distinguished obstacles and a unique set of actions to be utilized by the agent to achieve the optimal result. The agent has access to four controls or actions: move forward, move left, move right, and jump. The map begins with the agent encountering overwhelming stacked blocks with associated negative reinforcement given if the agent touches it. The map follows with additional stages containing a bridge over water, a massive staircase, and colossal cubes that block the right side of the path. These obstacles within each course are generated randomly upon the beginning of each episode.  All the obstacles and the surrounding glass guarding the entire field have a negative reinforcement that is small, numerically speaking, relative to the positive reinforcement of the redstone block at the end map. By touching the redstone, which represents the finish line, the agent receives a substantial reinforcement. This results in the agent learning that the best outcome is to reach the finish line by encountering the least number of obstacles on the courses, ultimately maximizing the reward. There are two embedded factors within the agent's goal; initially, the agent needs to learn to reach the finish line at any cost and then learn to acquire far more quickly than the previous iterations. 


#### The problem is not particularly trivial to solve using greedy or brute force algorithms or some form of scripted method because the map is complex, but additionally, the obstacles are generated randomly, making it impossible to use a discrete algorithm to solve such a stochastic problem. AI/ML algorithms are beneficial in this specific context since it can learn and improve from experience over time. This allows the agent to take more practical actions in less predictable dynamic environments. Utilizing a reinforcement learning algorithm provides the agent a framework or language to model the game's complex system as generically as possible. Moreover, using computer vision techniques such as depth map and segmentation provides the agent with pattern recognition ability to distinguish between a set of phenomenons or things within the game. 


![My image Name](assets/images/aeriel.png)

<br />

## **Approaches**

#### <u>DQN</u>

#### For our project we continued to use the Deep Q-Learning Algorithm. We also continued to utilize replay memory during training to allow the agent's observed transitions to be resued. Which then leads to the build up of a decorrelated batach of transitions significantly boosting the DQN's training. The given funtion allows the Q-Learning alogrithm to maximize a given reward:

<br />
&ensp;<img src="https://render.githubusercontent.com/render/math?math=Q^*: State \times Action \rightarrow \mathbb{R}">

<br />

##### When given an action the policy is utilized to maximize a reward as such:

<br />
&ensp;<img src="https://render.githubusercontent.com/render/math?math=\pi^*(s) = \arg\!\max_a \ Q^*(s, a)">

<br />

#### Since the information on the world is extremely limited and there is no access to the Q*, by utilizing convolutional neural networks as a function approximator we can construct one and train it to be similar Q* to. The Bellman equation given below is used as such that every Q* function for a policy obeys this equation.  
<br />
&ensp;<img src="https://render.githubusercontent.com/render/math?math=Q^{\pi}(s, a) = r + \gamma Q^{\pi}(s', \pi(s'))">

<br /> 

##### **The actions consists of the following:**

```math
1. Moving south (Forward)
2. Moving west (Left Horizontally)
3. Moving east (Right Horizontally) 
4. Jump Move (Up)
```
##### **The state space is the following:**

```math
[-10,10] x [1,40] = 840
```

<br />

#### **Loss function:**

#### In pursuit of constructing a policy that maximises the reward the Deep Q-learning algorithm utilizes the loss function below which is basically the difference between the two sides of the equality of the Bellman equation specified above, commonly reffered to as the temporal difference error.

<br />
&ensp;<img src="https://render.githubusercontent.com/render/math?math=\delta = Q(s, a) - (r + \gamma \max_a Q(s', a))">

<br />

#### **Reward Functions**

<br />
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=  250\hspace{0.4cm} \text{Agent reaches destination}">
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=  -1\hspace{0.4cm} \text{Agent touches the glass or the walls around the map or the glass on ground representing a river}">
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=  -1\hspace{0.4cm} \text{Agent touches diamond block}">
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=  -1\hspace{0.4cm} \text{Agent touches emerald_blck or the pole obstacles in the first phase}">
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=  -1\hspace{0.4cm} \text{Agent touches gold_block or the pole obstacles in the first phase}">
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=  -1\hspace{0.4cm} \text{Agent touches the Pink wool or the ground for initial state}">
&ensp;<img src="https://render.githubusercontent.com/render/math?math=R(s)=    1\hspace{0.4cm} \text{Every time the agent passes a quarter of the distance on the map vertically toward the finish line}">

<br />

#### The architecture of the Q-network is based on a convolutional neural network that takes the observation tensor's first index and then outputs the action size. The network is predicting the expected return of each specific action for the given input. When deciding which action to take, the epsilon greedy policy is utilized where partly, the model selects the action. At the early stages,  the actions are chosen by the random probability for exploration by starting with the hyperparameter epsilon start and decaying toward the epsilon end. The epsilon decay hyperparameter specifies how to manage the rate. The reinforcement learning algorithms pipeline begins where random or epsilon greedy action is an input to the Malmo environment where the next step is returned. The results are then recorded in the replay memory, and optimization is implemented on every iteration where random batches from replay memory are selected for the new policy training. One of the disadvantages of using a deep Q-network is that using a small action space is not sufficient to have the agent behave as desired. Additionally, this method's significant drawback is that training is slow since it converges with hard updates for the weights. 


### <u>Depth Map</u>	

#### Initially, the depth map image contains the necessary information about the distance between the objects' surface from a given viewpoint of a camera, where depth is created from the source image in grayscale format. The purpose behind the depth maps algorithm's implementation is to move left or right to steer toward the greatest depth, in essence, where the most discontinuity is in the depth map's gradient. Simply tracking through the middle line of the depth data and find the max discontinuities. In the case of a positive value, it represents a rapid change from close to far; for instance, the gap's left-hand edge where aiming to put this point in the leftmost quarter of the screen will cause it to aim for the gap. If it's a negative value, it represents a rapid change from far to close, for instance, the right-hand edge of a gap where aiming to put this point in the rightmost quarter of the screen will cause it to aim for the gap. If the delta, or the overall change in value, for the depth map is negative then the agent moves left, otherwise, it moves right. In the scenarios where there is nothing too apparent to aim for, the algorithm aims for the farthest point. Lastly, if there is no data in the depth map array, the agent simply continues to go in the direction it was already moving. In specific scenarios, the depth map algorithm faces challenges in regards to predicting depth due to texture, occlusion, and non-Lambertian surfaces, predominantly because the game is full of vibrant colors and aesthetics.

#### ***Input Image***

![My image Name](assets/images/depth_image.png)

![My image Name](assets/images/dep2.png)

![My image Name](assets/images/dep4.png)

#### *Depth Map*

![My image Name](assets/images/depth_map.jpg)

![My image Name](assets/images/dep2_map.JPG)

![My image Name](assets/images/dep4_map.JPG)
<br />

### <u>Segmenation</u>

#### Image segmentation was done for the first part of the stage to aid in computer vision and help the agent in avoiding the blocks and barriers. Training data was provided to a residual neural network by first generating dozens of images using the malmo screen capture API. Then these images were looped over pixel by pixel to segment for training purposes based upon the range of their RGB values. The sky was classified based upon if the pixel had an R value in the range (110, inf+), G value in the range (150, +in), and B value in the range (225, inf+). Barriers were either gold or green so they were classified Gold based on if they had R values in the range of (120, 210), G values in the range of (100,210), and B values in the range of (20,100), or Green based on if they had R values in the range of (15, 120), G values in the range of (80,205), and B values in the range of (25,210). Everything else was classified background. 

#### ***Code***

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

#### ***Training Data and Labels***

![My image Name](assets/images/plot0.png)

![My image Name](assets/images/plot1.png)



#### These images and manual labels for them were saved locally in our images folder. We then imported these images and labels using numpy, and split them into training and validation data with an 80/20 split. Here we then fed the training data into a residual neural network from pytorch which we would then train to automatically segment inputted images from the agent during gameplay for the barrier blocks.

#### ***Residual Net Breakdown***

![My image Name](assets/images/residualnet.png)

<br />

## **Evaluation**

### <u>DQN</u>

#### *Qualitative*

#### The overall goal of the project is for the agent to make it to the end with a minimal amount of collisions as possible. During the initial first few episodes the agent gets stuck behind a few barriers and is unable to jump over obstacles separating the different stages. However after about episode 20 it begins to be able to jump over these barriers, and after about episode 30 it can easily go up the stairs no problem reaching the end and getting the max reward for finishing. After which the agent begins to seek to minimize the amount of steps it takes to reach to get to the end since there still is a small penalty for each step that is taken. The agent takes input from both the depth map and segmented image to make its decision for the first stage, and then utilizes surrounding observations and the depth map to make its decisions for the 2nd and 3rd stage.

#### *Quantitative*

#### Below we can see the reward return graph chart. Again the goal is for the agent to make it to the end with the minimal possible collisions. The agent gets rewarded on the basis of how difficult it is for it to reach each section. Each step taken, or obstacle hit incurs a penalty for the agent, incentivizing it to reach the end in the minimal possible number of steps and least possible collisions. The finish line after the stairs has the highest possible reward, since the ultimate goal is for the agent to reach the end of the stage, after accomplishing this it then tries to reduce the amount of steps taken, and minimizes the reward. 

#### Here is the loss function which we can see converges towards zero as the agents step counts reach positive infinity.

### <u>Segmentation</u>

#### *Quantitative*

#### The evaluation for the segmentation was done while training the residual neural network. During each epoch the accuracy was computed by utilizing the validation data, which we had reserved using an 80/20 training validation split. We also computed the loss after each epoch as well, to ensure that the agent was training properly. As you can see below are our loss and accuracy graphs. Whilst the loss does generally trend downwards, the accuracy tends to oscillate after recovering from a major dip downwards, this is perhaps due to the low resolution of our training images, and limited hardware resources with regards to how much data we can provide to the network and for how long we can train.

#### *Loss*

![My image Name](assets/images/loss_segmentation.png)

#### *Accuracy*

![My image Name](assets/images/acc_segmentation.png)

#### *Qualitative*

#### The qualitative assement of the segmentation algorithm was done mainly via inspection, and comparing the segmented image produced by the neural net to what we can see for ourselves in the training data. Generally speaking the images looked better as the training went on with the edges getting crisper and more defined and the blocks being better distinguished from their surroundings. However, due to the variety of colors in our maps, we did experience a good amount of noise that caused the defintions of the blocks to be fuzzier than ideal. Further, more computational restrictions on training time added to not allowing us to train our network to be accurate as we would have liked.

#### Pre Training Image

![My image Name](assets/images/post_train_one.png)

![My image Name](assets/images/pre_train_one.png)

#### Post Training Image 

![My image Name](assets/images/post_train_one.png)

![My image Name](assets/images/post_train_two.png)

<br />

## **References**

#### The resources utilized so far have been using Malmo’s API to simulate the environment and Pytroch for creating tensors, neural networks, and optimizers. Certain functionalities from assignment that were useful were derived for this project. The following resources were used to develop implementations or to develop ideas.


1. [Policy Gradient Reinforcement Learning in Pytorch](https://medium.com/@ts1829/policy-gradient-reinforcement-learning-in-pytorch-df1383ea0baf)
2. [Building a DQN in Pytorch](https://blog.gofynd.com/building-a-deep-q-network-in-pytorch-fa1086aa5435)
3. [Pytorch Reinforcement Learning](https://github.com/bentrevett/pytorch-rl)
4. [How does the Bellman equation work in Deep RL](https://towardsdatascience.com/residual-network-implementing-resnet-a7da63c7b278)
5. [Residual Neural Nets in Pytorch](https://towardsdatascience.com/residual-network-implementing-resnet-a7da63c7b278)
6. [Pytorch and Image Segmentation](https://www.learnopencv.com/pytorch-for-beginners-semantic-segmentation-using-torchvision/)
7. [Depth Maps in Python](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html)
8. [Depth Maps in Python](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html)

