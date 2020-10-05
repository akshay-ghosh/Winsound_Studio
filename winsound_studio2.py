# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 16:59:04 2018

@author: Akshay Ghosh
-----------------------------------------------------------------------
IDEAS:
function where you can send array of [notes,times] and it plays that song

map notes to keyboard and have DYNAMIC KEYBOARD
-----------------------------------------------------------------------
BIG IDEAS:
    
send sound file and convert to winsound sounds (FOURIER TRANSFORM??)
read sheet music and convert to winsound sounds (FOURIER TRANSFORM OF PICS??)
-----------------------------------------------------------------------
"""

#######################################################################
#EXTENSIONS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
import winsound as ws
import time
import math
import random

#######################################################################
#FUNCTIONS

def npa(x):
    '''
    Converts a list x to a numpy array
    '''
    return np.array(x)

def convert_st_freq(x, ref = 220):
    '''
    Reads # of semitones up from ref, converts to frequency in Hz
    
    ref = 220 Hz by default (this is A3)
    x = # semitones up from A3
    '''
    #exp = math.log(ref, 2) + (x/12.0) #log of reference with base 2 plus number semitones
    note_freq = math.pow(2, math.log(ref, 2) + (x/12.0)) #raises 2 to the exponent what was just calculated to get note
    note_freq_int = int(round(note_freq)) # ws.Beep only takes integer freqs
    return note_freq_int

def convert_str_st(note_name):
    '''
    convert note as string to #semitones
    x is string
    output integer # of semitones
    '''
    notes = npa(["A3","Bb3","B3","C3","C#3","D3","Eb3","E3","F3","F#3","G3","G#3",
                      "A4","Bb4","B4","C4","C#4","D4","Eb4","E4","F4","F#4","G4","G#4",
                      "A5","Bb5","B5","C5","C#5","D5","Eb5","E5","F5","F#5","G5","G#5",
                      "A6","Bb6","B6","C6","C#6","D6","Eb6","E6","F6","F3#6","G6","G#6",
                      "A7","Bb7","B7","C7","C#7","D7","Eb7","E7","F7","F3#7","G7","G#7"])
    notes_l = len(notes)
    for i in range(notes_l):
        if note_name == notes[i]:
            output = i
            break

    return output

def m(x):
    '''
    Reads in a note as a string, converts to frequency in Hz
    
    note as string -> note as index in notes vector -> frequency in Hz
    '''
    return convert_st_freq(convert_str_st(x))

def n(note,time_):
    '''
    note as string -> note as idx in notes vec -> freq in Hz -> play sound
    time as string -> time in ms
    '''
    #print(note)
    if note == 'r':
        time.sleep(t(time_)/1000.0) # divide by 1000 bc time.sleep takes secs
    else:
        ws.Beep(convert_st_freq(convert_str_st(note)),t(time_))
        #print(convert_st_freq(convert_str_st(note))) ######
    return

def t(note_length):
    '''
    note length as string -> note length in ms
    
    currently only supports 4/4
    e - > eighth note, q -> quarter note, h - > half note, w -> whole note
    '''
    
    tempo = 60
    if note_length == 'ts':
        multiplier = 0.125 # thirty second
    if note_length == 's': # sixteenth
        multiplier = 0.25
    elif note_length == 'e': # eighth
        multiplier = 0.5
    elif note_length == 'q': # quarter
        multiplier = 1
    elif note_length == 'h': # half
        multiplier = 2
    elif note_length == 'w': # whole
        multiplier = 4
    
    note_time = (1.5*60000/tempo)*multiplier # converts from bpm to ms
    note_time_int = int(round(note_time)) # note time must be in int # of ms
    #print(note_time,note_time_int) #############
    return note_time_int
    
def playsong(notes,times):
    '''
    reads in a list of notes and times and plays the song
    '''
    song_l = len(notes)
    for i in range(song_l):
        n(notes[i],times[i])
    return

def playfromfile(filename):
    '''
    reads in a csv file and returns an array of notes,times as strings
    needs csv file in following format:
    col 0 is named Notes, col 1 is named Times
    '''
    df = pd.DataFrame()
    df = pd.read_csv(filename)
    
    X = npa(df[['Notes']]) # vector of notes
    Y = npa(df[['Times']]) # vector of times
    playsong(X,Y)
    return
    
#######################################################################
#MUSIC

def playscale(key,scale):
    '''
    key = root note as string eg 'A4'
    scale = type (major,minor)
    '''
    major_vec = npa([0,2,4,5,7,9,11,12])
    
    minor_vec = npa([0,2,3,5,7,8,10,12])
    
    harmonic_minor_vec = npa([0,2,3,5,7,8,11,12])
    
    pentatonic_vec = npa([0,3,5,7,10,12])
    
    
    key_idx = convert_str_st(key)
    if scale == 'major':
        vec = major_vec
        vec_l = len(major_vec)
    elif scale == 'minor':
        vec = minor_vec
        vec_l = len(minor_vec)
    elif scale == 'harmonic minor':
        vec = harmonic_minor_vec
        vec_l = len(harmonic_minor_vec)
    elif scale == 'pentatonic':
        vec = pentatonic_vec
        vec_l = len(pentatonic_vec)
        
    for i in range(vec_l):
        if i == vec_l - 1:
            ws.Beep(convert_st_freq(key_idx + vec[i]),t('q'))
            #n(convert_st_freq(key_idx + vec[i]),800)
        else:   
            ws.Beep(convert_st_freq(key_idx + vec[i]),t('e'))
            #n(convert_st_freq(key_idx + vec[i]),300)
            
    return


#######################################################################
#ACCESS DATA

filename = 'winsound_song1.csv'
#df = pd.DataFrame()
#df = pd.read_csv(filename)
#
#X = npa(df[['Notes']])
#Y = npa(df[['Times']])


#######################################################################
#SET TEMPO
    
#global tempo
#tempo = 220. # in beats/minute
#tempo = tempo * 1000 / float(60) # in beats/millisecond (q note)

#######################################################################
#MAIN

#song_notes = npa(['C#4','C#4','C4',
#                  'A3','G3','F3','E3',
#                  'C4','C4','C4',
#                  'A3','G3','F3','E3','A3','Bb3','C4','E4',
#                  'C4'])
#
#song_time =  npa(['h' ,'q', 'q' ,
#                  'q' ,'q' ,'q' ,'q',
#                  'h' ,'q', 'q',
#                  'e','e','e','e','e','e','e','e',
#                  'w'])
#
##playsong(fromfile(filename))
##playfromfile(filename)
##playsong(song_notes,song_time)
#playscale('A3','harmonic minor')

playfromfile('baba_o_riley_intro.csv')













