# Computational_Neuroscience_project

    Authors: Adelaide Stucchi, Corina Sidere, Gabriele Calamai, Gioia D'Andrea, Veronica Fossati
    
***
 <img src="https://github.com/adelplasters/Computational_Neuroscience_project/blob/main/env1.png" width="700">
The aim of the project is to simulate a decision - making protocol based on the experiments described in articles already published.

The task includes a robotic arm which has to decide wether throw a ball in a right net or left one, depending on an external indication. 
The robot is able to take the decision thanks to the neural network, which has the following structure: 

 <img src="https://github.com/adelplasters/Computational_Neuroscience_project/blob/main/net.png" width="500">
 
We start from two excitatory neuronal populations, A and B, with their proper external input stimuli, the populations are able to excite themselves whether their own stimulus is high. The decision making is binary, so just one stimulus at time can be high, the group for which this doesn’t happen is inhibited by a third population, which is composed by inhibitory interneurons. 
 Noise is another typology of external input, it is add in order to create a network coherent with the physiology of the real ones, in fact noise is always present in real neural connections. 
 
Here are shown the raster plots for three different input stimuli: 
* only noise
* only stimulus A
* only stimulus B 

Are also proposed two different codes, one for populations composed by 200 neurons and a second with 50. The codes show some differences in some parameters (epsilon, p_rate) tuning.

 | 200 neurons  | 50 neurons |
| ------------- | ------------- |
|  <img src="https://github.com/adelplasters/Computational_Neuroscience_project/blob/main/ord200.png" width="700">| <img src="https://github.com/adelplasters/Computational_Neuroscience_project/blob/main/ord50.png" width="450"> |
 

 ## NRP platfrom  
 

      
 
   * * *
