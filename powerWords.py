#!/usr/bin/env python3

from os import system
from os import name as os_name
from sys import stderr, exit
from datetime import datetime
from pathlib import Path
import cmd
import argparse
from fpdf import FPDF

LINE_SPACING = 5

def clear():
    '''Clears the screen. Written to work on both Windows and UNIX
    operating systems.
    '''
    if os_name == 'nt':
        system('cls') # Windows
    else:
        system('clear') # UNIX

def doc_write(string, pdf, file_name):
    '''Writes the text to the PDF file and log reading file.'''

    pdf.write(LINE_SPACING, string)
    with open(file_name + '.log', 'a') as f:
        f.write(string)

def doc_image(image_path, pdf, file_name):
    '''Adds the image to the document and a string to the log
    indicating the image added.
    '''

    pdf.write(LINE_SPACING, '\n')
    pdf.image(image_path, w = 50)
    with open(file_name + '.log', 'a') as f:
        f.write('\n\n!image ' + image_path)

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
    '''Generates the document file and data recovery log.'''

    date_string = datetime.now().strftime("%m-%d-%Y")

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_title("Session " + str(session_number) + ": " + session_title + " - " + date_string)
    pdf.set_font('Arial', size = 12)
    pdf.add_page()
    with open(file_name + '.log', 'w') as f:
        f.write("Session " + str(session_number) + ": " + session_title + " - " + date_string)
    
    return pdf

def append_note_to_file(file_name: str, pdf, note: str, *, newlines = 2):
    '''Appends a note to the log file.'''

    pdf.set_font('Arial', size = 12)
    doc_write(("\n" * newlines) + note, pdf, file_name)

def check_path(string):
    '''Checks to see if the passed string is a valid path.
    Returns the valid path, raises an exception if it is
    invalid.'''
    p = Path(string)
    if p.exists() and p.suffix == '.pdf':
        if Path(p.stem + '.log').exists():
            return p
        else:
            raise argparse.ArgumentTypeError('Could not find accompanying log file.')
    else:
        raise argparse.ArgumentTypeError('This is not a valid file path.')

def get_options():
    '''Gets the options that the user inputs when
    launching the program.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', action='store', type=check_path)
    options = parser.parse_args()
    return options

def rewrite_doc(fname: str):
    '''Returns a new CustomPDF object with all the logs
    from the log file written onto it.

    This function is necessary because the CustomPDF object does
    not allow further writes to be made once the output file has been generated.
    '''

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')

    pdf.set_font('Arial', size = 12)

    with open(fname + '.log', 'r') as f:
        lines = f.readlines()
        pdf.set_title(lines[0])
        pdf.add_page()
        for line in lines[1:]:
            if line[0:6] == '!image':
                image_path = line.split(' ')[1]
                if Path(image_path).exists():
                    pdf.write(LINE_SPACING, '\n')
                    pdf.image(image_path, w=50)
            else:  
                pdf.write(LINE_SPACING, line)
    
    return pdf

class CustomPDF(FPDF):

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(self.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(255, 255, 255)
        # self.set_text_color(31, 3, 1)
        # Title
        self.cell(w, 9, self.title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

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
            self.pdf = init_file(self.fname, self.session_title, self.session_number)
        else:
            self.fname = options.file.stem
            self.pdf = rewrite_doc(self.fname)
        self.previous_time = None
        clear()
    
    def do_image(self, arg_string):
        '''Adds an image in the same directory as the program
        to the document.'''
        
        #validation
        p = Path(arg_string)
        if not p.exists():
            print("That file could not be found.", file=stderr)
            return
        elif p.suffix not in ['.jpg', '.png']:
            print("That file is not an image.", file=stderr)
            return

        path_string = str(p.parents[0]) + '/' + p.name if p.parents else p.name
        
        doc_image(path_string, self.pdf, self.fname)
    
    def do_quit(self, arg_string):
        '''Outputs the notes and exits the application.'''
        self.pdf.output(self.fname + '.pdf')
        return True
    
    def default(self, arg_string):
        '''Appends a note to the log file.'''
        self.current_time = datetime.now().strftime('%I:%M %p')

        if self.current_time == self.previous_time:
            append_note_to_file(self.fname, self.pdf, arg_string, newlines=1)
        else:
            timed_arg_string = attach_time_to_note(arg_string)
            append_note_to_file(self.fname, self.pdf, timed_arg_string)

        self.previous_time = self.current_time

if __name__ == '__main__': PowerWords().cmdloop()
