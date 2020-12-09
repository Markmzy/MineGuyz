try:
    from malmo import MalmoPython
except:
    import MalmoPython
from map_generator_final import GetMissionXML
from RL_DQN import QNetwork, Hyperparameters, get_action, prepare_batch, learn, log_returns
import time

def init_malmo(agent_host,recordingsDirectory, video_width, video_height):
    
    my_mission = MalmoPython.MissionSpec(GetMissionXML(Hyperparameters.SIZE, Hyperparameters.OBS_SIZE, Hyperparameters.MAX_EPISODE_STEPS, video_width ,video_height), True)
    my_mission.setViewpoint(0)

    agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
    agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
    
    my_mission_record = MalmoPython.MissionRecordSpec()


    if recordingsDirectory:
        my_mission_record.recordRewards()
        my_mission_record.recordObservations()
        my_mission_record.recordCommands()
        if agent_host.receivedArgument("record_video"):
            my_mission_record.recordMP4(24,2000000)

    if recordingsDirectory:
        my_mission_record.setDestination(recordingsDirectory + "//" + "Mission_" + str(test + 1) + ".tgz")

    max_retries = 3
    my_clients = MalmoPython.ClientPool()
    my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available
    my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10001))
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_clients, my_mission_record, 0, "MineGuyz" )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                time.sleep(2)

    return agent_host