from __future__ import division
# pragma: no cover

import nest
import logging
import numpy
from hbp_nrp_cle.brainsim import simulator as sim
from hbp_nrp_excontrol.logs import clientLogger
import pyNN

__author__ = 'Alessandra Trapani, Francesco Sheiban'

logger = logging.getLogger(__name__)

# Helper functions to automatically tune the network weights so to have near-threshold dynamics
def LambertWm1(x):
    return nest.ll_api.sli_func('LambertWm1', float(x))

def ComputePSPNorm(tau_mem, C_mem, tau_syn, is_NMDA=False):
    a = (tau_mem / tau_syn)
    if is_NMDA:
        a *= 5.02
    b = (1.0 / tau_syn -1.0 / tau_mem)
    t_max = 1.0 / b * (-LambertWm1(-numpy.exp(-1.0/a)/a) - 1.0 / a)
    return (numpy.exp(1.0) / (tau_syn * (C_mem * b) * 
            ((numpy.exp( -t_max / tau_mem) - numpy.exp(-t_max / tau_syn)) / b - 
            t_max * numpy.exp(-t_max / tau_syn))))


# --------------------------------
# Main function: 
# Returns the spiking circuit to be connected to the robotic agent
# --------------------------------
def create_brain():
    #dt = 0.1    # the resolution in ms
    simtime = 1000.0  # Simulation time in ms
    delay = 5.    # Synaptic delay in ms
    delay_GABA = 0.3
    delay_NMDA = 15.
    delay_AMPA = 20.
    eta = 0.93  # External rate relative to threshold rate
    epsilon = 0.18  # Connection probability between populations
    epsilon_poptopop = 0.01 
    epsilon_poptoin = 0.25
    epsilon_intoin = 0.1
    epsilon_intopop = 0.25 

    order = 50 
    NA = 2 * order  # Number of excitatory neurons in pop A
    NB = 2 * order  # Number of excitatory neurons in pop A
    NI = 1 * order  # Number of inhibitory neurons
    N_neurons = NA + NB + NI   # Number of neurons in total

    CE = int(epsilon_poptopop * NA + epsilon * NB)  # Number of excitatory synapses per neuron 
    CI = int(epsilon_intopop * NI)  # Number of inhibitory synapses per neuron
    C_tot = int(CI + CE)      # Total number of synapses per neuron

    nr_ports = 4  # Number of receptor types (noise-related, AMPA, NMDA, GABA)
    tau_syn = [13., 2., 100., 2.0]  # Exponential time constant of post-synaptic current (PSC) for each receptor [ms]

    # Population-independent constants
    V_membrane = -70.0  # [mV] 
    V_threshold = -50.0  # [mV]
    V_reset = -55.0  # [mV]

    # Population-dependent constants
    # Excitatory
    C_m_ex = 500.0  # [pF]  
    # Inhibitory
    C_m_in = 200.0  # [pF]
    # Excitatory
    t_ref_ex = 2.0 
    # Inhibitory
    t_ref_in = 1.0
    # Excitatory
    tau_m_ex = 20.0
    # Inhibitory
    tau_m_in = 10.0

    # Storing the neurons' parameters in a dictionary to be assigned to the models later
    # Excitatory
    exc_neuron_params = {
        "E_L": V_membrane,
        "V_th": V_threshold,
        "V_reset": V_reset,
        "C_m": C_m_ex,  
        "tau_m": tau_m_ex,
        "t_ref": t_ref_ex, 
        "tau_syn": tau_syn
    }
    # Inhibitory 
    inh_neuron_params = {
        "E_L": V_membrane,
        "V_th": V_threshold,
        "V_reset": V_reset,
        "C_m": C_m_in, 
        "tau_m": tau_m_in,
        "t_ref": t_ref_in,
        "tau_syn": tau_syn 
    } 

    # Automatic weight tuning 
    J = 0.6  # Post-synaptic potential (PSP) induced by a single spike  [mV]  
    # Noise weights
    J_unit_noise = ComputePSPNorm(tau_m_ex, C_m_ex, tau_syn[0])
    J_norm_noise = J / J_unit_noise 
    # AMPA weights
    J_unit_AMPA = ComputePSPNorm(tau_m_ex, C_m_ex, tau_syn[1])
    J_norm_AMPA = J / J_unit_AMPA 
    # NMDA weights
    J_unit_NMDA = ComputePSPNorm(tau_m_ex, C_m_ex, tau_syn[2], is_NMDA=True)
    J_norm_NMDA = J / J_unit_NMDA 
    # GABA weights
    J_unit_GABA = ComputePSPNorm(tau_m_in, C_m_in, tau_syn[3])
    J_norm_GABA = J / J_unit_GABA

    #--------------------------------
    # Creating the nodes
    # --------------------------------
    # Defining the populations models and creating the nodes
    inputs = nest.Create("parrot_neuron", 3)  # Parrot neurons to transmit the inputs to the network, only act as separate buffers (one for each pop)   
    population = nest.Create("iaf_psc_exp_multisynapse", N_neurons)  # Instantiating a general (parameter-less) neuronal population (of current-based I&F) to model all the neurons
    nest.SetStatus(population[0: 4 * order - 1], exc_neuron_params)  # Defining the excitatory subpopulation numerosity and parameters
    nest.SetStatus(population[4 * order : (4 * order) + 1 * order - 1], inh_neuron_params)  # Defining the inhibitory subpopulation numerosity and parameters

    # Defining the quantities to be used in the connectivity instructions
    # Subpopulation A and relative input  
    pop_A = population[0:(order * 2 -1)]  
    input_A = inputs[0:1]
    # Subpopulation B and relative input  
    pop_B = population[(order * 2) : order * 4 -1]
    input_B = inputs[1:2]
    # Subpopulation C and relative input  
    pop_inh = population[(order * 4) : (order * 5 -1)]
    input_inh = inputs[2:3]
    
    nu_th_noise_ex = (numpy.abs(V_threshold) * 500.0) / (J_norm_noise * CE * numpy.exp(1) * 20.0 * tau_syn[0])
    nu_ex = eta * nu_th_noise_ex
    p_rate_ex = 1000.0 * nu_ex * CE

    nu_th_noise_in = (numpy.abs(V_threshold) * 200.0) / (J_norm_noise * CI * numpy.exp(1) * 10.0 * tau_syn[0])
    nu_in = eta * nu_th_noise_in
    p_rate_in = 1000.0 * nu_in * CI
    
    nest.SetDefaults("poisson_generator", {"rate": p_rate_ex})
    PG_noise_ex = nest.Create("poisson_generator")

    nest.SetDefaults("poisson_generator", {"rate": p_rate_in})
    PG_noise_in = nest.Create("poisson_generator")

    # Defining the synaptic connections names, parameters and receptor type to be used later
    nest.CopyModel("static_synapse", "excitatory_AMPA",
               {"weight": J_norm_AMPA, "delay": delay_AMPA})
    nest.CopyModel("static_synapse", "excitatory_NMDA",
                {"weight": J_norm_NMDA, "delay": delay_NMDA})
    nest.CopyModel("static_synapse", "noise_syn",
                {"weight": J_norm_noise, "delay": delay})
    nest.CopyModel("static_synapse", "inhibitory",
                {"weight": -J_norm_GABA, "delay": delay_GABA})
    noise_syn = {"model": "noise_syn",
                 "receptor_type": 1}
    AMPA_syn = {"model": "excitatory_AMPA",
                    "receptor_type": 2}
    NMDA_syn = {"model": "excitatory_NMDA",
                    "receptor_type": 3}
    GABA_syn = {"model": "inhibitory",
                    "receptor_type": 4}

    #--------------------------------
    # Connecting the nodes
    # -------------------------------
    # Population A
    # Defining the connectivty strategy to be used
    conn_params_ex_auto = {'rule': 'pairwise_bernoulli', 'p': epsilon}
    conn_params_ex_poptopop = {'rule': 'pairwise_bernoulli', 'p': epsilon_poptopop}
    conn_params_ex_poptoin = {'rule': 'pairwise_bernoulli', 'p': epsilon_poptoin}
    # Connecting the components
    # Input
    #nest.Connect(input_A, pop_A, 'all_to_all', {"receptor_type": 1})
    nest.Connect(input_A, pop_A, syn_spec=noise_syn)
    # Recurrent
    nest.Connect(pop_A, pop_A, conn_params_ex_auto, AMPA_syn)
    nest.Connect(pop_A, pop_A, conn_params_ex_auto, NMDA_syn)
    # To pop B
    nest.Connect(pop_A, pop_B, conn_params_ex_poptopop, AMPA_syn)
    nest.Connect(pop_A, pop_B, conn_params_ex_poptopop, NMDA_syn)
    # To pop inh.
    nest.Connect(pop_A, pop_inh, conn_params_ex_poptoin, AMPA_syn)
    nest.Connect(pop_A, pop_inh, conn_params_ex_poptoin, NMDA_syn)

    # Population B
    # Input
    nest.Connect(input_B, pop_B, syn_spec=noise_syn)
    #nest.Connect(input_B, pop_B, 'all_to_all', {"receptor_type": 1})
    # Recurrent
    nest.Connect(pop_B, pop_B, conn_params_ex_auto, AMPA_syn)
    nest.Connect(pop_B, pop_B, conn_params_ex_auto, NMDA_syn)
    # To pop A
    nest.Connect(pop_B, pop_A, conn_params_ex_poptopop, AMPA_syn)
    nest.Connect(pop_B, pop_A, conn_params_ex_poptopop, NMDA_syn)
    # To pop inh.
    nest.Connect(pop_B, pop_inh, conn_params_ex_poptoin, AMPA_syn)
    nest.Connect(pop_B, pop_inh, conn_params_ex_poptoin, NMDA_syn)

    # Population inh 
    # Defining the connectivty strategy to be used
    conn_params_in_intoin = {'rule': 'pairwise_bernoulli', 'p': epsilon_intoin}
    conn_params_in_intopop = {'rule': 'pairwise_bernoulli', 'p': epsilon_intopop}
    # Input
    #nest.Connect(input_inh, pop_inh,'all_to_all', {"receptor_type": 1})
    nest.Connect(input_inh, pop_inh, syn_spec=noise_syn)
    # Recurrent
    nest.Connect(pop_inh, pop_inh, conn_params_in_intoin, GABA_syn)
    # To pop A
    nest.Connect(pop_inh, pop_A, conn_params_in_intopop, GABA_syn)
    # To pop B
    nest.Connect(pop_inh, pop_B, conn_params_in_intopop, GABA_syn)
    
    nest.Connect(PG_noise_ex, pop_A, syn_spec=noise_syn)
    nest.Connect(PG_noise_ex, pop_B, syn_spec=noise_syn)
    nest.Connect(PG_noise_in, pop_inh, syn_spec=noise_syn)
    
    #--------------------------------
    # End of function
    # -------------------------------
    # Finally, return the network composed by the sum of the two distinct node types (populations), 
    # the "input cells" and neuronal cells
    nodes = inputs + population
    return nodes

circuit = create_brain()