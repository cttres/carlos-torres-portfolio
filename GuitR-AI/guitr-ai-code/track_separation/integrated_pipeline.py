import os
import torch
import numpy as np

from demucs_isolation import isolate_guitar   # Your file for guitar isolation
from data_prep import extract_chroma          # Or wherever your chroma code is
from model import ChordRNN                    # Your RNN model
# If you have a saved chord_vocab, either import or load it

def predict_chords_from_audio(input_file, model, chord_vocab, seq_length=20):
    """
    1) Isolate guitar track using Demucs.
    2) Extract chroma features from isolated guitar.
    3) Split into sequences and run RNN for chord prediction.
    """
    # 1. Isolate guitar
    guitar_path = isolate_guitar(input_file)

    # 2. Extract chroma from the isolated guitar
    chroma = extract_chroma(guitar_path)  # shape: (num_frames, 12)

    # 3. Prepare sequences for RNN
    X = []
    for start_idx in range(0, chroma.shape[0] - seq_length, seq_length):
        end_idx = start_idx + seq_length
        X.append(chroma[start_idx:end_idx])
    X = np.array(X, dtype=np.float32)  # shape: (num_sequences, seq_length, 12)

    # Convert to torch tensor
    X_tensor = torch.from_numpy(X)  # (num_sequences, seq_length, 12)

    # 4. Run inference
    model.eval()
    with torch.no_grad():
        outputs = model(X_tensor)  # (num_sequences, num_classes)
        preds = torch.argmax(outputs, dim=1).tolist()

    # 5. Map IDs to chord labels
    inv_vocab = {v: k for k, v in chord_vocab.items()}
    chord_predictions = [inv_vocab[p] for p in preds]

    return chord_predictions

if __name__ == "__main__":
    # Load your trained model
    num_classes = 589  # or len(chord_vocab)
    model = ChordRNN(input_size=12, hidden_size=64, num_layers=2, num_classes=num_classes)
    model.load_state_dict(torch.load("chord_rnn.pth", map_location=torch.device("cpu")))

    # Suppose chord_vocab is loaded or re-generated. Example:
    chord_vocab = {
    "N/A": 0,
    "C:maj": 1,
    "D:maj": 2,
    # etc...
}  # or load from file

    # Run the pipeline on a sample track
    input_song = "test_clip1.wav"
    chords = predict_chords_from_audio(input_song, model, chord_vocab)
    print("Predicted chord sequence:", chords)
