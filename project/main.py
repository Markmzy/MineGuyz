try:
    from malmo import MalmoPython
except:
    import MalmoPython

import os
import glob
import sys
import time
import json
import random
from tqdm import tqdm
from collections import deque
import matplotlib.pyplot as plt 
import numpy as np
from numpy.random import randint
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from map_generator_final import GetMissionXML
from RL_DQN import QNetwork, Hyperparameters, get_action, prepare_batch, learn, log_returns
from get_observation import get_observation
from init_malmo import init_malmo
from vision import view_surrounding, clear_images, get_img, Eyes
import malmoutils
from past.utils import old_div

os.environ['KMP_DUPLICATE_LIB_OK']='True'

GET_VISION_DATA= True
VISION_ENABLED= False

#### Depth_Map Testing
def processFrame( frame ):

    global current_yaw_delta_from_depth

    y = int(old_div(video_height, 2))
    rowstart = y * video_width
    
    v = 0
    v_max = 0
    v_max_pos = 0
    v_min = 0
    v_min_pos = 0
    
    dv = 0
    dv_max = 0
    dv_max_pos = 0
    dv_max_sign = 0
    
    d2v = 0
    d2v_max = 0
    d2v_max_pos = 0
    d2v_max_sign = 0
    
    for x in range(0, video_width):
        nv = frame[(rowstart + x) * 4 + 3]
        ndv = nv - v
        nd2v = ndv - dv

        if nv > v_max or x == 0:
            v_max = nv
            v_max_pos = x
            
        if nv < v_min or x == 0:
            v_min = nv
            v_min_pos = x

        if abs(ndv) > dv_max or x == 1:
            dv_max = abs(ndv)
            dv_max_pos = x
            dv_max_sign = ndv > 0
            
        if abs(nd2v) > d2v_max or x == 2:
            d2v_max = abs(nd2v)
            d2v_max_pos = x
            d2v_max_sign = nd2v > 0
            
        d2v = nd2v
        dv = ndv
        v = nv
    

    if dv_max_sign:
        edge = old_div(video_width, 4)
    else:
        edge = 3 * video_width / 4

    if d2v_max > 8:
        current_yaw_delta_from_depth = (old_div(float(d2v_max_pos - edge), video_width)) 
    else:
        if v_max < 255:
            current_yaw_delta_from_depth = (old_div(float(v_max_pos), video_width)) - 0.5
        else:
            if current_yaw_delta_from_depth < 0:
                current_yaw_delta_from_depth = -1
            else:
                current_yaw_delta_from_depth = 1


current_yaw_delta_from_depth = 0
video_width = 512
video_height = 512

