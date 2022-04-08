import pygame
import websockets
import asyncio
import json
import sys
import multiprocessing

pygame.init()
joysticks = []

# {
# sequenceNumber: 1234,
# eventType: "XBOX",
# input:
#   {
#      type: "DPAD"
#      key: "DPAD1",
#      value: {
#        x: 0.5,
#        y: -0.5
#      }
#   }
# }

#inputPackage = []

#set all axes "initial" value to -10 so that input is sent if they start at 1 from the start of the program
#idk actually, just a safety net
# axisValues = [-10.0,
#               -10.0,
#               -10.0,
#               -10.0,
#               -10.0,
#               -10.0]
#making this for button backlog stuff
# waitingToSendInput = [-1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       -1,
#                       ]
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
axisToString = ["L-Y",
                "L-X",
                "R-Y",
                "R-X",
                "LEFT_TRIGGER",
                "RIGHT_TRIGGER"
                ]


for i in range(0, pygame.joystick.get_count()):
    # create a Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()

async def _main():
    seqNum = 0
    async with websockets.connect("ws://untrobotics.com:9111/team",subprotocols=['team']) as websocket:
        while doStuff:
            event = pygame.event.wait()
            event_type = event.type
            #make sure that it's a button input (instead of connecting the controller, activating the mic [idk how that works], etc)
            if event_type == 1536 or event_type == 1538 or event_type == 1539 or event_type == 1540:
                eventDict = event.__dict__
                key = ""
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
                await websocket.send(json.dumps(
                {
                        'teamNumber': teamNumber,
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
    # clock.tick(1)
    # for event in pygame.event.get():
    #     inputPackage.append(event)
    # if inputPackage:
    #     print(inputPackage)
    #     inputPackage.clear()
        #if the event is for an axis input
    #     if event.type==1536:
    #         newAxisValue = event.__dict__['value']
    #         axisNum = event.__dict__['axis']
    #         if newAxisValue < .01:
    #             newAxisValue = 0
    #         #only send the value if it changed by more than 0.01 since the last update
    #         if abs(newAxisValue-axisValues[axisNum-1])>.01:
    #             toAdd = True
    #             #checking if an input for this axis was already sent this "frame"
    #             for i in range(len(inputPackage)):
    #                 #make sure that it is an axes input, and that the axes nums are equal
    #                 if inputPackage[i][0]=='a' and inputPackage[i][1]==axisNum:
    #                     #overwriting the axis value
    #                     axisValues[axisNum] = newAxisValue
    #                     inputPackage[i]= ('a', axisNum, newAxisValue)
    #                     toAdd = False
    #                     break
    #             if toAdd:
    #                 axisValues[axisNum] = newAxisValue
    #                 inputPackage.append(('a', axisNum, newAxisValue))
    #     # if the event is for a button
    #     elif event.type==1539 or event.type==1540:
    #         buttonNum = event.__dict__['button']
    #         if waitingToSendInput[buttonNum]==-1:
    #             #Adds a tuple containing what button was pressed and if the button is pressed down (true if it is)
    #             inputPackage.append(('b', buttonNum, event.type == 1539))
    #             waitingToSendInput[buttonNum]= 1 if event.type==1539 else 0
    #         elif waitingToSendInput[buttonNum]==0:
    #     #d-pad is rarely used, so we can make it the last else
    #     #there should be no other inputs besides this
    #     elif event.type==1538:
    #         inputPackage.append(('d',event.__dict__['value']))
    # if inputPackage:
    #     print(inputPackage)
    #     #send inputPackage
    #     inputPackage.clear()
    #     #print(inputPackage)

# def waitToKill():
#     while True:
#         msg = input("Enter \"-E\" to exit, without the quotation marks.\n")
#         if msg == "-E":
#             sys.exit()

teamNumber = sys.argv[1]
asyncio.run(_main())
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