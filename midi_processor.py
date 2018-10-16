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


#Run forever
while True:
#    if a message exists
    if in_midi_device.poll():
#        store the first 10 new midi messages
        midi_events = in_midi_device.read(10)
        #print received midi messages
        for j in range(len(midi_events)):
            print(midi_events[0][j])
            print(midi_events[0][0][0],midi_events[0][0][1],midi_events[0][0][2])
            out_midi_device.write_short(midi_events[0][0][0],midi_events[0][0][1],midi_events[0][0][2])
        if midi_events[0][0] == [144, 72, 1, 0]:
            break
        

#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()

