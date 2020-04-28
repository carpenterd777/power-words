#!/usr/bin/env python3

from os import system
from os import name as os_name
from sys import stderr, exit
from datetime import datetime

def clear():
    '''Clears the screen. Written to work on both Windows and UNIX
    operating systems.
    '''
    if os_name == 'nt':
        system('cls') # Windows
    else:
        system('clear') # UNIX

def session_number_prompt():
    '''Prompts the user for the session number until a valid one
    is entered. Returns a valid session number.'''

    session_number = None
    while type(session_number) != int:
        session_number = input("Session number: ")
        try:
            session_number = int(session_number)
        except ValueError:
            print("That is not a valid session number.", file=stderr)
            continue

    return session_number

def session_title_prompt():
    '''Prompts the user for the session title. Returns the session
    title.'''

    session_title = ''
    while session_title == '':
        session_title = input("Session title: ")
    
    return session_title

def attach_time_to_note(note: str):
    '''Returns a string with a time affixed to the front of
    the string.'''

    time = datetime.now().strftime('%I:%M %p')

    return time + " " + note

def init_file(session_title: str, session_number: int):
    '''Generates the log file. Resets it if it already 
    exists.'''

    file_name = '_'.join(session_title.lower().split(' '))
    date_string = datetime.now().strftime("%m-%d-%Y")

    f = open(file_name + '.txt', 'w')
    f.write("Session " + str(session_number) + ": " + session_title + " - " + date_string)
    f.close()

def append_note_to_file(session_title: str, note: str, *, newlines = 2):
    '''Appends a note to the log file.'''
    file_name = '_'.join(session_title.lower().split(' '))

    with open(file_name + '.txt', 'a') as f:
        f.write(("\n" * newlines) + note)

def check_commands(command: str):
    if command == "-q":
        exit()
    
def note_prompt():
    '''Quietly prompts the user for a note. Checks for commands. 
    If no commands given, returns the note as a string.'''

    clear()
    note = input()
    check_commands(note)
    return note

def main():
    clear()
    print("powerWords v0.1\n")
    print("Commands:")
    print("-q: quit\n")
    session_title = session_title_prompt()
    session_number = session_number_prompt()
    init_file(session_title, session_number)
    previous_time = None
    while True:

        note = note_prompt()
        current_time = datetime.now().strftime('%I:%M %p')

        if current_time == previous_time:
            append_note_to_file(session_title, note, newlines=1)
        else:
            note = attach_time_to_note(note)
            append_note_to_file(session_title, note)

        previous_time = current_time

if __name__ == '__main__':
    main()