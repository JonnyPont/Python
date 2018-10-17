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
input_note_table = [empty_midi_byte] * 10


all_times = []

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
                    if input_note_table[j][2] != 0:
                        input_note_table[j+1] = input_note_table[j]                         
                input_note_table[j] = midi_events[i][0]
                input_note_table[0] = midi_events[i][0]
            elif midi_events[i][0][0] == 128: #if note off
                '''Remove note from notetable here''' 
                for j in range(len(input_note_table)):
                    #Find OffNote message in table
                    if midi_events[i][0][1] == input_note_table[j][1]:
                        #Shift every following note back up one
                        for k in range(j,9):
                            if k < 9:
                                input_note_table[k] = input_note_table[k+1]
                #Replace final note with empty values                
                input_note_table[9] = empty_midi_byte
            #Check for new notes
            elif in_midi_device.poll():
                print('The end 1')
                break
#            print(midi_events[0][i])

            #send to output (windows' own synth) - keep for future reference
            #out_midi_device.write_short(midi_events[0][0][0],midi_events[0][0][1],midi_events[0][0][2])
            output_note_table = input_note_table[:]
            for byte in output_note_table:
                print(*byte)    
            print('\n') 
        
        '''This currently causes the code to halt if notes are played in quick 
        succession. Need to lok into this better. '''
#        #Check if new note has been played
#        if in_midi_device.poll():
#            print('The end 2')
#            break
            
#        output_note_table.sort(key=lambda x: x[1])              #upArp
#        output_note_table.sort(key=lambda x: x[1],reverse=True) #downArp 
        
        #UpdownArp
        step_count = 0
        step_increase = 1
        
#        #UpArp
#        step_count = 0
#        step_increase = 2
#        
#        #downArp
#        step_count = 1
#        step_increase = 2
#        
#        #downupArp
#        step_count = 1
#        step_increase = 1
        current_note = empty_midi_byte
        
        while in_midi_device.poll() == False:
            if step_count % 2 == 0:
                output_note_table.sort(key=lambda x: x[1])              #upArp
            elif step_count % 2 == 1:
                output_note_table.sort(key=lambda x: x[1],reverse=True) #downArp 
            #loop through note table and play the notes
            for i in range(len(output_note_table)):
                if output_note_table[i][0] == 144:
                    if output_note_table[i] == current_note:
                        continue    
                    else:    
                        out_midi_device.write_short(output_note_table[i][0],output_note_table[i][1],output_note_table[i][2])
                        elapsed = time.time()-t
                        all_times.append(elapsed)
                        time.sleep(0.2)
                        current_note = output_note_table[i]
            step_count+=1
               


#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()