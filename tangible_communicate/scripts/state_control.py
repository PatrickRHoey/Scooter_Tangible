#!usr/bin/env python

import rospy
from tangible_master.msg import button_leds

def set_state(tangible):
    """
    Handles the state of the tangible user interface based upon the input recieved via the buttons and current system
    status
    buttons go in this order [yes, no, pick, place, basket, drive]
    leds go in this order [thinking, wait for input, wrist lasers]
    """
    if(tangible.state == "driving"):
        if(tangible.recieved_msg.button[2] == 1):
            tangible.state = "gather_pick_cloud"

    #TODO add is pointcloud gathered flag
    if(tangible.state == "gather_pick_cloud"):
        if(tangible.pick_cloud_gathered):
            tangible.state == "pick"
            tangible.pick_cloud_gathered = False

    if(tangible.state == "pick"):
        if(tangible.recieved_msg.button[5] == 1):
            tangible.state = "driving"
        elif(tangible.recieved_msg.button[0] == 1):
            tangible.state = "confirm_object"

    #TODO IMPLEMENT METHOD OF ONLY TAKING IN MESSAGE ONCE, WHETER THAT BE A REST OR SOMETHING ELSE
    if(tangible.state == "confirm_object"):
        if(tangible.recieved_msg.button[0] == 1):
            tangible.state = "confirm_pick"
        elif(tangible.recieved_msg.button[1] == 1):
            state_name = "driving"

    #Not sure how this is working with the grasp sucess detection code
    if(tangible.state == "confirm_pick"):
        if(tangible.recieved_msg[1] == 1):
            tangible.state = "object_held"
        elif(tangible.recieved_msg[1] == 1):
            tangible.state = "driving"

    if(state_name == "object_held"):
        if(tangible.recieved_msg[5] == 1):
            tangible.state = "driving"
        elif(tangible.recieved_msg[3] == 1):
            tangible.state = "gather_place_cloud"
        elif(tangible.recieved_msg[4] == 1):
            tangible.state = "basket"

    #TODO Need complete flag
    if(tangible.state == "basket"):
        if(tangible.basket_complete):
            tangible.state = "driving"
            tangible.basket_complete = False

    #TODO need cloudReady flag
    if(tangible.state == "gather_place_cloud"):
        if(tangible.place_cloud_gathered):
            tangible.state = "place"
            tangible.place_cloud_gathered = False

    if(tangible.state == "place"):
        if(tangible.recieved_msg[0] == 1):
            tangible.state = "place_confirm"

    if(tangible.state == "place_confirm"):
        if(tangible.recieved_msg[0] == 1):
            tangible.state = "placing"
        elif(tangible.recieved_msg[1] == 1):
            tangible.state = "place"

    #TODO Need placed confirm flag
    if(tangible.state == "placing" and tangible.placed_complete):
        tangible.state = "driving"
        tangible.placed_complete = False





def compare_state(tangible):
    """
    Compares current state to desired LED state for the interface
    """
    #Buttons[yes, no, pick, place, basket, drive]
    #Leds
    #1 means solid light on, 2 means that it should be blinking, 0 is off
    #first led is thinking, second is ready for selection
    if(tangible.state == "driving"):
        tangible.button_msg.button = [0, 0, 2, 0, 0, 1]
        tangible.button_msg.leds = [0, 0, 0]

        tangible.scooter.go_to_travel_config()

    elif(tangible.state == "gather_pick_cloud"):
        tangible.button_msg.button = [0, 0, 1, 0, 0, 0]
        tangible.button_msg.leds = [1, 0, 0]



        tangible.scooter.go_to_fold_config()
        tangible.scooter.update_pointcloud()

    elif(tangible.state == "pick"):
        tangible.button_msg.button = [2, 2, 1, 0, 0, 0]
        tangible.button_msg.leds = [0, 1, 1]

        tangible.center = tangible.scooter.wait_for_laser()
        tangible.sample_points = tangible.scooter(tangible.scooter.get_sample_points(tangible.center))

        if tangible.sample_points is None or len(tangible.sample_points) == 0:
            tangible.sample_points = tangible.scooter.get_sample_points(tangible.center)


    elif(tangible.state == "confirm_object"):
        tangible.button_msg.button = [2, 2, 1, 0, 0, 0]
        tangible.button_msg.leds = [0, 0, 0]

    elif(tangible.state == "currently_picking"):
        tangible.grasp  = tangible.scooter.get_reachable_grasps(tangible.sample_points)
        tangible.grasp = tangible.scooter.automatic_grasp_selection(tangible.grasp, tangible.sample_points, tangible.center)
        tangible.scooter.pick_object(tangible.grasp)


    elif(tangible.state == "confirm_pick"):
        tangible.button_msg.button = [2, 2, 0, 0, 0, 0]
        tangible.button_msg.leds = [0, 0, 0]


    elif(tangible.state == "object_held"):
        tangible.button_msg.button = [0, 0, 0, 2, 2, 1]
        tangible.button_msg.leds = [0, 0, 0]


    elif(tangible.state == "gather_place_cloud"):
        tangible.button_msg.button = [0, 0, 0, 1, 0, 0]
        tangible.button_msg.leds = [1, 0, 0]


    elif(tangible.state == "place"):
        tangible.button_msg.button = [2, 2, 0, 1, 0, 0]
        tangible.button_msg.leds = [0, 1, 1]


    elif(tangible.state == "place_confirm"):
        tangible.button_msg.button = [2, 2, 0, 1, 0, 0]
        tangible.button_msg.leds = [0, 0, 0]


    elif(tangible.state == "basket"):
        tangible.button_msg.button = [0, 0, 0, 0, 1, 0]
        tangible.button_msg.leds = [0, 0, 0]


    elif(tangible.state == "placing"):
        tangible.button_msg.button = [1, 0, 0, 1, 0, 0]
        tangible.button_msg.leds = [0, 0, 1]


