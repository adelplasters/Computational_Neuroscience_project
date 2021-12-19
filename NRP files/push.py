@nrp.MapRobotPublisher("shoulder_rot", Topic('/arm_robot_0/arm_1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("shoulder_flex", Topic('/arm_robot_0/arm_2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("elbow_flex", Topic('/arm_robot_0/arm_3_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("wrist_flex", Topic('/arm_robot_0/arm_5_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber("command", Topic('/arm_robot_0/commands', std_msgs.msg.String))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.Neuron2Robot()
def go (t,shoulder_rot,shoulder_flex,elbow_flex, wrist_flex,last_command_executed,command):
    if command.value is None:
        return
    else:
        command_str = command.value.data
    if command_str == last_command_executed.value:
        return
    if command_str == "PUSH":
        shoulder_rot.send_message(std_msgs.msg.Float64(0.5))
        shoulder_flex.send_message(std_msgs.msg.Float64(-0.8))
        elbow_flex.send_message(std_msgs.msg.Float64(1.4))
        wrist_flex.send_message(std_msgs.msg.Float64(-0.4))
    last_command_executed.value = command_str