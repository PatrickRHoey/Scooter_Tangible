#!usr/bin/env python

import rospy
import state_control
from tangible_master.msg import button_leds
import simple_ui

class Tangible():
    def __init__(self):
        self.scooter = simple_ui.Scooter()
        self.grasp = None
        self.sample_points = None
        self.center = None


        self.state = "driving"

        self.recieved_msg = button_leds()
        self.send_msg = button_leds()

        self.pickCloudGathered = False
        self.basket_complete = False
        self.placed_complete = False

        #Michaels stuff dont know if i need ?
        self.basket = False
        self.place = False
        self.getPCH = False
        self.backLaser = False




    def callback(self, data):
        #Sets current button status to the one being published by the arduino
        self.recieved_msg.button = data

    def talker(self):
        """
        ROS publisher/subscriber node, used to communicate with the tangible interface
        via /button_led and /tangible_buttons
        """

        rospy.init_node('tangible_talker', anonymous=True)

        #Pub
        pub = rospy.Publisher('button_leds', button_leds, queue_size=10)

        #Sub
        rospy.Subscriber("tangible_buttons", button_leds, self.callback)

        self.send_msg.button = [0, 0, 0, 0, 0, 0]


        while not rospy.is_shutdown():
            #TODO figure out what i named the serial pub and subscribe here
            #Sets current state according to the array the buttons are publishing
            self.state_control.set_state(self)
            #Compares state to required Led pattern and sets msg in accordance
            state_control.compare_state(self)


            rospy.loginfo(self.send_msg)
            pub.publish(self.send_msg)
            rospy.sleep(1)


if __name__ == "__main__":
    try:
        tangible = Tangible()
        tangible.talker()

    except rospy.ROSInterruptException:
        pass


