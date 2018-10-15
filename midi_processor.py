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

i = pygame.midi.Input( input_id )



#Run forever
while True:
#    if a message exists
    if i.poll():
#        store the first 10 new midi messages
        midi_events = i.read(10)
        #print received midi messages
        for j in range(len(midi_events)):
            print(midi_events[0][j])




#Close off all of the opened channels and exit the initialisations.
i.close()

pygame.midi.quit()

pygame.quit()

