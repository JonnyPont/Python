# Imports
import numpy as np
#import matplotlib.pyplot as plt
# matplotlib inline
import pretty_midi
#import librosa
#import librosa.display
#import mir_eval
#import mir_eval.display
#import tables
#import IPython.display
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

#Get a file and check what it matches in MSD.
with open(SCORE_FILE) as f:
    scores = json.load(f)
# Grab a Million Song Dataset ID from the scores dictionary 
msd_id = list(scores.keys())[1234] #this doesn't seem to select different files as you may hope
#print('Million Song Dataset ID {} has {} MIDI file matches:'.format(
#    msd_id, len(scores[msd_id])))
#for midi_md5, score in scores[msd_id].items():
#    print('  {} with confidence score {}'.format(midi_md5, score))


''' Looping chromagram plotter. Set i<1 for a single iteration. Currently broke on iteration 865 '''
midi_file_number = 0
saved            = 0
while midi_file_number<len(scores):
    midi_file_number+=1
    ''' This particular iteration seems to cause issues which I cannot explain. 
        Long term it's worth working out a better method than popitem() for 
        iterating through the data as the current method effectively only has 
        one shot of completion but saves everything off as it runs so there's 
        no reason why it couldn't be 'paused' and 'resumed' '''
#    if midi_file_number == 865:
#        continue
    print(midi_file_number)
    #error in this particular midi file. seems to have note outside of 0-127 range?
    start = time.time()
    # Grab an MSD ID and its dictionary of matches
    msd_id, matches = scores.popitem() #removes most recently added - matches is sometimes missing and sometimes not
    # Grab a MIDI from the matches
    midi_md5, score = matches.popitem()
    # Construct the path to the aligned MIDI
    aligned_midi_path = get_midi_path(msd_id, midi_md5, 'aligned')
    
    #Some of the midi data contains midi note values >127. This try avoids issues in these areas
    try:
        # Load/parse the MIDI file with pretty_midi
        pm = pretty_midi.PrettyMIDI(aligned_midi_path)
    except OSError:
        continue
    
    
    # Retrieve piano roll of the MIDI file
    piano_roll = pm.get_piano_roll()
    
    # Retrieve the beats and downbeats from pretty_midi
    # Note that the beat phase will be wrong until the first time signature change after 0s
    # So, let's start beat tracking from that point
    '''List index out of range error - just skipping that value for now'''
    try:
        first_ts_after_0 = [ts.time for ts in pm.time_signature_changes if ts.time > 0.][0]
    except IndexError:
        continue
    
    # Get beats from pretty_midi, supplying a start time
    beats = pm.get_beats(start_time=first_ts_after_0)
    
    # .. downbeats, too
    downbeats = pm.get_downbeats(start_time=first_ts_after_0)
            
    #Process 8 bar sections for each instrument.
    for instrument_channel in range(len(pm.instruments)):
        # Retrieve piano roll of one of the instruments. Defined in 16th beats
        piano_roll = pm.instruments[instrument_channel].get_piano_roll(fs=4/(beats[1]-beats[0])) #beats is seconds. Input is frequency.
        # Use 7 octaves starting from C1
        #piano_roll = piano_roll[12:96]
        
        # Get instrument name
        program_name = pretty_midi.program_to_instrument_name(pm.instruments[instrument_channel].program)
        #Skip instrument if drum.
        if pm.instruments[instrument_channel].is_drum:
            continue
        
        # pretty_midi also provides direct access to the pitch and start/end time of each note
        intervals = np.array([[note.start, note.end] for note in pm.instruments[instrument_channel].notes])
        notes = np.array([note.pitch for note in pm.instruments[instrument_channel].notes]) 
        
#        # Get key data for each MIDI file.
#        for key_change in pm.key_signature_changes:
#            print('Key {} starting at time {:.2f}'.format(
#                pretty_midi.key_number_to_key_name(key_change.key_number), key_change.time))
        
        # Redefine each on note as a 1 rather than assigning a velcoity.
        tester = piano_roll >= 1
        for midi_note in range(piano_roll.shape[0]):
            for sixteenth_beat in range(piano_roll.shape[1]):
                if tester[midi_note][sixteenth_beat] == True:
                    piano_roll[midi_note][sixteenth_beat] = 1
        
        #If not divisible into exact number of bars, cut off the final part of bar.
        piano_roll_trimmed = piano_roll
        while piano_roll_trimmed.shape[1]/16 % 1 != 0: #while non-integer
            piano_roll_trimmed = np.delete(piano_roll_trimmed,-1,axis=1)
        
        #check to avoid zero error. Not sure why piano_roll_trimmed.shape[1]==0
        if piano_roll_trimmed.shape[1] !=0:
            formatted_bars = np.split(piano_roll_trimmed,piano_roll_trimmed.shape[1]/16,axis=1)
        
        #determine if monophonic
        monophonic = True
        for midi_note in range(len(formatted_bars)):
            for sixteenth_beat in range(formatted_bars[midi_note].shape[1]):
                if sum(formatted_bars[midi_note][:,sixteenth_beat]) > 1:
                    monophonic = False
        
        #Save conditions. Saving 8 bar sections if monophonic.
        if monophonic == True:
            save_list   = [None]*8
            count       = 0
            for bar_id in range(len(formatted_bars)):
                #we are looping through all bars, but we want to only ever save the list when count reaches 8 and then reset
                save_list[bar_id%8] = formatted_bars[bar_id]
                count += 1
                #save off if 8 consecutive bars found
                if count%8==0:
                    np.save('8_bar_data/monophonic_8bar_'+'{}'.format(saved)+'.npy',save_list)
#                    print('file saved')
                    saved += 1            
                    #once saved need to prepare for the next scan through
                    save_list=[None]*8
            #see if any bars were not saved
#            if count%8!=0:
#                print('Some bars lost to the void')
                    
#        elseif monophonic == False:
            '''An idea here would be to save off the polyphonic music tracks. 
               These have many potential uses. 
               1. Put into melody GAN to see what happens.
               2. Polyphonic is more relevant to arpeggiator usecase.
               3. Might as well have the data.
               Before implementing - ensure to have separate monophonic/polyphonic
               save folders.'''
#            print('Data includes polyphonic sections so is not appropriate for saving.')
            
            
            
            
            