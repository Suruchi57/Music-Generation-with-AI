from music21 import converter, note, chord
import glob
import pickle

def get_notes(midi_folder='data/'):
    notes = []
    for file in glob.glob(f"{midi_folder}/*.mid"):
        midi = converter.parse(file)
        notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    with open("notes.pkl", "wb") as f:
        pickle.dump(notes, f)
    return notes
