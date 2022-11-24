# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 11:06:02 2022

@author: alexp
Deprecated code that was used at one point but removed for ease of use

"""
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')
df= pd.DataFrame()
for k,v in total_invas.items():
    #for dataframe in interval:
    df[k] = v[0]['mean']
df_coord = df.join(pd.DataFrame.from_dict(dict_pos,orient ='index')).rename(columns = {0:'lat', 1:'long'})
from datetime import datetime
filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+'_Mean_invasion_probability_per_year'
df_coord.to_csv(filename)

df2 = pd.DataFrame()
for k,v in total_invas.items():
    #for dataframe in interval:
    df2[k] = v[1]['mean']
df_coord = df2.join(pd.DataFrame.from_dict(dict_pos,orient ='index')).rename(columns = {0:'lat', 1:'long'})

filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+'_Mean_invasion_year'
df_coord.to_csv(filename)
#save data to CSV file using the following format Sim_YYYY_MM_DD_####(number of simulations)


filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)
invas_time.to_csv(filename)

print(time.process_time() - start)
