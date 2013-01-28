from playdoh import *
import numpy as np

class PiMonteCarlo(ParallelTask): # This class derives from the ParallelTask
    def initialize(self, n):
        # Specifies the samples number on this node
        self.n = n
    
    def start(self):
        # Draw n points uniformly in [0,1]^2
        samples = np.random.rand(2,self.n)
        # Counts the number of points inside the quarter unit circle
        self.count = np.sum(samples[0,:]**2+samples[1,:]**2<1)
    
    def get_result(self):
        # Returns the result
        return self.count
    
def pi_montecarlo(samples, nodes):
    # Calculates the number of samples for each node
    split_samples = [samples/nodes]*nodes
    # Launches the task on the local CPUs
    task = start_task(PiMonteCarlo, # name of the task class
                      cpu = nodes, # use <nodes> CPUs on the local machine
                      args=(split_samples,)) # arguments of MonteCarlo.initialize as a list, 
                                             # node #i receives split_samples[i] as argument
    # Retrieves the result, as a list with one element returned by MonteCarlo.get_result per node
    result = task.get_result()
    # Returns the estimation of Pi
    return sum(result)*4.0/samples

if __name__ == '__main__':
    # Evaluates Pi with 10,000 samples and 2 CPUs
    print pi_montecarlo(1000000, 2)