def main(agent_host):
    device = torch.device("cpu")
    if VISION_ENABLED:
        eyes = Eyes()
    if GET_VISION_DATA:
        clear_images()
    malmoutils.fix_print()
    malmoutils.parse_command_line(agent_host)
    recordingsDirectory = malmoutils.get_recordings_directory(agent_host)

    q_network = QNetwork((2, Hyperparameters.OBS_SIZE, Hyperparameters.OBS_SIZE), len(Hyperparameters.ACTION_DICT))
    target_network = QNetwork((2, Hyperparameters.OBS_SIZE, Hyperparameters.OBS_SIZE), len(Hyperparameters.ACTION_DICT))
    target_network.load_state_dict(q_network.state_dict())

    optim = torch.optim.Adam(q_network.parameters(), lr= Hyperparameters.LEARNING_RATE)

    replay_buffer = deque(maxlen=Hyperparameters.REPLAY_BUFFER_SIZE)

    global_step = 0
    num_episode = 0
    epsilon = 1
    start_time = time.time()
    returns = []
    steps = []
    loss_array = []

    loop = tqdm(total=Hyperparameters.MAX_GLOBAL_STEPS, position=0, leave=False)

    result_dataset = []

    print("Global Step", Hyperparameters.MAX_GLOBAL_STEPS)
    while global_step < Hyperparameters.MAX_GLOBAL_STEPS:
        episode_step = 0
        episode_return = 0
        episode_loss = 0
        done = False
        

        #Initialize
        agent_host = init_malmo(agent_host,recordingsDirectory, video_width,video_height)
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            #for error in world_state.errors:
                #print("\nError:",error.text)
        obs = get_observation(world_state, agent_host)


        #Testing  
        agent_host.sendCommand( "move 1" )

        while world_state.is_mission_running:
            time.sleep(2)  
            #Depth Implementation
            while world_state.number_of_video_frames_since_last_state < 1 and world_state.is_mission_running:
                time.sleep(0.05)
                world_state = agent_host.getWorldState()

            if world_state.is_mission_running:
                processFrame(world_state.video_frames[0].pixels)
                print("Yaw Delta ", current_yaw_delta_from_depth)  
                #agent_host.sendCommand( "turn " + str(current_yaw_delta_from_depth) )
                if current_yaw_delta_from_depth > 0:
                    agent_host.sendCommand(Hyperparameters.ACTION_DICT[1])
                else:
                    agent_host.sendCommand(Hyperparameters.ACTION_DICT[2])
        

            action_idx = get_action(obs, q_network, epsilon)
            command = Hyperparameters.ACTION_DICT[action_idx]

            agent_host.sendCommand(command)
            #agent_host.sendCommand( "turn " + str(current_yaw_delta_from_depth) )

            #time.sleep(.3)

            if VISION_ENABLED:
                input_img_temp = get_img(world_state, agent_host,eyes,device,video_width,video_height)
                print("Testing 555")
            episode_step += 1
            if episode_step >= Hyperparameters.MAX_EPISODE_STEPS or \
                    (obs[0, int(Hyperparameters.OBS_SIZE/2)+1, int(Hyperparameters.OBS_SIZE/2)] == -1 and \
                    command == 'movesouth 1'):
                done = True
                time.sleep(2)  

            world_state = agent_host.getWorldState()
            if GET_VISION_DATA and world_state.is_mission_running:
                result_dataset.append(view_surrounding(video_height, video_width, world_state.video_frames[0].pixels, global_step))
            
            for error in world_state.errors:
                print("Error:", error.text)
            
            next_obs = get_observation(world_state, agent_host) 
        
            reward = 0
            for r in world_state.rewards:
                reward += r.getValue()
            episode_return += reward

            replay_buffer.append((obs, action_idx, next_obs, reward, done))
            obs = next_obs

            global_step += 1
            #print(global_step)
            if global_step == Hyperparameters.MAX_GLOBAL_STEPS:
                break

            if global_step > Hyperparameters.START_TRAINING and global_step % Hyperparameters.LEARN_FREQUENCY == 0:
                batch = prepare_batch(replay_buffer)
                loss = learn(batch, optim, q_network, target_network)
                episode_loss += loss

                if epsilon > Hyperparameters.MIN_EPSILON:
                    epsilon *= Hyperparameters.EPSILON_DECAY

                if global_step % Hyperparameters.TARGET_UPDATE == 0:
                    target_network.load_state_dict(q_network.state_dict())



        num_episode += 1
        returns.append(episode_return)
        loss_array.append(episode_loss)
        steps.append(global_step)
        avg_return = sum(returns[-min(len(returns), 10):]) / min(len(returns), 10)
        loop.update(episode_step)
        loop.set_description('Episode: {} Steps: {} Time: {:.2f} Loss: {:.2f} Last Return: {:.2f} Avg Return: {:.2f}'.format(
            num_episode, global_step, (time.time() - start_time) / 60, episode_loss, episode_return, avg_return))

        if num_episode > 0 and num_episode % 10 == 0:
            log_returns(steps, loss_array)
            #print()

    #print(len(result_dataset))
    np.save("images/image_labels",np.array(result_dataset))
    #print('Labels Saved')
        

if __name__ == '__main__':
    
    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        #print('ERROR:', e)
        #print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        #print(agent_host.getUsage())
        exit(0)

    main(agent_host)

