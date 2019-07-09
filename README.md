# Scale
**Scale** is a project I built when I was a Data Engineering Fellow at Insight Data Science. It focusses on finding similar songs based on the number of shared instruments in a song.

### Motivation
Everybody loves listening to new music. That has led to various kinds of Music Recommendation engines using different techniques like:
* **Collaborative Filtering**: based on user's listening behavior. This fails to recommend new and good songs.
* **Raw Audio Signal analysis**: Attempts to find good and new songs based on similar instruments. It's not a definitive analysis as same instruments could be present in 2 songs playing in different scale(pitch) and the analysis would fail to gauge the similarity.

These approaches fails to find equivalence that can readily gauged using MIDI files.

### Solution
I used MIDI files - a file format that was established in the 1980's. It's still a very popular file format now. It's used by musicians as it essentially is a digital version of music score. I used a dataset of MIDI files to find similar songs within that dataset.

![MIDI file](assets/MIDI_file.png?raw=true "MIDI File in Garage Band")
*MIDI file opened in Garage Band. Note the list of instruments shown on the left side.*

For every MIDI file, we can fetch the list of instruments used in a song. I used this list of instruments to gauge the similarity between songs - based on the number of shared instruments.

### Tech Stack
![Tech Stack](assets/Tech_Stack.png?raw=true "Tech Stack used in project")
*Tools used in this project*

### Similarity Score
The similarity score between a pair of songs is computed based on the number of shared instruments. The below picture elaborates on this using an example.

![Similarity SCore](assets/Similarity_Score.png?raw=true "Method of computing Similarity Score between a pair of songs")
*Method of computing Similarity Score between a pair of songs*
