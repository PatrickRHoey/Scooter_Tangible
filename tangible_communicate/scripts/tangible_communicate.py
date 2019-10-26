#!usr/bin/env python

import rospy
import state_control
from tangible_master.msg import button_leds
from ur_scooter import simple_ui

recieved_msg = button_leds()

def callback(data):
    #Sets current button status to the one being published by the arduino
    #recieved_msg.button = data.button
    #recieved_msg.leds = data.leds
    global recieved_msg
    recieved_msg = data

def talker():
    """
    ROS publisher/subscriber node, used to communicate with the tangible interface
    via /button_led and /tangible_buttons
    """

    rospy.init_node('tangible_talker', anonymous=True)
    rate = rospy.Rate(100)   #10 hz

    #Pub
    pub = rospy.Publisher('button_leds', button_leds, queue_size=10)

    #Sub
    rospy.Subscriber("tangible_interface_send", button_leds, callback)

    msg = button_leds()
    msg.button = [0, 0, 0, 0, 0, 0]

    state = "driving"

    while not rospy.is_shutdown():
        #TODO figure out what i named the serial pub and subscribe here
        #Sets current state according to the array the buttons are publishing
        state = state_control.set_state(state, recieved_msg)
        #Compares state to required Led pattern and sets msg in accordance
        msg = state_control.compare_state(state, msg)

        print("tangible state name is " + state + '\n')
        print("tangible send message is " + str(msg) + '\n')

        #rospy.loginfo(msg)
        pub.publish(msg)
        #rate.sleep
        rospy.sleep(1)


if __name__ == "__main__":
	try:
		talker()

	except rospy.ROSInterruptException:
		pass
