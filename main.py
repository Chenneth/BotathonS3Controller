import signal

import pygame
import websockets
import asyncio
import json
import sys
import multiprocessing
async def _main():
    seqNum = 0
    print("Trying to connect to websocket")
    eventCount = 0
    # async with websockets.connect("ws://untrobotics.com:9111/team",subprotocols=['team']) as websocket:
    async for websocket in websockets.connect("ws://untrobotics.com:81/team",subprotocols=['team']):
        # while doStuff:
        print("Connected to websocket")
        try:
            while doStuff:
                event = pygame.event.wait()
                eventCount += 1
                event_type = event.type
                eventDict = event.__dict__
                #make sure that it's a button input (instead of connecting the controller,
                # activating the mic [idk how that works], etc)
                if event_type == 1536 or event_type == 1538 or event_type == 1539 or event_type == 1540:

                    key = ""
                    #makes sure the instance id has a number assigned to it
                    if eventDict["instance_id"] not in devToTeamNum.keys():
                        print("Controller of instance ID {} is not assigned a team number. Ignoring input."
                              "Are you sure less than 2 controllers were connected first?".format(eventDict['instance_id']))
                        break
                    if event_type == 1536: #Input is an axis
                        key = axisToString[eventDict['axis']]
                        value = eventDict['value']

                    elif event_type==1538: #Input is D-Pad
                        key = "DPAD1"
                        coords = eventDict['value']
                        value = {'x':coords[0], 'y':coords[1]}
                    else: #Input is a button
                        key = buttonToString[eventDict['button']]
                        value = event_type == 1539
                    print("Sending input for {}, team number {}, value of {}."
                          "Total inputs sent: {}".format(key, devToTeamNum[eventDict['instance_id']], value, seqNum))
                    print(event)
                    await websocket.send(json.dumps(
                    {
                            'teamNumber': devToTeamNum[eventDict['instance_id']],
                            'sequenceNumber': seqNum,
                            'eventType': "XBOX",
                            'input':
                                {
                                    'type': "AXIS" if event_type == 1536 else "DPAD" if event_type == 1538 else "BUTTON",
                                    'key': key,
                                    'value': value
                                }
                    }
                    ))
                    seqNum += 1
                    print("Input successfully sent.")
                #todo: does not work, pygame assigns the same instance ID to the controllers when dc'ing and rc'ing
                # elif event_type == 1541 \
                #         and len(openTeamNums) > 0:
                #                         # This is the event for when
                #                         # a controller is connected, just reinitializing the list
                #     print("New controller detected.")
                #     # joysticks.clear()
                #     for i in range(0, pygame.joystick.get_count()):
                #         # create a Joystick object in our list
                #         newJoystick = pygame.joystick.Joystick(i)
                #         joysticks.append(newJoystick)
                #         joysticks[i].init()
                #         joysticks_count = len(joysticks)
                #         #assigns the last joystick added the corresponding team number based on its index
                #         devToTeamNum[joysticks[i].get_instance_id()] = openTeamNums[0]
                #         openTeamNums.pop(0)
                #         if len(openTeamNums) < 1:
                #             print("No more open team numbers to assign.")
                #             break
                # #controller is disconnected
                # elif event_type==1542 and eventDict['instance_id'] in devToTeamNum:
                #     instanceID = eventDict['instance_id']
                #     openTeamNums.append(devToTeamNum[instanceID])
                #     # potentialDeviceID.append(instanceID)
                #     devToTeamNum.pop(instanceID)
                #     print("Removed the joystick and team numbers from active dictionary.")
                #     #need to remove the controller
                #     for i in range(len(joysticks)):
                #         if joysticks[i].get_instance_id() == instanceID:
                #             joysticks.pop(i)
                #             print("Removed joystick from array")
                #             # joysticks_count = len(joysticks)
                #             break
                else:
                    print(event)
                    # print( await websocket.recv())
        except websockets.ConnectionClosed:
            print("Web Socket disconnected. Trying to reconnect...")
            continue
    print("Exited loop.")


joysticks = []
doStuff = True
buttonToString = ["A_BUTTON",
                  "B_BUTTON",
                  "X_BUTTON",
                  "Y_BUTTON",
                  "LEFT_BUMPER",
                  "RIGHT_BUMPER",
                  "VIEW_BUTTON",
                  "MENU_BUTTON",
                  "L_JOY_PRESS",
                  "R_JOY_PRESS",
                  "XBOX_BUTTON",
                  "HOME_BUTTON",]
axisToString = ["L-X",
                "L-Y",
                "R-X",
                "R-Y",
                "LEFT_TRIGGER",
                "RIGHT_TRIGGER"
                ]

devToTeamNum = {}
teamNums = [0,0]
openTeamNums = []

# potentialDeviceID = []
# guidToTeamNum = {}
try:
    teamNumber = sys.argv[1]
    teamNumberTwo = sys.argv[2]

    #making sure the arg is an int
    int(teamNumber)
    int(teamNumberTwo)
    teamNums[0] = teamNumber
    teamNums[1] = teamNumberTwo
except (IndexError, ValueError):
    print("\nWARNING:\n\nThis executable should be run through command prompt with your team number as an argument.\n"
          "Usage:\t'UNTRoboticsXBoxController.exe <team number>'\n"
          "Ex:\t\t'UNTRoboticsXBoxController.exe 12'\n"
          "Quitting program...")
    quit()

pygame.init()
print("Trying to add controller to list")
for i in range(0, pygame.joystick.get_count()):
    # create a Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    print(joysticks[i])
    #only adding 2 controllers we care about
    if i < 2:
        # print("i < 2. Adding to list")
        devToTeamNum[joysticks[i].get_instance_id()] = teamNums[i]
        # guidToTeamNum[joysticks[i].()] = teamNums[i]
        # print("Initialized controller instance {} to team number {}"
        #       .format(joysticks[i].get_instance_id(), teamNums[i]))

    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print("Initialized {} controller(s).".format(i+1))
# for openNum in teamNums:
#     openTeamNums.append(openNum)
asyncio.run(_main())
# loop = asyncio.get_event_loop()
# main_task = asyncio.ensure_future(_main())
# for signal in [signal.SIGINT, signal.SIGTERM]:
#     loop.add_signal_handler(signal,main_task.cancel)
# try:
#     loop.run_forever(main_task)
# finally:
#     loop.close()

# p1 = multiprocessing.Process(target=waitToKill)
# p1.start()

#List of event types (as far as I'm aware, this numbering is constant)
#Axes input:    1536
#Button Down:   1539        True
#Button Up:     1540        False
#D-Pad:         1538
#there's also the gamepad being connected and mic/headphones (but no one cares about that)

#list of buttons/axes and their corresponding xbox input:
#NOTE: D-Pad comes with a value in an ordered pair representing x,y
#Axes 1,0:  Left joystick, x,y
#Axes 3,2:  Right joystick, x,y
#Axis 4:    Left Trigger, positive is pushed in
#Axis 5:    Right Trigger, same as Axis 4 (Left Trigger)
#Button 0:  A Button
#Button 1:  B Button
#Button 2:  X Button
#Button 3:  Y Button
#Button 4:  Left Bumper
#Button 5:  Right Bumper

#The three center buttons (excluding the xbox)
#Button 6:  Left center Button
#Button 7:  Right Center Button
#Button 11: Center Center Button

#Button 8:  Left Joystick Button
#Button 9:  Right Joystick Button
#Button 10: XBox Button