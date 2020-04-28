# power-words

A command-line tool to quickly take timestamped notes exported to a PDF.

## Adding Text

To add some text to the document, simply begin entering text into the prompt, and hit Enter to write the new note. Keep in mind that the program will attempt to run this text as a command if it begins with one of the command keywords, so plan accordingly.

## Commands

### image

Adds a .png or .jpg image to the document with the specified file path relative to the file location of this program.

### quit

Exits the program, and outputs the resulting PDF.

## Opening Up a Previous Session

Using the -f or --file options, the program can open a previous session's PDF file and continue adding to that document. Currently, PowerWords will look for a `session_title.log` file that corresponds to a `session_title.pdf` file in the same file location. This file, as well as any previous image files added to the document last session, are required in order to properly reload the document.
