'''
Simulation class for Chapter 7 Tutorial of Intro Network Science book

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
        self._initial_state = initial_state
        self._state_transition = state_transition
        self.name = name or 'Simulation'
        self._states = []
        self._value_index = {}
        from matplotlib.colors import LinearSegmentedColormap
        #choose the colours for the colour map
        cmap = LinearSegmentedColormap.from_list('my_list',['#d62728','#6e8f6e'] , N=2)
        self._cmap = plt.cm.get_cmap(cmap)
        
        self._grid_invas = {}
        self._prop_infect = {}
        self._time_invas = {}
        self._prob_invas = {}
        self._prog_pres = {}
        self._propagule_pres = {}
        self._test = []
        self._initialize()
        #self._intro_time = pd.DataFrame(index=self.G)

        self._pos = nx.get_node_attributes(G, 'pos')
        self._grid_id = nx.get_node_attributes(G, 'Grid_ID')
        
    def _append_state(self, state):
        self._states.append(state)
        # Update self._value_index
        for value in set(state.values()):
            if value not in self._value_index:
                self._value_index[value] = len(self._value_index)

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

    def _step(self):
    
        # We're choosing to use the node attributes as the source of truth.
        # This allows the user to manually perturb the network in between steps.
        state = nx.get_node_attributes(self.G, 'state')
        
        state_in_trans = self._state_transition(self.G, state)
        #state_in_trans[0] represents a dictionary of campgrounds that are infested
        new_state = state_in_trans[0]
        self._test.append(state_in_trans)
        
        

                
        
        #This creates a dictionary to show what time period each k(node name) changes v(state) to infested 
        #For those that are already infested at step 0(Edmundston, Moncton,Fredericton, Halifax, Oromocto)
        for k, v in state.items():
            #Create a dictionary that represents the propagule pressure of each piece of firewood arriving state_in_trans[1] gives the number of pieces of firewood showing up by campground by month
            self._prog_pres[len(self._states) - 1] = state_in_trans[1]
            if v == 'I':
                if k not in self._time_invas:
                    self._time_invas[k] = len(self._states)
                    self._prob_invas[k] = 1
                    
        for k, v in new_state.items():
            if k not in self._time_invas:
              self._time_invas[k] = len(self._states)
              self._prob_invas[k] = 1
              self._grid_invas[k] = nx.get_node_attributes(self.G, 'Grid_ID')[k]
        
        state.update(new_state)
        nx.set_node_attributes(self.G, state, 'state')
        self._append_state(state)
        
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

    def draw(self, step=-1, labels=None, **kwargs):
        '''
        Use networkx.draw to draw a simulation state with nodes colored by
        their state value. By default, draws the current state.

        Args:
            step: the step of the simulation to draw. Default is -1, the
            current state.
            kwargs: keyword arguments are passed to networkx.draw()

        Raises:
            IndexError: if `step` argument is greater than the number of steps.
        '''
        from mpl_toolkits.basemap import Basemap
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection
        import numpy as np
        import os
        
        os.chdir('\..')
        os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding')
        
        city_nodes = [n
            for (n, ty) in \
                nx.get_node_attributes(self.G, 'Type').items() if ty == 'city_to_city']
        #for changing shapes of citys and campgrounds
        camp_nodes = [n  
            for (n, ty) in \
                nx.get_node_attributes(self.G, 'Type').items() if ty == 'city_to_camp']
        
        #TODO add written descriptions of these 
        plt.rcParams['figure.dpi'] = 300
        fig     = plt.figure()
        ax      = fig.add_subplot(111)
        
    
        #Create the outer edges of the image
        map = Basemap(llcrnrlon=-68.6,llcrnrlat=43.42,urcrnrlon=-59.68,urcrnrlat=48.07,resolution='l', ellps='WGS84',lat_0=-64.37, lon_0=45.73)
        # Get shapegfile data and colour it by provincs
        map.readshapefile("maritime_prov1", "states")
        patches   = []
        
        for info, shape in zip(map.states_info, map.states):
            if info['Name_EN'] == 'New Brunswick' or 'Nova Scotia' or 'Prince Edward Island' :
                patches.append( Polygon(np.array(shape), True) )
        ax.add_collection(PatchCollection(patches, facecolor= 'thistle', edgecolor='k', linewidths=1., zorder=0))
        
         # add other boundaries and colour in water as blue and other states as grey
        map.drawmapboundary(fill_color='paleturquoise',zorder=-2)
        map.drawstates(linewidth=0.2)
        map.fillcontinents(color='gray',zorder=-1)
        map.drawcoastlines()   
    
        state = self.state(step)
      #
        node_colors = [self._categorical_color(state[n]) for n in self.G.nodes]
        #nx.draw(self.G, pos=nx.get_node_attributes(self.G, 'pos'), node_color=node_colors, node_size=8, width=0.05, **kwargs)
        
        nx.draw_networkx_nodes(self.G, pos=nx.get_node_attributes(self.G, 'pos'), node_shape = 'o', node_size=10 ,node_color=node_colors)
        #nx.draw_networkx_nodes(self.G, pos=nx.get_node_attributes(self.G, 'pos'), nodelist = camp_nodes, node_shape = 'o', node_size=8,node_color=node_colors)
        if labels is None:
            labels = sorted(set(state.values()), key=self._value_index.get)
        patches = [mpl.patches.Patch(color=self._categorical_color(l), label=l)
                   for l in labels]
        plt.legend(handles=patches)

        if step == -1:
            step = self.steps
        if step == 0:
            title = 'initial state'
        else:
            title = 'year %i' % (step)
        if self.name:
            title = '{}: {}'.format(self.name, title)
        plt.title(title)
        
        plt.show()
        return fig
    def animate(self, step= -1,**kwargs):
        '''
        Create a short animation that shows the invasion of a locaiton over one iteration
        '''

        from matplotlib import pyplot as plt, animation
        state = self.state(step)
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig = plt.figure()
        
        node_colors = [self._categorical_color(state[n]) for n in self.G.nodes]
        nx.draw(self.G, pos=nx.get_node_attributes(self.G, 'pos'), node_color=node_colors, node_size=8, width=0.05, **kwargs)
        def animate(frame):
           fig.clear()
           nx.draw(self.G, with_labels=True)
        
        ani = animation.FuncAnimation(fig, animate, frames=len(self._states) - 1, interval=1000, repeat=True)

        plt.show()

        
    def plot(self, min_step=None, max_step=None, labels=None, **kwargs):
        '''
        Use pyplot to plot the relative number of nodes with each state at each
        simulation step. By default, plots all simulation steps.

        Args:
            min_step: the first step of the simulation to draw. Default is
                None, which plots starting from the initial state.
            max_step: the last step, not inclusive, of the simulation to draw.
                Default is None, which plots up to the current step.
            labels: ordered sequence of state values to plot. Default is all
                observed state values, approximately ordered by appearance.
            kwargs: keyword arguments are passed along to plt.plot()

        Returns:
            Axes object for the current plot
        '''
        import numpy as np
        x_range = range(min_step or 0, max_step or len(self._states))
        counts = [Counter(s.values()) for s in self._states[min_step:max_step]]
        if labels is None:
            labels = {k for count in counts for k in count}
            labels = sorted(labels, key=self._value_index.get)
        
        plt.figure(figsize=(15,10))
        
        for label in labels:
            series = [count.get(label, 0) / sum(count.values()) for count in counts]
            plt.plot(x_range, series, label=label, **kwargs)
    
        
        title = 'node state proportions'
        if self.name:
            title = '{}: {}'.format(self.name, title)
        plt.title(title)
        plt.xlabel('Simulation step')
        plt.xticks(np.arange(min(x_range), max(x_range)+1, 1.0))
        plt.ylabel('Proportion of nodes')
        plt.legend()
        plt.xlim(x_range.start)

        return plt.gca()

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
    def test(self):
        #print(self._test)
        state = nx.get_node_attributes(self.G, 'state')
        print(self._state_transition(self.G, state))