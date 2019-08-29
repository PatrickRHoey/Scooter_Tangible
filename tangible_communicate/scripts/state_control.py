#!usr/bin/env python

import rospy
from tangible_master.msg import button_leds

def set_state(state_name, recieved_msg, pick_cloud_gathered, basket_complete, place_cloud_gathered, placed_complete):
    """
    Handles the state of the tangible user interface based upon the input recieved via the buttons and current system
    status
    buttons go in this order [yes, no, pick, place, basket, drive]
    leds go in this order [thinking, wait for input, wrist lasers]
    """
    if(state_name == "driving"):
        if(recieved_msg.button == [0, 0, 1, 0, 0, 0]):
            state_name = "gather_pick_cloud"
        else:
            pass

    #TODO add is pointcloud gathered flag
    if(state_name == "gather_pick_cloud"):
        if(pick_cloud_gathered):
            state_name == "pick"
        else:
            pass

    if(state_name == "pick"):
        if(recieved_msg.button == [0, 0, 0, 0, 0, 1]):
            state_name = "driving"
        elif(recieved_msg.button == [1, 0, 0, 0, 0, 0]):
            state_name = "confirm_object"
        else:
            pass

    if(state_name == "confirm_object"):
        if(recieved_msg.button == [1, 0, 0, 0, 0, 0]):
            state_name = "confirm_pick"
        elif(recieved_msg.button == [0, 1, 0, 0, 0, 0]):
            state_name = "driving"
        else:
            pass

    #Not sure how this is working with the grasp sucess detection code
    if(state_name == "confirm_pick"):
        if(recieved_msg == [1, 0, 0, 0, 0, 0]):
            state_name = "object_held"
        elif(recieved_msg == [1, 0, 0, 0, 0, 0]):
            state_name = "driving"
        else:
            pass

    if(state_name == "object_held"):
        if(recieved_msg == [0, 0, 0, 0, 0, 1]):
            state_name = "driving"
        elif(recieved_msg == [0, 0, 0, 1, 0, 0]):
            state_name = "gather_place_cloud"
        elif(recieved_msg == [0, 0, 0, 0, 1, 0]):
            state_name = "basket"
        else:
            pass

    #TODO Need complete flag
    if(state_name == "basket"):
        if(basket_complete):
            state_name = "driving"
        else:
            pass
    #TODO need cloudReady flag
    if(state_name == "gather_place_cloud"):
        if(place_cloud_gathered):
            state_name = "place"
        else:
            pass

    if(state_name == "place"):
        if(recieved_msg == [1, 0, 0, 0, 0, 0]):
            state_name = "place_confirm"
        else:
            pass

    if(state_name == "place_confirm"):
        if(recieved_msg == [1, 0, 0, 0, 0, 0]):
            state_name = "placing"
        elif(recieved_msg == [0, 1, 0, 0, 0, 0]):
            state_name = "place"
        else:
            pass

    #TODO Need placed confirm flag
    if(state_name == "placing" and placed_complete):
        state_name = "driving"





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
        button_msg.leds = [0, 1, 1]

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
        button_msg.leds = [0, 1, 1]


    elif(state_name == "place_confirm"):
        button_msg.button = [2, 2, 0, 1, 0, 0]
        button_msg.leds = [0, 0, 0]


    elif(state_name == "basket"):
        button_msg.button = [0, 0, 0, 0, 1, 0]
        button_msg.leds = [0, 0, 0]


    elif(state_name == "placing"):
        button_msg.button = [1, 0, 0, 1, 0, 0]
        button_msg.leds = [0, 0, 1]


