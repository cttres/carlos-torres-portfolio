import os
import subprocess
import sys
import shutil


def isolate_guitar(input_file, base_output_dir="./test_audio"):
    """
    Runs Demucs on the input file and returns the path to the isolated 'other.wav' stem.
    After Demucs finishes, the isolated file is moved to:
        ../chords_recognition/wav_audio/{base_name}_other.wav
    relative to the current script location (track_separation folder).
    """
    # Extract the file's base name (e.g., "test_clip1" from "test_clip1.wav")
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Create a custom output directory for Demucs
    output_dir = os.path.join(base_output_dir, f"separated_{base_name}")
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs using the same Python interpreter as this script
    cmd = [
        sys.executable,
        "-m", "demucs",
        "--out", output_dir,
        input_file
    ]

    try:
        # Capture stdout/stderr for better UI error reporting
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        # Raise with full Demucs log for debugging
        raise RuntimeError(f"Demucs failed with exit code {e.returncode}:\n{e.stdout}") from e

    # Default folder structure used by Demucs:
    # ./test_audio/separated_{base_name}/htdemucs/{base_name}/other.wav
    model_folder = "htdemucs"
    demucs_output_path = os.path.join(output_dir, model_folder, base_name, "other.wav")

    if not os.path.exists(demucs_output_path):
        raise FileNotFoundError(f"Could not find 'other.wav' at {demucs_output_path}")

    # Move the isolated file into chords_recognition/wav_audio
    final_output_dir = os.path.join("..", "chords_recognition", "wav_audio")
    os.makedirs(final_output_dir, exist_ok=True)
    final_path = os.path.join(final_output_dir, f"{base_name}_other.wav")
    shutil.move(demucs_output_path, final_path)

    return final_path


if __name__ == "__main__":
    import sys as _sys
    if len(_sys.argv) < 2:
        print("Usage: python demucs_isolation.py <path_to_audio_file>")
        _sys.exit(1)

    test_audio = _sys.argv[1]
    print(f"Running Demucs on {test_audio}...")

    try:
        isolated_file = isolate_guitar(test_audio)
        print(f"Isolated guitar track saved at: {isolated_file}")
    except Exception as ex:
        print("Error:", ex)
