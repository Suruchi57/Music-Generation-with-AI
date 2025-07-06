import pickle
import numpy as np
import os
from music21 import stream, note, chord
from keras.models import load_model

def generate_music():
    # Load trained model
    model_path = "model/music_model.keras"  # ✅ use .keras if you updated save format
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found at {model_path}. Train your model first.")
    model = load_model(model_path)

    # Load notes
    with open("notes.pkl", "rb") as f:
        notes = pickle.load(f)

    pitch_names = sorted(set(notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))
    n_vocab = len(set(notes))

    # Prepare input sequence (use a random chunk)
    sequence_length = 100
    start_index = np.random.randint(0, len(notes) - sequence_length - 1)
    pattern = notes[start_index:start_index + sequence_length]
    int_pattern = [note_to_int[n] for n in pattern]

    print("🎶 Generating music...")

    prediction_output = []

    for _ in range(500):  # number of notes to generate
        input_seq = np.reshape(int_pattern, (1, sequence_length, 1)) / float(n_vocab)
        prediction = model.predict(input_seq, verbose=0)

        index = np.argmax(prediction)
        result = pitch_names[index]
        prediction_output.append(result)

        int_pattern.append(index)
        int_pattern = int_pattern[1:]

    # Convert to MIDI stream
    offset = 0
    midi_stream = stream.Stream()

    for pattern in prediction_output:
        if "." in pattern or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes_list = [note.Note(int(n)) for n in notes_in_chord]
            for n in notes_list:
                n.storedInstrument = None
            midi_chord = chord.Chord(notes_list)
            midi_chord.offset = offset
            midi_stream.append(midi_chord)
        else:
            midi_note = note.Note(pattern)
            midi_note.offset = offset
            midi_note.storedInstrument = None
            midi_stream.append(midi_note)
        offset += 0.5

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    output_path = "output/generated.mid"
    midi_stream.write("midi", fp=output_path)
    print(f"✅ Music saved to {output_path}")

    return output_path
