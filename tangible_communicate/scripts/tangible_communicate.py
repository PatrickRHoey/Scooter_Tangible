#!usr/bin/env python

import rospy
from tangible_master.msg import button_leds
import state_control

recieved_msg = []

def callback(data):
    #Sets current button status to the one being published by the arduino
    recieved_msg = data

def talker():
    """
    ROS publisher/subscriber node, used to communicate with the tangible interface
    via /button_led and /tangible_buttons
    """

    rospy.init_node('tangible_talker', anonymous=True)
    rate = rospy.Rate(10)   #10 hz

    #Pub
    pub = rospy.Publisher('button_leds', button_leds, queue_size=10)

    #Sub
    rospy.Subscriber("tangible_buttons", button_leds, callback)

    msg = button_leds()
    msg.button = [0, 0, 0, 0, 0, 0]

    state = "driving"

    while not rospy.is_shutdown():
        #TODO figure out what i named the serial pub and subscribe here
        #Sets current state according to the array the buttons are publishing
        set_state(state, recieved_msg)
        #Compares state to required Led pattern and sets msg in accordance
        compare_state(state, msg)


        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep


if __name__ == "__main__":
	try:
		talker()

	except rospy.ROSInterruptException:
		pass
