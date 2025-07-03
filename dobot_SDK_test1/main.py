import threading
import DobotDllType as dType
import random


CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #Async PTP Motion
    for i in range(0, 50):
        x, y = random.randint(160, 300), random.randint(-90,40) 
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, -45.6, 50, isQueued = 1)[0]

    # dType.SetEMotor(api, 0, 1, 10000, isQueued=1)
    # dType.SetEMotorS(api, 0, 1, 10000, 20000,isQueued=1)



    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    count = 1
    #Wait for Executing Last Command
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        print(count)
        count += 1
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)
