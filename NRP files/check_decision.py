@nrp.MapSpikeSink("pop_A", nrp.brain.pop_A, nrp.population_rate)
@nrp.MapSpikeSink("pop_B", nrp.brain.pop_B, nrp.population_rate)
@nrp.MapRobotPublisher("decision", Topic('/arm_robot_0/decision', std_msgs.msg.String))
@nrp.MapVariable("index", initial_value=0)
@nrp.Neuron2Robot()
def check_decision (t,pop_A,pop_B,index,decision):
    if pop_A.rate >= pop_B.rate:
        index.value = index.value +1
    elif pop_A.rate < pop_B.rate:
        index.value = 0
    clientLogger.info("indice:",index.value) 
    if index.value > 70:
        decision.send_message(std_msgs.msg.String('YES'))
    else:
        decision.send_message(std_msgs.msg.String('NO'))