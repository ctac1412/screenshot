import postgresql
import db_conf
import pyaudio
import wave

def errorLog(module_name, error_message):
    error_message = (error_message[:250] + '..') if len(error_message) > 250 else error_message
    db = postgresql.open(db_conf.connectionString())
    insert = db.prepare("insert into error_log (module_name,error_message) values($1,$2)")
    insert(module_name, str(error_message))
    playAlarmSound()

def playAlarmSound():
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