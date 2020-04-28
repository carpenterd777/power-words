#!/usr/bin/env python3

from os import system
from os import name as os_name
from sys import stderr, exit
from datetime import datetime
from pathlib import Path
import cmd
import argparse

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

def init_file(file_name: str, session_title: str, session_number: int):
    '''Generates the log file. Resets it if it already 
    exists.'''

    date_string = datetime.now().strftime("%m-%d-%Y")

    f = open(file_name + '.txt', 'w')
    f.write("Session " + str(session_number) + ": " + session_title + " - " + date_string)
    f.close()

def append_note_to_file(file_name: str, note: str, *, newlines = 2):
    '''Appends a note to the log file.'''

    with open(file_name + '.txt', 'a') as f:
        f.write(("\n" * newlines) + note)

def check_path(string):
    '''Checks to see if the passed string is a valid path.
    Returns the valid path, raises an exception if it is
    invalid.'''
    p = Path(string)
    if p.exists() and p.suffix == '.txt':
        return p
    else:
        raise argparse.ArgumentTypeError('This is not a valid file path.')

def get_options():
    '''Gets the options that the user inputs when
    launching the program.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', action='store', type=check_path)
    options = parser.parse_args()
    return options

class PowerWords(cmd.Cmd):
    
    intro = "powerWords v1.0\n"
    prompt = "PowerWords> "

    def preloop(self):
        clear()
        options = get_options()
        if not options.file:
            self.session_title = session_title_prompt()
            self.session_number = session_number_prompt()
            self.fname = '_'.join(self.session_title.lower().split(' '))
            init_file(self.fname, self.session_title, self.session_number)
        else:
            self.fname = options.file.stem
        self.previous_time = None
        clear()
    
    def do_quit(self, arg_string):
        '''Exit the application.'''
        return True
    
    def default(self, arg_string):
        '''Appends a note to the log file.'''
        self.current_time = datetime.now().strftime('%I:%M %p')

        if self.current_time == self.previous_time:
            append_note_to_file(self.fname, arg_string, newlines=1)
        else:
            timed_arg_string = attach_time_to_note(arg_string)
            append_note_to_file(self.fname, timed_arg_string)

        self.previous_time = self.current_time

if __name__ == '__main__': PowerWords().cmdloop()
