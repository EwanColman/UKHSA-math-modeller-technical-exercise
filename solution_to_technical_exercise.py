# -*- coding: utf-8 -*-
"""
Code for UKSHA interview
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np
import pandas as pd
import smallestenclosingcircle
#### Put you code here #####

# read in the data
cases_df=pd.read_csv('Data/2023-10-15_Modelling_test_case_locations_v1.0.csv')
pop_df=pd.read_csv('Data/2023-10-15_Modelling_test_population_v1.0.csv')

# get case coordinates as lists
# rescale to be same as pop grid
x_coords=[x/100 for x in cases_df['X'].tolist()]
y_coords=[y/100 for y in cases_df['Y'].tolist()]


# m will be the matrix
M=[]
# read and convert to matrix
for i,row in pop_df.iterrows():
    M.append(row.tolist())

M=np.array(M)
#M=np.transpose(M)

x_max=M.shape[1]
y_max=M.shape[0]


#### plotting ####
fs=12
fig=plt.figure(figsize=(10,10))
ax = fig.add_subplot()

#tick values
x_vals=range(0,x_max,10)
y_vals=range(0,y_max,10)

print(x_vals,y_vals)

plt.xticks(x_vals,[i*100 for i in x_vals],size=fs,rotation=60)
plt.yticks(y_vals,[i*100 for i in y_vals],size=fs)
#ax.xaxis.tick_top()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.imshow(M,cmap='Greys',origin='lower') # displays in color



plt.xlabel('X',size=fs)
plt.ylabel('Y',size=fs,rotation=0)

#plot the cases
plt.scatter(x_coords,y_coords)  


########### ALGORITHM #################
#You may assume that the pathogen has spread no further than the furthest
#  cases, and that it spreads evenly in all directions – i.e. forms a 
# circle. You may wish to consider this part of the test as an example of 
# the minimum bounding circle problem.

# Algorithm to use: 
    
points=zip(x_coords,y_coords)    

center_x, center_y, radius = smallestenclosingcircle.make_circle(points)

print(center_x, center_y,radius)
circle=patch.Circle((center_x, center_y),radius=radius,color='b',alpha=0.1)
ax.add_patch(circle)

# When you have determined the extent of the spread, you will then need 
# to count the population affected.

# keep running total of population
total_population_affected=0
cells_affected=0

# loop over a rectangle that covers the circle
for x in range(int(np.floor(center_x-radius)),int(np.ceil(center_x+radius))):
    for y in range(int(np.floor(center_y-radius)),int(np.ceil(center_y+radius))):
        # is it in the circle?
        # disance to the centre
        d=(((x+0.5-center_x)**2)+((y+0.5-center_y)**2))**(1/2)
        # if its closer than the radius then add the population
        
        if d<radius:
            
            total_population_affected=total_population_affected+M[x,y]
            cells_affected=cells_affected+1

# some outputs
print('Total population affected:',total_population_affected)
print('Cells affected:',cells_affected)


# add result to plot
plt.text(80,5,'Total population affected: '+str(round(total_population_affected,2)),size=fs)
plt.savefig('visualisation.png',format='png',dpi=300,bbox_inches='tight')






