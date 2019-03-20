import postgresql
import pyaudio
import wave
import db_query


def error_log(module_name, error_message):
    db = postgresql.open(db_query.connection_string())
    print('Error:' + error_message)
    insert = db.prepare("insert into error_log (module_name, error_message) values($1,$2)")
    insert(module_name, str(error_message))
    play_alarm_sound()


def play_alarm_sound():
    return
    chunk = 1024
    f = wave.open("C:/OSPanel/domains/screenshot/ALERT.wav", "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk)
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
