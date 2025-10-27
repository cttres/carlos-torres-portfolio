# GuitR-AI
Real Time Guitar Chord Recognition And Learning Assistant

## Overview
GuitR-AI is an application that leverages artificial intelligence to recognize acoustic guitar chords from audio recordings in real time. It isolates the guitar stem using the Demucs library and performs chord recognition with madmom’s library, then displays the detected chords along with fingering diagrams to assist users in learning.

## Features
  - Guitar Stem Isolation: Separate guitar from full-mix audio using Demucs.
  - Chord Recognition: Analyze isolated guitar stem with madmom to detect chord progressions.
  - Real-Time Display: Visualize chords synchronized with playback.
  - Learning Center: Provide fretboard diagrams, popular strumming patterns, and chord shapes.
  - Key & Capo Suggestions: Identify song key to help estimate capo placement.

## Installation
  1) Download the zip file or clone the repository using git clone "the_repository_link"
  2) Install dependencies
  3) Run using python main.py

## Dependencies
  - Demucs
  - madmom
  - Python 3.7+
  - numpy, scipy, torch, soundfile, matplotlib

## Usage
  1) Drop an audio file containing acoustic guitar into the isolation part.
  2) Download the isolated guitar stem audio file.
  3) Drop the isolated guitar audio file into the recognition algorithm.
  4) Play the guitar following the chords and times being displayed.

## Third-Party Licenses
  - Demucs: Licensed under the MIT License.
  - madmom: Source code under 3‑clause BSD; data/models under CC BY‑NC‑SA 4.0.
Please refer to each project’s repository for full license texts.

## Acknowledgements
Team Members:

  - Carlos Torres (cttres@nmsu.edu)
  - Mingfang Zhu (lisazhu@nmsu.edu)
  - Edward Rivota (rivota@nmsu.edu)
  - Erick Lopez (elopez17@nmsu.edu)

Faculty Mentor: 
  - Bill Hamilton

Libraries: 
  - Demucs, madmom

## References
- Böck, S., Korzeniowski, F., Schlüter, J., Krebs, F., & Widmer, G. (2016). _madmom: A new Python audio and music signal processing library_. ACM International Conference on Multimedia. 
- Rouard, S., Massa, F., & Défossez, A. (2023). _Hybrid Transformers for Music Source Separation_. ICASSP. 
- Défossez, A. (2021). _Hybrid Spectrogram and Waveform Source Separation_. ISMIR Workshop on Music Source Separation.

Contributed to the original project at lisazhuuu/GuitR-AI. This fork includes my contributions.
