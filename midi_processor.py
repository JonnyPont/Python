# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:54:00 2018

@author: jp15101

https://github.com/kushalbhabra/pyMidi/blob/master/src/test.py

"""

import pygame

import pygame.midi

import time

#Needs initialising for some reason, and declaring that events need to be got
pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

#Separate midi functions, controllers, outputs need to be defined
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
output_id = pygame.midi.get_default_output_id()

in_midi_device = pygame.midi.Input( input_id )
out_midi_device = pygame.midi.Output(output_id)

#Creates an empty note table 
empty_midi_byte = [0,0,0,0]
input_note_table = [empty_midi_byte] * 10

#Little code test speed nugget
all_times = []

#Run forever
while True:
#    if a message exists
    if in_midi_device.poll():
        t = time.time()
#        store the first 10 new midi messages
        midi_events = in_midi_device.read(10)
        
        #Little code for turning off the programme from the midi controller.
        if midi_events[0][0] == [144, 72, 1, 0]:
            break
        
        #print received midi messages and 
        for i in range(len(midi_events)):
            if midi_events[i][0][0] == 144: #if note on
                #Add note to the top of the noteTable and shift everything down one line
                for j in range(8,-1,-1):
                    if input_note_table[j][2] != 0:
                        input_note_table[j+1] = input_note_table[j]                         
                input_note_table[j] = midi_events[i][0]
                input_note_table[0] = midi_events[i][0]
            elif midi_events[i][0][0] == 128: #if note off
                #Remove note from the noteTable 
                for j in range(len(input_note_table)):
                    #Find OffNote message in table
                    if midi_events[i][0][1] == input_note_table[j][1]:
                        #Shift every following note back up one
                        for k in range(j,9):
                            if k < 9:
                                input_note_table[k] = input_note_table[k+1]
                #Replace final note with empty values                
                input_note_table[9] = empty_midi_byte

            #print output noteTable for viewing reference
            output_note_table = input_note_table[:]
            for byte in output_note_table:
                print(*byte)    
            print('\n') 
        

#        #UpdownArp - functions
#        step_count = 0
#        step_increase = 1
        
#        #UpArp - functions
#        step_count = 0
#        step_increase = 2
        
#        #downArp - functions.
#        step_count = 1
#        step_increase = 2
        
        #downupArp - functions
        step_count = 1
        step_increase = 1
        
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
            for i in range(len(output_note_table)):
                if output_note_table[i][0] == 144:
                    #Don't play a note if it's the same as the last note played and there are other notes available.
                    #Removes repeats of high notes. Causes single notes to be played on repeat.
                    if output_note_table[i] == current_note and input_note_table[1] != empty_midi_byte:
                        continue    
                    else:    
                        #play notes from output table
                        out_midi_device.write_short(output_note_table[i][0],output_note_table[i][1],127)
                        #evaluate code runtime
                        elapsed = time.time()-t
                        all_times.append(elapsed)
                        time.sleep(0.2)
                        current_note = output_note_table[i]
            #counter used to control Up/Down functionalities            
            step_count+=step_increase
               

#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()