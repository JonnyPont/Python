# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:20:57 2018

@author: Jon
"""

import time

def remove_note(note_table,input_note):
    'Remove a midi note from the notetable'    
    #Remove note from the noteTable 
    empty_midi_byte = [0,0,0,0]
    for temp_midi_loc in range(len(note_table)):
        #Find OffNote message in table
        if input_note == note_table[temp_midi_loc][1]:
            #Shift every following note back up one
            for k in range(temp_midi_loc,len(note_table)-1):
                if k < len(note_table)-1:
                    note_table[k] = note_table[k+1]
    #Replace final note with empty values                
    note_table[-1] = empty_midi_byte
    return note_table


        
def add_note(note_table,new_note):
    'Add a midi note to the top of the notetable.'
    #Add note to the top of the noteTable and shift everything down one line
    for temp_midi_loc in range(len(note_table)-2,-1,-1): # -2 as final datum not important and code runs to +1
        if note_table[temp_midi_loc][2] != 0:
            note_table[temp_midi_loc+1] = note_table[temp_midi_loc]                         
    note_table[temp_midi_loc] = new_note
    note_table[0] = new_note
    return note_table


def arpeggiate_note_table(in_midi_device,out_midi_device,input_note_table,arpeggiate_type='updown',tempo=120):
    '''Arpeggiate the received note table'''
    empty_midi_byte = [0,0,0,0]
    output_note_table = input_note_table[:]
    
    if str(arpeggiate_type) == 'up':
        step_count = 0
        step_increase = 2
    elif str(arpeggiate_type) == 'down':
        step_count = 1
        step_increase = 2
    elif str(arpeggiate_type) == 'downup':
        step_count = 1
        step_increase = 1
    elif str(arpeggiate_type) == 'updown':    
        step_count = 0
        step_increase = 1        
    else:
        print("That is not a valid arpeggiator function")        

    current_note = empty_midi_byte
    
    '''This runs indefinitely until a new message has been received. Currently, 
    if new note on messages are received then everything is fine and dandy. 
    If new note off messages are received then the output only changes after a 
    complete loop. This means there is significant delay. I need to look into
    how the poll messages look for NoteOff and see how they differ from note on
    to see if that can give the necessary answers.'''
    while in_midi_device.poll() == False:
        if step_count % 2 == 0:
            output_note_table.sort(key=lambda x: x[1])              #upArp
        elif step_count % 2 == 1:
            output_note_table.sort(key=lambda x: x[1],reverse=True) #downArp 
        #loop through note table and play the notes
        for note_loc in range(len(output_note_table)):
            t = time.time()
            if output_note_table[note_loc][0] == 144:
                #Don't play a note if it's the same as the last note played and there are other notes available.
                #Removes repeats of high notes. Causes single notes to be played on repeat.
                if output_note_table[note_loc] == current_note and input_note_table[1] != empty_midi_byte:
                    continue    
                else:    
                    #play notes from output table
                    out_midi_device.write_short(output_note_table[note_loc][0],output_note_table[note_loc][1],127)
                    #evaluate code runtime - bit antequated...I could do with a new way of going about doing this.
                    elapsed = time.time()-t
#                    #IT would be better to wait for the remaining amount of time. If code has run for 0.1 secs
#                    #already then we want it to only wait 0.1 secs. for example
#                    all_times.append(elapsed)
                    time.sleep(60/tempo-elapsed)
                    current_note = output_note_table[note_loc]
        #counter used to control Up/Down functionalities            
        step_count+=step_increase