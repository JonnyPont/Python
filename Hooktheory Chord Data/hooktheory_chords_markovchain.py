# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 17:13:36 2018

@author: Jon

This should be a MARKOV CHAIN!
"""

import pickle
import numpy as np
import random
import bisect

first_order_chords  = pickle.load(open("first_order_chords_normalised.p","rb"))
keys                = list(first_order_chords.keys())
keys_sorted         = sorted(keys)

''' Loop through all of the data.'''
trans_mat = np.zeros([len(keys_sorted),len(keys_sorted)]) #This nearly returns a zeros matrix. I need it to be zero anyway. Might have to do it manually.

for key in keys_sorted:    
    ''' For key, find the prob of relative key. Find in numpy matrix and replace
        the value present.'''   
    for i in range(len(first_order_chords[key])):    
        ''' This has not been tested, but the logic is sound. '''
        input_chord_loc     = keys_sorted.index(key) #location of input chord
        output_chord        = first_order_chords[key][i]['chord_ID'] #Value of output chord
        output_prob         = first_order_chords[key][i]['probability'] #probability of output chord
        '''Check the chord exists in the list. This means that not all my 
           row probabilities add to 1. Not sure if this is an issue or not. In 
           time it will be worth normalising this.'''
        if output_chord in keys_sorted:
            output_chord_loc    = keys_sorted.index(first_order_chords[key][i]['chord_ID']) #index of output chord    
            trans_mat[input_chord_loc][output_chord_loc] = output_prob
        
''' Generate a sequence of 4 chords. '''    

''' Make a normalised random input chord vector. Attempt to weight it in the 
    direction of a certain chord in the list. '''
current_state = [0]*len(keys_sorted)
for i in range(len(keys_sorted)):
    current_state[i] = random.random()
    
#current_state[0] = 1    #bias towards this chord? Testing seems to prove this is the case.
prob_factor      = 1/sum(current_state)
current_state    = [prob_factor * p for p in current_state]

''' Generate a chord sequence following a markov chain. '''
for chord in range(10):
    ''' Roulette wheel sampler '''
    seed = random.random()        
    index_for_now = bisect.bisect_left(np.cumsum(current_state),seed)-1 #Finds insertion point. I want value one before insertion point.
    print(keys_sorted[index_for_now])
    current_state = trans_mat.dot(current_state)
    
    

'''Next state = transitionMatrix*currentState. This should actually be: 
    transitionMatrix.dot(currentState)'''

''' I think a state would be the chances of playing each chord. '''

''' For now, just select the most likely chord to be played next.'''    