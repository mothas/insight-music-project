# Music Recommendation using music-elements


## Use Case
This project enables us to compare and match songs purely based on their musical features, as opposed to audio-signal elements. It creates a new pipeline consisting purely of musical features. This pipeline is fed to a ML model to figure out the best features to use. The ML part is NOT in the scope of this project. This project explores in how to extract useful musical features from MIDI files.

## Motivation
Spotify's current raw audio-signal analysis is a step in the right direction to analyze new and unpopular songs. But it fails to match songs in a musical realm. They are missing out on recommending songs that are very relevant and already in their library.

Raw analysis reveals only a few musical traits.

## Solution
MIDI files to the rescue! They allow us to analyze music is the realm of music - as opposed to audio signal realm.

The richer musical traits that are available from MIDI files are:
* Notes
* Chords
* Key signature
* Rhythm
* Note progression
* Chord progression
* Time signature

## Tech Stack
* AWS S3
* Spark
* Flask

## Project Scope
### In scope
* Build a new method to analyze music
* Enables ML engineers to improve recommendation

### NOT in scope
* Figure out the best musical features to compare songs
  * Could be chord progression OR rhythm progression
  * It is purely a ML task
