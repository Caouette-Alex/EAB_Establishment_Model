'''
Simulation class that changes states of campgrounds based on movmeent of firewood from cities to campgrounds 

The example from the Chapter 7 Tutorial was used as a basis from the book Intro Network Science book
        Copyright 2018 Indiana University and Cambridge University Press
'''
#

from collections import Counter
from operator import itemgetter

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


class StopCondition(StopIteration):
    pass

class Simulation:
    '''Simulate state transitions on a network'''
    invasion_step={}

    def __init__(self, G, initial_state, state_transition, name=''):
        '''
        Create a Simulation instance.

        Args:
            G: a networkx.Graph instance.
            initial_state: function with signature `initial_state(G)`, that
                accepts a single argument, the Graph, and returns a dictionary
                of all node states. The keys in this dict should be node names
                and the values the corresponding initial node state.
            state_transition: function with signature
                `state_transition(G, current_state)` that accepts two
                arguments, the Graph and a dictionary of current node states,
                and returns a dictionary of updated node states. The keys in
                this dict should be node names and the values the corresponding
                updated node state.

        Keyword Args:
            name (optional): a string used in titles of plots and drawings.

        Raises:
            ValueError: if not all graph nodes have an initial state.
        '''
        
        #Create a copy of the network graph
        self.G = G.copy()
        
        #Create instance for the initial state of the model and the transitions between states
        self._initial_state = initial_state
        self._state_transition = state_transition
        
        #create instance that lists the current state of each node (Infected or susceptible) 
        self._states = []
        self._value_index = {}
        
        from matplotlib.colors import LinearSegmentedColormap
        #choose the colours for the colour map
        cmap = LinearSegmentedColormap.from_list('my_list',['#d62728','#6e8f6e'] , N=2)
        self._cmap = plt.cm.get_cmap(cmap)
        
        #create dictionaries to represent different outputs of interest
        self._grid_invas = {}
        self._prop_infect = {}
        self._time_invas = {}
        self._prob_invas = {}
        self._prog_pres = {}
        self._propagule_pres = {}
        
        self._inf_camp = []
        
        self._initialize()
        #self._intro_time = pd.DataFrame(index=self.G)
        
        #Get spatial characteristics of the model
        #self._pos = nx.get_node_attributes(G, 'pos')
        #self._grid_id = nx.get_node_attributes(G, 'Grid_ID')
        
    def _append_state(self, state):
        self._states.append(state)
        
        #Update self._value_index
        #for value in set(state.values()):
           #print(value)
           #if value not in self._value_index:
               #self._value_index[value] = len(self._value_index)
        
        
    def _initialize(self):
        if self._initial_state:
            if callable(self._initial_state):
                state = self._initial_state(self.G)
            else:
                state = self._initial_state
            nx.set_node_attributes(self.G, state, 'state')

        if any(self.G.nodes[n].get('state') is None for n in self.G.nodes):
            raise ValueError('All nodes must have an initial state')

        self._append_state(state)


    #iterate through a single year. in this case we go through the class state transition once that's found in the file 3-Creation_of_Network_graph.py
    def _step(self):
    
        # We're choosing to use the node attributes as the indicator of changes in states from susceptible 'S' and infected 'I'
        # We perturb the network in between steps using the state transition class that selects new infested locations based on introcution model 
        
        #state of all the nodes at that step
        state = nx.get_node_attributes(self.G, 'state')
        
        
        state_in_trans = self._state_transition(self.G, state)
        
        #state_in_trans[0] represents a dictionary of campgrounds that are infested
        new_state = state_in_trans[0]
       
        self._inf_camp.append(state_in_trans)
        
        #This creates a dictionary to show what time period each k(node name) changes v(state) to infested 
        #For those that are already infested at step 0(Edmundston, Moncton,Fredericton, Halifax, Oromocto)
        #iterate through all the nodes. If the node becomes infested at this step then record that location as infested and track the time point that it became infested.
        
        #for k, v in state.items():
            #Create a dictionary that represents the propagule pressure of each piece of firewood arriving state_in_trans[1] gives the number of pieces of firewood showing up by campground by month
           # self._prog_pres[len(self._states) - 1] = state_in_trans[1]
            #If state is infected
            #if v == 'I':
                # node name or campground not in time to invasion dictionary add the time period where the location became infested
                #if k not in self._time_invas:
                    #self._time_invas[k] = len(self._states)
                    #Add a binary value to represent if a location becomes invaded
                    #self._prob_invas[k] = 1
        
                
        
        for k, v in new_state.items():
            
            if k not in self._time_invas:
            #Timepoint at which the campground becomes infested.
              self._time_invas[k] = len(self._states)
            # Measures a 1 or 0 if the location becomes infested
              self._prob_invas[k] = 1
            # Print the Grid ID value if the locations becomes established
              self._grid_invas[k] = nx.get_node_attributes(self.G, 'Grid_ID')[k]
        
        
        #update the state of the nodes based on the new state values 
        state.update(new_state)
        nx.set_node_attributes(self.G, state, 'state')
        self._append_state(state)
        
        #Measure the proportion of infested campgrounds based on the total number of campgrounds
        self._prop_infect[len(self._states)-1] = list(state.values()).count('I')

    def _categorical_color(self, value):
        index = self._value_index[value]
        node_color = self._cmap(index)
        return node_color

    @property
    def steps(self):
        ''' Returns the number of steps the sumulation has run '''
        return len(self._states) - 1

    def state(self, step=-1):
        '''
        Get a state of the simulation; by default returns the current state.

        Args:
            step: the step of the simulation to return. Default is -1, the
            current state.

        Returns:
            Dictionary of node states.

        Raises:
            IndexError: if `step` argument is greater than the number of steps.
        '''
        try:
            return self._states[step]
        except IndexError:
            raise IndexError('Simulation step %i out of range' % step)

    def run(self, steps=1):
        '''
        Run the simulation one or more steps, as specified by the `steps`
        argument. Default is to run a single step.

        Args:
            steps: number of steps to advance the simulation.
        '''
        for _ in range(steps):
            try:
                self._step()
            except StopCondition as e:
                print(
                    "Stop condition met at step %i." % self.steps
                    )
                break
    