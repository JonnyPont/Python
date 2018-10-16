# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:54:00 2018

@author: jp15101

https://github.com/kushalbhabra/pyMidi/blob/master/src/test.py

"""




import pygame

import pygame.midi

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
#        store the first 10 new midi messages
        midi_events = in_midi_device.read(10)
        
        if midi_events[0][0] == [144, 72, 1, 0]:
            break
        
        #print received midi messages and send to output (windows' own synth)
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
                    if midi_events[i][0][1] == note_table[j][1]:
                        for k in range(j,9):
                            if k < 9:
                                note_table[k] = note_table[k+1]  
                                print(k+1)
                note_table[9] = empty_midi_byte              
#            print(midi_events[0][i])
            for byte in note_table:
                print(*byte)    
            out_midi_device.write_short(midi_events[0][0][0],midi_events[0][0][1],midi_events[0][0][2])
        print('\n')    
        
        
        
        

#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()