@nrp.MapRobotSubscriber("camera", Topic('/arm_robot/camera', sensor_msgs.msg.Image))
@nrp.MapSpikeSource("red_right_eye", nrp.brain.input_A, nrp.poisson)
@nrp.MapSpikeSource("red_left_eye", nrp.brain.input_B, nrp.poisson)
@nrp.MapSpikeSource("inhibition", nrp.brain.input_in, nrp.poisson)
@nrp.Robot2Neuron()
def check_circle (t, camera,red_left_eye,red_right_eye,inhibition):
    width = 320
    height = 240    
    half_width = int(width / 2)
    width = int(width)
    n = int(half_width * height)
    image_results = hbp_nrp_cle.tf_framework.tf_lib.get_color_values(image=camera.value,width=width,height=height)
    red_value_right = image_results.right_red
    red_value_left = image_results.left_red
    red_sum_right = red_value_right[0]
    red_sum_left = red_value_left[0]
    for i in range(1, n-1):
        red_sum_right = red_sum_right + red_value_right[i]
        red_sum_left = red_sum_left + red_value_left[i]
    clientLogger.info(red_sum_right)
    clientLogger.info(red_sum_left)
    if red_sum_right > 1700:
        red_left_eye.rate = 265.
    else:
        red_left_eye.rate = 0.
    if red_sum_left > 1700:
        red_right_eye.rate = 265.
    else:
        red_right_eye.rate = 0.