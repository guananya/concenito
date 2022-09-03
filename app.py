from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

PEOPLE_FOLDER = os.path.join('static', 'sheet_music')

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
index = -1

ind = 0

tot_files = 0

@app.route('/', methods= ['GET', 'POST'])
def get_message():
    # if request.method == "GET":
    print("Got request in main function")
    for f in os.listdir(PEOPLE_FOLDER):
        os.remove(os.path.join(PEOPLE_FOLDER, f))
    #index += 1
    #ind += 1
    return render_template("index.html", count=index+1)

@app.route('/upload_static_file', methods=['POST'])
def upload_static_file():
    global index
    index += 1
    print("Got request in static files")
    print(request.files)
    f = request.files['static_file']
    f.save(os.path.join(PEOPLE_FOLDER, str(str(index) + '.png')))
    resp = {"success": True, "response": "file saved!"}
    return jsonify(resp), 200

@app.route('/sheets_uploaded', methods=['POST'])
def uploaded():
    return render_template('files.html', count=len(os.listdir(PEOPLE_FOLDER)))

@app.route('/files_page', methods=['POST'])
def files_page():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '0.png')
    global tot_files 
    tot_files = len(os.listdir(PEOPLE_FOLDER))
    global index
    index = -1
    global ind
    ind = 0
    return render_template('page.html', source=full_filename)
           

@app.route('/messages', methods = ['POST'])
def api_message():
    f = open('./file.wav', 'wb')
    f.write(request.data)
    f.close()
    
    return "saved"

@app.route('/predict', methods = ['POST'])
def predict(): 
    AUDIO_FILE = ("/Users/ananyagupta/Downloads/closerest/file.wav")

    # use the audio file as the audio source

    r = sr.Recognizer()
    
    result = ""
        
    try:
        with sr.AudioFile(AUDIO_FILE) as source:
                #reads the audio file. Here we use record instead of
                #listen
            audio = r.record(source) 
        print("in messages")
        try:
            global ind
            global tot_files
            result =  r.recognize_google(audio)
            if ind + 1 < tot_files:
                print(ind, "lesser than", tot_files)
                if "swipe" in result or "wipe" in result or "pipe" in result or "sweet" in result or "site" in result or "Skype" in result or "Swift" in result:
                    ind += 1
                elif "back" in result or "tack" in result or "lack" in result:
                    ind = ind - 1
            print("The audio file contains: " + result)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
    except:
        print("not done")
    
    print("done")
        
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], str(str(ind) + '.png'))
    
    #resp = {"success": True, "response": result}
    #return jsonify(resp), 200
    
    #if cachestat:
     #   return render_template('page.html', cachestat=cachestat, result=result, source=full_filename)
    #else:
    return render_template('page.html', result="Page " + str(ind+1) + " of " + str(tot_files) , source=full_filename)


if __name__ == '__main__':
    app.run(debug=True)