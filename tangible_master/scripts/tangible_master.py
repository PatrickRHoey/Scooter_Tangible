#!usr/bin/env python

import rospy
from tangible_master.msg import button_leds

def talker():
    """
    ROS publisher node, used to communicate with the tangible interface
    via /button_led
    """

    pub = rospy.Publisher('button_led', button_leds, queue_size=10)

    rospy.init_node('tangible_talker', anonymous=True)

    rate = rospy.Rate(10)   #10 hz

    msg = button_leds()

    msg.button_led = [0, 0, 0, 0, 0, 0]

    while not rospy.is_shutdown():
        print("It's Working\n")
        print(msg)
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep


if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

