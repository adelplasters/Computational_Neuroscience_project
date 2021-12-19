@nrp.MapRobotPublisher("hand_index_distal", Topic('/arm_robot_0/hand_j14/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_index_medial", Topic('/arm_robot_0/hand_Index_Finger_Distal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_index_proximal", Topic('/arm_robot_0/hand_Index_Finger_Proximal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_distal", Topic('/arm_robot_0/hand_j15/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_medial", Topic('/arm_robot_0/hand_Middle_Finger_Distal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_proximal", Topic('/arm_robot_0/hand_Middle_Finger_Proximal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_distal", Topic('/arm_robot_0/hand_j17/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_medial", Topic('/arm_robot_0/hand_j13/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_proximal", Topic('/arm_robot_0/hand_Pinky/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_distal", Topic('/arm_robot_0/hand_j16/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_medial", Topic('/arm_robot_0/hand_j12/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_proximal", Topic('/arm_robot_0/hand_Ring_Finger/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_opposition", Topic('/arm_robot_0/hand_Thumb_Opposition/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_distal", Topic('/arm_robot_0/hand_j4/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_medial", Topic('/arm_robot_0/hand_j3/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_proximal", Topic('/arm_robot_0/hand_Thumb_Flexion/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_palm", Topic('/arm_robot_0/hand_j5/cmd_pos', std_msgs.msg.Float64))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.MapRobotSubscriber("command", Topic('/arm_robot_0/commands', std_msgs.msg.String))
@nrp.Neuron2Robot()
def close_hand (t,hand_index_distal,hand_index_medial,hand_index_proximal,hand_middle_distal,hand_middle_medial,hand_middle_proximal,hand_pinky_distal,hand_pinky_medial,hand_pinky_proximal,hand_ring_distal,hand_ring_medial,hand_ring_proximal,hand_thumb_opposition,hand_thumb_distal,hand_thumb_medial,hand_thumb_proximal,hand_palm,command,last_command_executed):
    if command.value is None:
        return
    else:
        command_str = command.value.data
    if command_str == last_command_executed.value:
        return
    if command_str == "CLOSE_HAND":
        hand_index_distal.send_message(std_msgs.msg.Float64(0.2))
        hand_index_medial.send_message(std_msgs.msg.Float64(0.2))
        #hand_index_proximal.send_message(std_msgs.msg.Float64(0.4))
        hand_middle_distal.send_message(std_msgs.msg.Float64(0.2))
        hand_middle_medial.send_message(std_msgs.msg.Float64(0.2))
        #hand_middle_proximal.send_message(std_msgs.msg.Float64(0.4))
        hand_pinky_distal.send_message(std_msgs.msg.Float64(0.2))
        hand_pinky_medial.send_message(std_msgs.msg.Float64(0.2))
        #hand_pinky_proximal.send_message(std_msgs.msg.Float64(0.4))
        hand_ring_distal.send_message(std_msgs.msg.Float64(0.2))
        hand_ring_medial.send_message(std_msgs.msg.Float64(0.2))
        hand_ring_proximal.send_message(std_msgs.msg.Float64(0.2))
        hand_thumb_opposition.send_message(std_msgs.msg.Float64(0.9))
        hand_thumb_distal.send_message(std_msgs.msg.Float64(0.2))
        hand_thumb_medial.send_message(std_msgs.msg.Float64(0.2))
        #hand_thumb_proximal.send_message(std_msgs.msg.Float64(0.4))
        hand_palm.send_message(std_msgs.msg.Float64(0.0))
    last_command_executed.value = command_str