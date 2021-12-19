@nrp.MapRobotPublisher("shoulder_rot", Topic('/arm_robot_0/arm_1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("shoulder_flex", Topic('/arm_robot_0/arm_2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("elbow_flex", Topic('/arm_robot_0/arm_3_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("elbow_rot", Topic('/arm_robot_0/arm_4_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("wrist_flex", Topic('/arm_robot_0/arm_5_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("wrist_rot", Topic('/arm_robot_0/arm_6_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.MapRobotSubscriber("command", Topic('/arm_robot_0/commands', std_msgs.msg.String))
@nrp.Neuron2Robot()
def down (t, shoulder_rot,shoulder_flex, elbow_flex, elbow_rot,wrist_flex,wrist_rot,last_command_executed,command):
    if command.value is None:
        return
    else:
        command_str = command.value.data
    if command_str == last_command_executed.value:
        return
    if command_str == "DOWN":
        wrist_rot.send_message(std_msgs.msg.Float64(3.01))
        shoulder_rot.send_message(std_msgs.msg.Float64(-0.4))
        shoulder_flex.send_message(std_msgs.msg.Float64(-0.6))
        elbow_flex.send_message(std_msgs.msg.Float64(1.6))
        wrist_flex.send_message(std_msgs.msg.Float64(0.0))
        shoulder_rot.send_message(std_msgs.msg.Float64(-0.2))
    last_command_executed.value = command_str