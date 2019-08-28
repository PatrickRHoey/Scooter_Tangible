#!usr/bin/env python

import rospy
from tangible_master.msg import button_leds

def set_state(state_name, recieved_msg):
    """
    Handles the state of the tangible user interface based upon the input recieved via the buttons and current system
    status
    """
    pick_cloud_gathered = True
    basket_complete = True
    place_cloud_gathered = True



    if(state_name == "driving"):
        if(recieved_msg.button[2] == 1):
            #state_name = "gather_pick_cloud"
            state_name = "pick"

    #TODO add is pointcloud gathered flag
    if(state_name == "gather_pick_cloud"):
        if(pick_cloud_gathered):
            state_name == "pick"

    elif(state_name == "pick"):
        if(recieved_msg.button[5] == 1):
            state_name = "driving"
        elif(recieved_msg.button[0] == 1):
            state_name = "confirm_object"
            rospy.sleep(5)

    elif(state_name == "confirm_object"):
        if(recieved_msg.button[0] == 1):
            state_name = "confirm_pick"
            rospy.sleep(5)
        elif(recieved_msg.button[1] == 1):
            state_name = "driving"

    #Not sure how this is working with the grasp sucess detection code
    elif(state_name == "confirm_pick"):
        if(recieved_msg.button[0] == 1):
            state_name = "object_held"
            rospy.sleep(5)

        elif(recieved_msg.button[5] == 1):
            state_name = "driving"

    elif(state_name == "object_held"):
        if(recieved_msg.button[5] == 1):
            state_name = "driving"
        elif(recieved_msg.button[3] == 1):
            state_name = "gather_place_cloud"
        elif(recieved_msg.button[4] == 1):
            state_name = "basket"

    #TODO Need complete flag
    elif(state_name == "basket"):
        if(basket_complete):
            state_name = "driving"
    #TODO need cloudReady flag
    elif(state_name == "gather_place_cloud"):
        if(place_cloud_gathered):
            state_name = "place"

    elif(state_name == "place"):
        if(recieved_msg.button[0] == 1):
            state_name = "place_confirm"

    elif(state_name == "place_confirm"):
        if(recieved_msg.button[0] == 1):
            state_name = "placing"
        elif(recieved_msg.button[1] == 1):
            state_name = "place"

    #TODO Need placed confirm flag  ######and (placed_complete == True)
    elif((state_name == "placing")):
        state_name = "driving"

    print(str(recieved_msg) + '\n')
    print("current state name: " + state_name + '\n')
    return state_name





def compare_state(state_name, button_msg):
    """
    Compares current state to desired LED state for the interface
    """
    #1 means solid light on, 2 means that it should be blinking, 0 is off
    #first led is thinking, second is ready for selection
    if(state_name == "driving"):
        button_msg.button = [0, 0, 2, 0, 0, 1]
        button_msg.leds = [0, 0, 0]

    elif(state_name == "gather_pick_cloud"):
        button_msg.button = [0, 0, 1, 0, 0, 0]
        button_msg.leds = [1, 0, 0]

    elif(state_name == "pick"):
        button_msg.button = [2, 2, 1, 0, 0, 0]
        button_msg.leds = [0, 1, 0]

    elif(state_name == "confirm_object"):
        button_msg.button = [2, 2, 1, 0, 0, 0]
        button_msg.leds = [0, 0, 0]

    elif(state_name == "confirm_pick"):
        button_msg.button = [2, 2, 0, 0, 0, 0]
        button_msg.leds = [0, 0, 0]


    elif(state_name == "object_held"):
        button_msg.button = [0, 0, 0, 2, 2, 1]
        button_msg.leds = [0, 0, 0]


    elif(state_name == "gather_place_cloud"):
        button_msg.button = [0, 0, 0, 1, 0, 0]
        button_msg.leds = [1, 0, 0]


    elif(state_name == "place"):
        button_msg.button = [2, 2, 0, 1, 0, 0]
        button_msg.leds = [0, 1, 0]


    elif(state_name == "place_confirm"):
        button_msg.button = [2, 2, 0, 1, 0, 0]
        button_msg.leds = [0, 0, 0]


    elif(state_name == "basket"):
        button_msg.button = [0, 0, 0, 0, 1, 0]
        button_msg.leds = [0, 0, 0]


    elif(state_name == "placing"):
        button_msg.button = [1, 0, 0, 1, 0, 0]
        button_msg.leds = [0, 0, 0]

    return button_msg

