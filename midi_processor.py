# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:54:00 2018

@author: jp15101

https://github.com/kushalbhabra/pyMidi/blob/master/src/test.py

next job is to make the arpeggiated note table, I think I'll need to define
some new ways of sorting. Each list will need indexing before pulling so to 
reduce the amount of loops used in looking through the data.

"""




import pygame

import pygame.midi

import time

#Needs initialising for some reason, and declaring that events need to be got
pygame.init()

pygame.fastevent.init()

event_get = pygame.fastevent.get

event_post = pygame.fastevent.post


pygame.midi.init()

input_id = pygame.midi.get_default_input_id()
output_id = pygame.midi.get_default_output_id()


in_midi_device = pygame.midi.Input( input_id )
out_midi_device = pygame.midi.Output(output_id)

#Creates an empty note table
empty_midi_byte = [0,0,0,0]
note_table = [empty_midi_byte] * 10


#Run forever
while True:
#    if a message exists
    if in_midi_device.poll():
        t = time.time()
#        store the first 10 new midi messages
        midi_events = in_midi_device.read(10)
        
        if midi_events[0][0] == [144, 72, 1, 0]:
            break
        
        #print received midi messages and 
        for i in range(len(midi_events)):
            if midi_events[i][0][0] == 144: #if note on
                '''Add note to notetable here'''
                for j in range(8,-1,-1):
                    if note_table[j][2] != 0:
                        note_table[j+1] = note_table[j]                         
                note_table[j] = midi_events[i][0]
                note_table[0] = midi_events[i][0]
            elif midi_events[i][0][0] == 128: #if note off
                '''Remove note from notetable here''' 
                for j in range(len(note_table)):
                    #Find OffNote message in table
                    if midi_events[i][0][1] == note_table[j][1]:
                        #Shift every following note back up one
                        for k in range(j,9):
                            if k < 9:
                                note_table[k] = note_table[k+1]
                #Replace final note with empty values                
                note_table[9] = empty_midi_byte              
#            print(midi_events[0][i])
            for byte in note_table:
                print(*byte)    
            #send to output (windows' own synth) - keep for future reference
            #out_midi_device.write_short(midi_events[0][0][0],midi_events[0][0][1],midi_events[0][0][2])
        
        #loop through note table and play the notes
        for i in range(len(note_table)):
            if note_table[i][0] == 144:
                out_midi_device.write_short(note_table[i][0],note_table[i][1],note_table[i][2])
                elapsed = time.time()-t
                time.sleep(0.1)
        print('\n')    
        
        
        
        

#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()