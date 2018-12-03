# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 12:52:11 2018

@author: Jon
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
# matplotlib inline
import pretty_midi
import librosa
import librosa.display
import mir_eval
import mir_eval.display
import tables
import IPython.display
import os
import json
import time


# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
    """Given an MSD ID, generate the path prefix.
    E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
    return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)


def msd_id_to_mp3(msd_id):
    """Given an MSD ID, return the path to the corresponding mp3"""
    return os.path.join(DATA_PATH, 'msd', 'mp3',
                        msd_id_to_dirs(msd_id) + '.mp3')


# h5 removed from following bracket
def msd_id_to_h5(msd_id):
    """Given an MSD ID, return the path to the corresponding h5"""
    return os.path.join(RESULTS_PATH, 'lmd_matched_h5',
                        msd_id_to_dirs(msd_id) + '.h5')


def get_midi_path(msd_id, midi_md5, kind):
    """Given an MSD ID and MIDI MD5, return path to a MIDI file.
    kind should be one of 'matched' or 'aligned'. """
    return os.path.join(RESULTS_PATH, 'lmd_{}'.format(kind),
                        msd_id_to_dirs(msd_id), midi_md5 + '.mid')


# Local path constants
DATA_PATH = 'data'
RESULTS_PATH = 'C:/Users/Jon/Uni/Year 4/Project' #'results'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')

with open(SCORE_FILE) as f:
    scores = json.load(f)
# Grab a Million Song Dataset ID from the scores dictionary 
msd_id = list(scores.keys())[1234] #this doesn't seem to select different files as you may hope
print('Million Song Dataset ID {} has {} MIDI file matches:'.format(
    msd_id, len(scores[msd_id])))
for midi_md5, score in scores[msd_id].items():
    print('  {} with confidence score {}'.format(midi_md5, score))


i = 0

while i<3:#len(scores):
    i+=1
    start = time.time()
    # Grab an MSD ID and its dictionary of matches
    msd_id, matches = scores.popitem() #removes most recently added
    # Grab a MIDI from the matches
    midi_md5, score = matches.popitem()
    # Construct the path to the aligned MIDI
    aligned_midi_path = get_midi_path(msd_id, midi_md5, 'aligned')
    # Load/parse the MIDI file with pretty_midi
    pm = pretty_midi.PrettyMIDI(aligned_midi_path)

    # Retrieve piano roll of the MIDI file
    piano_roll = pm.get_piano_roll()
    
    # Use 7 octaves starting from C1
    piano_roll = piano_roll[12:96]
    
    #not producing the plot on each iteration causes memory to eventually crash
    fig = plt.figure(figsize=(3, 3))
#    plt.subplot(211)
    librosa.display.specshow(piano_roll)#, y_axis='cqt_note', cmap=plt.cm.hot)


    filename = 'resolution_testing' + '{0:05}'.format(i) + '.png'
    fig.savefig(filename,format='png',dpi=25,bbox_inches='tight',pad_inches=0) #currently 65x63 might need to adjust the data sooner
    plt.close(fig) #without this line, the code crashed after 62 iterations...with it, closed after 89
    print(filename + ' saved')
    end = time.time()
    print( str(end-start) + ' seconds to save chromagram')

## Retrieve piano roll of one of the instruments
#piano_roll = pm.instruments[4].get_piano_roll()
#piano_roll = piano_roll[12:96]
#fig = plt.figure(figsize=(10, 3))
#librosa.display.specshow(piano_roll, y_axis='cqt_note', cmap=plt.cm.hot)
## Get the text name of this instrument's program number
#program_name = pretty_midi.program_to_instrument_name(pm.instruments[4].program)
#plt.title('Instrument 4 ({}) piano roll'.format(program_name));
#fig.savefig('Instrument_Note_Piano_Roll.png',format='png',dpi=1200)
#
## pretty_midi also provides direct access to the pitch and start/end time of each note
#intervals = np.array([[note.start, note.end] for note in pm.instruments[4].notes])
#notes = np.array([note.pitch for note in pm.instruments[4].notes])
#fig = plt.figure(figsize=(10, 3))
#mir_eval.display.piano_roll(intervals, midi=notes, facecolor='orange')
#plt.title('Instrument 4 ({}) piano roll'.format(program_name))
#plt.xlabel('Time')
#plt.ylabel('MIDI note number');
#fig.savefig('Instrument_Midi_Piano_Roll.png')

