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
### Approach
#### Todo 

<br />
### Evaluation
#### Todo

<br />
### Remaining Goals 
#### Todo

<br />
### Resources Used
#### Todo
