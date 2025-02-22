tone_dictionary = {"C" : 60, "D" : 62, "E" : 64, "F" : 65, "G" : 67, "A" : 69, "B" : 71, "#" : 1, "4" : 0, "3" : -12, "2" : -24, "1" : -36, "0" : -48}

class Key:
    def __init__(self, key : str):
        self.key = key
    def __str__(self):
        return self.key
    def __float__(self):
        return float(tone_dictionary[self.key])

""" Reference
# Play some notes (middle C, E, G).
synthesizer.note_on(0, 60, 100)
synthesizer.note_on(0, 64, 100)
synthesizer.note_on(0, 67, 100)
"""

class KeyEvent:
    def __init__(self, keys : list):
        self.tones = []
        for key in keys:
            tone = 0
            for element in str(key):
                tone += tone_dictionary[element]
            self.tones.append(tone)
        
    def __len__(self):
        return len(self.tones)
            
    def __str__(self):
        return f"Tones for KeyEvent: {self.tones}"
    
    def __getitem__(self,index):
        return float(self.tones[index])