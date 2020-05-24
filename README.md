# power-words

A command-line tool to quickly take timestamped notes exported to a PDF.

## Dependencies

To run this, the [PyFPDF module](https://pypi.org/project/fpdf/) is requried.

Run `pip install fpdf`

## Adding Text

To add some text to the document, simply begin entering text into the prompt, and hit Enter to write the new note. Keep in mind that the program will attempt to run this text as a command if it begins with one of the command keywords, so plan accordingly.

## Commands

### image

Adds a .png or .jpg image to the document with the specified file path relative to the file location of this program.

### quit

Exits the program, and outputs the resulting PDF.

## Opening Up a Previous Session

Using the --recover option, PowerWords can open the previous session's data and generate a new document with the old data plus any new data added. Currently, this is only available for the session immediately prior.
