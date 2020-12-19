import random
blocktype = ["gold_block", "emerald_block"]
color = ["MAGENTA", "PURPLE", "BLUE", "BROWN", "RED"]


def GetMissionXML(SIZE , OBS_SIZE, MAX_EPISODE_STEPS, video_width, video_height):
  WIDTH = 10 
  myxml = ""
  JUMP_MOVE_ENABLED = True

  bridgeL = int(SIZE/4)
  bridgeW = int(SIZE/8)
  riverW = WIDTH-int(SIZE/8)
  
  for x in range(-WIDTH,WIDTH+1):
        for y in range(1,int(SIZE/4)):			
            if random.random() < 0.1:
                myxml += "<DrawCuboid x1='{}' y1='10' z1='{}' x2='{}' y2='12' z2='{}'  type='{}' />".format(x,y,x,y,random.choice(blocktype))
              
  version = random.randrange(2)
  myxml2 = "" 
  if version == 0:
    x = int(WIDTH/2 +1)
    for y in range(int(SIZE*2/3)+2, SIZE,2):
        if x == int(WIDTH/2 +1):
            myxml2 += "<DrawCuboid x1='{}' y1='10' z1='{}' x2='{}' y2='12' z2='{}'  type='{}' />".format(x,y,x+1,y,random.choice(blocktype))
            myxml2 += "<DrawBlock x='{}' y='10' z='{}'  type='{}' />".format(x+2,y,random.choice(blocktype))
            x=WIDTH-2
        else:
            myxml2 += "<DrawBlock x='{}' y='10' z='{}'  type='{}' />".format(x,y,random.choice(blocktype))
            myxml2 += "<DrawCuboid x1='{}' y1='10' z1='{}' x2='{}' y2='12' z2='{}'  type='{}' />".format(x+1,y,x+2,y,random.choice(blocktype))
            x=int(WIDTH/2 +1)
    for x in range(-WIDTH,int(-WIDTH/2)):
        for y in range(int(SIZE*2/3)+2, SIZE):      
            if random.random() < 0.2:
                myxml2 += "<DrawBlock x='{}' y='9' z='{}'  type='glass' />".format(x,y)
  else:
    x = -WIDTH+1
    for y in range(int(SIZE*2/3)+2, SIZE,2):
        if x == -WIDTH+1:
            myxml2 += "<DrawCuboid x1='{}' y1='10' z1='{}' x2='{}' y2='12' z2='{}'  type='{}' />".format(x,y,x+1,y,random.choice(blocktype))
            myxml2 += "<DrawBlock x='{}' y='10' z='{}'  type='{}' />".format(x+2,y,random.choice(blocktype))
            x=int(-WIDTH/2 -2)
        else:
            myxml2 += "<DrawBlock x='{}' y='10' z='{}'  type='{}' />".format(x,y,random.choice(blocktype))
            myxml2 += "<DrawCuboid x1='{}' y1='10' z1='{}' x2='{}' y2='12' z2='{}'  type='{}' />".format(x+1,y,x+2,y,random.choice(blocktype))
            x=-WIDTH+1
    for x in range(int(WIDTH/2),WIDTH):
        for y in range(int(SIZE*2/3)+2, SIZE):      
            if random.random() < 0.2:
                myxml2 += "<DrawBlock x='{}' y='9' z='{}'  type='glass' />".format(x,y)

  if JUMP_MOVE_ENABLED == True:
    myxml2 += "<DrawCuboid x1='-2' y1='10' z1='{}' x2='2' y2='15' z2='{}' type='air'/>".format(int(SIZE*2/3)+1,SIZE)
    for x in range(int(SIZE*2/3)+2,SIZE,2):
    	myxml2 += "<DrawCuboid x1='-2' y1='10' z1='{}' x2='2' y2='{}' z2='{}' type='stone'/>".format(x,int((x-int(SIZE*2/3)-2)/2)+10,x+1)
                
  return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>10000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;1;"/>
                  <DrawingDecorator>''' + \
                    "<DrawCuboid x1='{}' y1='0' z1='-6' x2='{}' y2='8' z2='{}' type='stone'/>".format(-WIDTH-1,WIDTH+1,SIZE+1) + \
                    "<DrawCuboid x1='{}' y1='10' z1='-6' x2='{}' y2='15' z2='{}' type='glass'/>".format(-WIDTH-1,WIDTH+1,SIZE+1) + \
                    "<DrawCuboid x1='{}' y1='10' z1='-5' x2='{}' y2='40' z2='{}' type='air'/>".format(-WIDTH,WIDTH,SIZE) + \
                    "<DrawCuboid x1='{}' y1='9' z1='-6' x2='{}' y2='9' z2='-1' type='wool' colour='PINK'/>".format(-WIDTH-1,WIDTH+1) + \
                    "<DrawCuboid x1='{}' y1='9' z1='0' x2='{}' y2='9' z2='{}' type='wool' colour='{}'/>".format(-WIDTH-1,WIDTH+1,int(SIZE/4),random.choice(color)) + \
                    "<DrawCuboid x1='{}' y1='9' z1='{}' x2='{}' y2='10' z2='{}' type='diamond_block'/>".format(-WIDTH-1,int(SIZE/4)+1,WIDTH+1,int(SIZE/4)+1) + \
                    "<DrawCuboid x1='{}' y1='9' z1='{}' x2='{}' y2='9' z2='{}' type='wool' colour='{}'/>".format(-WIDTH-1,int(SIZE/4)+2,WIDTH+1,int(SIZE*2/3)-2,random.choice(color)) + \
                    "<DrawCuboid x1='{}' y1='9' z1='{}' x2='{}' y2='10' z2='{}' type='iron_block'/>".format(-WIDTH,int(SIZE*2/3)-1,WIDTH,int(SIZE*2/3)-1) + \
                    "<DrawCuboid x1='{}' y1='9' z1='{}' x2='{}' y2='9' z2='{}' type='wool' colour='{}'/>".format(-WIDTH-1,int(SIZE*2/3),WIDTH+1,SIZE+1,random.choice(color)) + \
                    "<DrawCuboid x1='{}' y1='9' z1='{}' x2='{}' y2='10' z2='{}' type='redstone_block'/>".format(-WIDTH,SIZE+1,WIDTH,SIZE+1) + \
                    "<DrawCuboid x1='{}' y1='8' z1='-5' x2='{}' y2='8' z2='{}' type='water'/>".format(-WIDTH,WIDTH,SIZE) + \
                    myxml + \
                  '''</DrawingDecorator>
                  <AnimationDecorator ticksPerUpdate="40">
                    <Linear>
                      <CanvasBounds>''' +\
                        "<min x='{}' y='9' z='0'/>".format(-WIDTH-riverW-1) +\
                        "<max x='{}' y='9' z='100'/>".format(WIDTH+riverW) +\
                      '''</CanvasBounds>'''+ \
                      "<InitialPos x='{}' y='9' z='{}'/>".format(-WIDTH-riverW-1,int(SIZE/3)) +\
                      "<InitialVelocity x='1' y='0' z='0'/>" +\
                    '''</Linear>
                    <DrawingDecorator>''' + \
                      "<DrawCuboid x1='0' y1='0' z1='0'  x2='{}' y2='0' z2='{}' type='glass'/>".format(riverW-1,bridgeL) +\
                      "<DrawCuboid x1='{}' y1='0' z1='0'  x2='{}' y2='0' z2='{}' type='wool' colour='ORANGE'/>".format(riverW,riverW+bridgeW,bridgeL) +\
                      "<DrawCuboid x1='{}' y1='0' z1='0'  x2='{}' y2='0' z2='{}' type='glass'/>".format(riverW+bridgeW+1,2*riverW+bridgeW-1,bridgeL) +\
                      "<DrawCuboid x1='{}' y1='0' z1='0'  x2='{}' y2='0' z2='{}' type='wool' colour='ORANGE'/>".format(2*riverW+bridgeW,2*riverW+2*bridgeW,bridgeL) +\
                      "<DrawCuboid x1='{}' y1='0' z1='0'  x2='{}' y2='0' z2='{}' type='glass'/>".format(2*riverW+2*bridgeW+1,3*riverW+2*bridgeW,bridgeL) +\
                    '''</DrawingDecorator>
                  </AnimationDecorator>
                  
                  <DrawingDecorator>''' + \
                    "<DrawCuboid x1='-5' y1='10' z1='{}' x2='5' y2='15' z2='{}' type='glass'/>".format(int(SIZE*2/3)+1,SIZE) + \
                    myxml2 + \
                  '''</DrawingDecorator>
                  
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>Diablo!</Name>
                <AgentStart>
                    <Placement x="0.5" y="10" z="0.5" yaw="0"/>
                </AgentStart>
                <AgentHandlers>
                  <VideoProducer want_depth="true">
                    <Width>''' + str(video_width) + '''</Width>
                    <Height>''' + str(video_height) + '''</Height>
                  </VideoProducer>
                  <DiscreteMovementCommands/>
                  <ObservationFromFullStats/>
                  <ObservationFromGrid>
                            <Grid name="floorAll">
                                <min x="-'''+str(int(OBS_SIZE/2))+'''" y="-1" z="-'''+str(int(OBS_SIZE/2))+'''"/>
                                <max x="'''+str(int(OBS_SIZE/2))+'''" y="0" z="'''+str(int(OBS_SIZE/2))+'''"/>
                            </Grid>
                  </ObservationFromGrid>
                  <AgentQuitFromReachingCommandQuota total="'''+str(MAX_EPISODE_STEPS)+'''" />
                  <RewardForTouchingBlockType>
                    <Block reward="100" type="diamond_block" behaviour="onceOnly" />
                    <Block reward="150" type="iron_block" behaviour="onceOnly" />
                    <Block reward="-10" type="glass" />
                    <Block reward="-1" type="gold_block" />
                    <Block reward="-1" type="emerald_block" />
                  </RewardForTouchingBlockType>
                  <RewardForSendingCommand reward = "-0.1"/>
                  <RewardForMissionEnd rewardForDeath="0">
                      <Reward description="found_goal" reward="250" />
                  </RewardForMissionEnd>
                  <AgentQuitFromTouchingBlockType>
                      <Block type="redstone_block" description="found_goal"/>
                  </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
