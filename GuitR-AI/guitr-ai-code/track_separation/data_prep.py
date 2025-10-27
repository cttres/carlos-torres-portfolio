import os
import json
import librosa
import numpy as np

def parse_jams_file(jams_file):
    """
    Manually parse a .jams file (JSON) and return chord annotations.
    Returns a list of (start_time, end_time, chord_label).
    """
    chord_annotations = []
    with open(jams_file, 'r') as f:
        data = json.load(f)

    for annotation in data.get("annotations", []):
    # We read 'annotation["namespace"]' directly
        if annotation.get("namespace") == "chord":
            for obs in annotation.get("data", []):
                start_time = obs.get("time", 0.0)
                duration = obs.get("duration", 0.0)
                chord_label = obs.get("value", "N/A")
                end_time = start_time + duration
                chord_annotations.append((start_time, end_time, chord_label))
    return chord_annotations


def extract_chroma(audio_path, sr=22050, hop_length=512):
    """
    Loads an audio file with librosa and returns chroma features of shape (num_frames, 12).
    """
    y, sr = librosa.load(audio_path, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length)
    return chroma.T


def create_frame_labels(chroma, annotations, sr=22050, hop_length=512):
    """
    For each frame in chroma, determine which chord label applies based on annotations.
    Returns a list of chord labels (length = number of frames).
    """
    num_frames = chroma.shape[0]
    time_per_frame = hop_length / sr
    labels = ["N/A"] * num_frames

    for (start, end, chord) in annotations:
        start_idx = int(start / time_per_frame)
        end_idx = int(end / time_per_frame)
        # Clip to avoid out-of-range indices
        start_idx = max(0, start_idx)
        end_idx = min(num_frames, end_idx)
        for i in range(start_idx, end_idx):
            labels[i] = chord
    return labels


def build_chord_vocab(list_of_chord_lists):
    """
    Builds a vocabulary (dict) mapping chord strings to integer IDs.
    Example usage:
        chord_vocab = build_chord_vocab([all chord labels from all songs])
    """
    chord_set = set()
    for chord_list in list_of_chord_lists:
        chord_set.update(chord_list)
    # Sort for consistent ordering
    chord_vocab = {chord: i for i, chord in enumerate(sorted(chord_set))}
    return chord_vocab


def convert_chords_to_ids(chord_labels, chord_vocab):
    """
    Converts a list of chord labels into a list of integer IDs using chord_vocab.
    """
    return [chord_vocab[chord] for chord in chord_labels]


def chunk_data(chroma, chord_ids, seq_length=20):
    """
    Splits the frame-level data into smaller sequences for RNN training.
    X: (num_sequences, seq_length, 12)
    Y: (num_sequences,) single label per sequence
    """
    X, Y = [], []
    num_frames = len(chord_ids)
    for start_idx in range(num_frames - seq_length):
        end_idx = start_idx + seq_length
        X.append(chroma[start_idx:end_idx])
        # We use the chord at the last frame as the label. Adjust as needed.
        Y.append(chord_ids[end_idx - 1])
    return X, Y


def get_training_data(audio_dir, jams_dir):
    """
    Parses all audio (.wav) and matching .jams files in directories,
    aligns them, and returns the data ready for training.

    1. First loop: parse existing .jams files to collect chord labels (for vocab).
    2. Build chord vocab from all collected labels.
    3. Second loop: parse again, convert labels to IDs, and chunk into sequences.
    """
    all_X = []
    all_Y = []
    all_chord_lists = []

    # Helper function to compute the matching base name.
    def get_base_name(file_name):
        # Remove the ".wav" extension.
        base = file_name.replace(".wav", "")
        # Remove extra parts like "_mic" if present.
        base = base.replace("_mic", "")
        return base

    # =============== 1) FIRST LOOP: Build chord label lists for vocab ===============
    for file_name in os.listdir(audio_dir):
        if file_name.endswith(".wav"):
            audio_path = os.path.join(audio_dir, file_name)
            base = get_base_name(file_name)
            jams_name = base + ".jams"
            jams_path = os.path.join(jams_dir, jams_name)
            
            if not os.path.exists(jams_path):
                # print(f"[First Loop] Skipping {file_name} because {jams_path} doesn't exist.")
                continue
            # else:
            #     print(f"[First Loop] Processing {file_name} with {jams_path}")
            
            annotations = parse_jams_file(jams_path)
            chroma = extract_chroma(audio_path)
            chord_labels = create_frame_labels(chroma, annotations)
            all_chord_lists.append(chord_labels)

    # =============== 2) BUILD VOCAB ===============
    chord_vocab = build_chord_vocab(all_chord_lists)

    # =============== 3) SECOND LOOP: Convert to IDs and chunk data ===============
    for file_name in os.listdir(audio_dir):
        if file_name.endswith(".wav"):
            audio_path = os.path.join(audio_dir, file_name)
            base = get_base_name(file_name)
            jams_name = base + ".jams"
            jams_path = os.path.join(jams_dir, jams_name)
            
            if not os.path.exists(jams_path):
                # print(f"[Second Loop] Skipping {file_name} because {jams_path} doesn't exist.")
                continue
            # else:
            #     print(f"[Second Loop] Processing {file_name} with {jams_path}")
            
            annotations = parse_jams_file(jams_path)
            chroma = extract_chroma(audio_path)
            chord_labels = create_frame_labels(chroma, annotations)
            chord_ids = convert_chords_to_ids(chord_labels, chord_vocab)

            X_song, Y_song = chunk_data(chroma, chord_ids, seq_length=20)
            all_X.extend(X_song)
            all_Y.extend(Y_song)

    return all_X, all_Y, chord_vocab


if __name__ == "__main__":
    # For testing, define directories relative to this file
    this_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(this_dir, "RNN_Training_Dataset", "audio_files")
    jams_dir = os.path.join(this_dir, "RNN_Training_Dataset", "jams_files")

    X_all, Y_all, chord_vocab = get_training_data(audio_dir, jams_dir)
    print("Training data loaded:")
    print("Number of sequences:", len(X_all))
    print("Chord vocabulary:", chord_vocab)
