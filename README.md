# Gaps in population data could limit predictive potential of invasive species establishment models: The case of the emerald ash borer

## Overview

This project develops a risk assessment model that simulates emerald ash borer transportation in firewood by campers in the Maritime provinces of Canada.
Using this model we perform local and global sensitivity analyses to measure the importance of introduction and establishment characteristics in our risk analysis model

The goal of this project is to enhance the accuracy of risk assessment models for invasive forest insect establishment by incorportaing underexplored factors such as Allee effects and the timing of intoductions. 

Using a modelling approach to emerald ash borer movement, this project: 
* Simulates the arrival of emerald ash borer to vampgrounds through the movement of firewood
* Performs a sensitivity analysis to investigate the factors that impact establishment

## Project structure

The code is seperated into 3 distinct sections for different stages in model creation and analysis:

### 1. The creation of the edgelist 
    
    Take information from campgrounds and cities in the maritimes and create an edgelist of origin and destinations including city->city and city->campground
    
    * We create two dataframes of city to city and of city to campground (edge between each connection) 
    * The dataframe is then merged into one dataframe containing both city->camp edges and city->camp edges
    
    Script: **1-Create_edgelist.py**

### 2. Addition of the edgelist characteristics
    
    This takes the edgelist and adds distance and travel between origin and destination
    
    Script: **2-Merge_distance_to_edgelist.py**

### 3. The simulation of firewood transportation from origin and destination locations to simulate 
    
    This step simulates firewood transportation from infested cities to susceptible cities or campgrounds to estimate the risk of EAB establishment.
    
    * Use the edgelist to simulate the movement of infested firewood from origins (Edmundston, Halifax, Fredericton, Moncton, and Oromocto) 
    * estimates the number of infested firewood leaving the origin and then distribute them randomly to destinations based on weighted values.
    * extract the probability that emerald ash borer establishes at campgrounds based on data from the simulations into dataframes, the time to the first transportation of firewood,the number of pieces of firewood that see emerald ash borer emergence and the number of emergences required in a single month for populations to establish.
    
    Scripts : 
    
    * **B-simulation.py (contains a simulation class that instructs the steps to do in the simulation)**
    * **3-Creation_of_network_graph_SA-2.py**


### Camping_data
    Data includes raw data and node list and edgelist of campgrounds in the Maritimes 

### City_data
    Data includes all raw data of cities Cen_div_city.csv and raw data for travel between counties from the TSRC
### TRSC
    Movement of between regions of TSRC 
