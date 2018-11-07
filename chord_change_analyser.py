# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 23:43:15 2018

@author: Jon
"""

import pickle

chord_changes = pickle.load(open('chord_change_probabilities.p','rb'))

keys = chord_changes.keys()

prec_chord_seq = list(chord_changes.loc[:,keys[0]])
prec_chord = list(chord_changes.loc[:,keys[1]])
next_chord = list(chord_changes.loc[:,keys[2]])
probability = list(chord_changes.loc[:,keys[3]])

diff_prec_chords = set(prec_chord) #74 different chords
diff_next_chords = set(next_chord) #169 different chords

'''
Loop through diff_prec_chords:
    Loop through prec_chord:
        if diff == prec:
            find probability of the next chord given previous by making a list of
            probabilities.
            Will probs have to be a list of lists.
            OR MAYBE A DICTIONARY - BUT THAT INVOLVES SOME GOOD THINKING.
'''