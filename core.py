from symusic import Score, Note, Track, Synthesizer, BuiltInSF3, dump_wav
'''@inproceedings{symusic2024,
    title={symusic: A swift and unified toolkit for symbolic music processing},
    author={Yikai Liao, Zhongqi Luo, et al.},
    booktitle={Extended Abstracts for the Late-Breaking Demo Session of the 25th International Society for Music Information Retrieval Conference},
    year={2024},
    url={https://ismir2024program.ismir.net/lbd_426.html#lbd},
}'''

import numpy as np
from event import Key, KeyEvent
from playsound import playsound

sf_path = ""
if sf_path == None or sf_path == "":
    sf_path = BuiltInSF3.MuseScoreGeneral().path(download=True)
synth = Synthesizer(sf_path = sf_path,sample_rate=44100)
print("Startup Complete")

def change_synth(sf_path : str, sr=44100):
    global synth
    synth = Synthesizer(sf_path = sf_path,sample_rate=sr)
    print("Synth Changed")

def play_note(keyevent : KeyEvent, time_val = 100, duration_val = 100, velocity_val = 60):
    
    sequence_length = len(keyevent)

    time_list = [time_val for _ in range(sequence_length)]
    duration_list = [duration_val for _ in range(sequence_length)]
    pitch_list = [keyevent[i] for i in range(sequence_length)]
    velocity_list = [velocity_val for _ in range(sequence_length)]

    # Scores are made from a 2D Numpy Array

    # Looking at the output of `print(score.tracks[0].notes.numpy())`:
    # First channel: time
    # Second channel: duration
    # Third channel: pitch
    # Fourth channel: velocity

    time_channel = np.array(time_list)
    duration_channel = np.array(duration_list)
    pitch_channel = np.array(pitch_list)
    velocity_channel = np.array(velocity_list)
    score_noncompiled = Note.from_numpy(time=time_channel,duration=duration_channel,pitch=pitch_channel,velocity=velocity_channel)

    score = Score()
    track = score.tracks.append(Track(notes=score_noncompiled))

    print(score)

    audio = synth.render(score)
    dump_wav("out.wav", audio, sample_rate=44100, use_int16=True)
    playsound("out.wav")