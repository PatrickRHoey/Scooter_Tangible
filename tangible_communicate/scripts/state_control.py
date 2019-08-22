#!usr/bin/env python

import rospy
from tangible_master.msg import button_leds

def set_state(state_name, recieved_msg):
    """
    Handles the state of the tangible user interface based upon the input recieved via the buttons and current system
    status
    """
    if(state_name == "driving"):
        if(recieved_msg.button == [0, 0, 1, 0, 0, 0]):
            state_name = "pick"
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
            state_name = "place"
        elif(recieved_msg == [0, 0, 0, 0, 1, 0]):
            state_name = "basket"
        else:
            pass

    #TODO Need complete flag
    if(state_name == "basket"):
        if(complete):
            state_name = "drive"
        else:
            pass
    #TODO need cloudReady flag
    if(state_name == "place"):
        if(cloud_ready and recieved_msg == [1, 0, 0, 0, 0, 0]):
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
    if(state_name == "placing" and placed):
        state_name = "driving"





def compare_state(state_name, button_msg):
    """
    Compares current state to desired LED state for the interface
    """

    if(state_name == "driving"):
        pass
    elif(state_name == "pick"):
        pass
    elif(state_name == "confirm_object"):
        pass
    elif(state_name == "confirm_pick"):
        pass
    elif(state_name == "object_held"):
        pass
    elif(state_name == "place"):
        pass
    elif(state_name == "place_confirm"):
        pass
    elif(state_name == "basket"):
        pass
    elif(state_name == "placing"):
        pass
