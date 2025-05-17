from flask import Flask, request
from core import Key, KeyEvent, play_note, change_synth #TODO: Add library.
import asyncio
app = Flask(__name__)

change_synth("module90.sf2")

buffer = [Key("C")]

@app.route("/store-note", methods = ["POST"])
def store_note():
    if request.method == "POST":
        #data = request.form
        data = request.form.getlist("notedata")
        [buffer.append(Key(note)) for note in data]
    return "200"
        

@app.route("/execute-buffer", methods = ["GET"])
def execute_buffer():
    ke = KeyEvent(buffer)
    asyncio.run(play_note(ke)) # TODO: streaming audio from API.
    return "200"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = True)