import sys

import numpy as np
import rospy
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose, Twist, Point, Vector3, Quaternion
import tf.transformations as tf_t
import csv
import sys

rospy.init_node("move")
# rospy.wait_for_service('add_two_ints')
set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)


csv_file = open(sys.argv[1], "r")
csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')

poses = [[np.array([float(i) for i in row[1:4]]), np.array([float(i) for i in row[4:7]])] for row in csv_reader if len(row) > 2]


poses.append(poses[-1])
hz = 24

# prev = [np.array([0, 0, 0]), np.array([0, 0, 0])]


def orientation_from_quaternion(q):
    return Quaternion(*q)


def orientation_from_euler(r, p, y):
    q = tf_t.quaternion_from_euler(r, p, y)
    return orientation_from_quaternion(q)


for i in range(len(poses)-1):
    now = poses[i]
    nxt = poses[i+1]

    v = (nxt[0] - now[0]) / (1/hz)
    w = (nxt[1] - now[1]) / (1/hz)
    print(v, w)

    # prev = [np.copy(pnt), np.copy(rot)]
    set_model_state(model_state=ModelState(
        model_name="test",
        pose=Pose(
            position=Point(
                x=now[0][0],
                y=now[0][1],
                z=now[0][2]
            ),
            orientation=orientation_from_euler(
                r=now[1][0],
                p=now[1][1],
                y=now[1][2]
            )
        ),
        twist=Twist(
            linear=Vector3(
                x=v[0],
                y=v[1],
                z=v[2]
            ),
            angular=Vector3(
                x=w[0],
                y=w[1],
                z=w[2]
            )
        ),
        reference_frame="world"
    ))
    rospy.sleep(1/hz)


