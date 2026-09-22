# Before running, set env variables:
# export FLASK_APP=UI.py
# export FLASK_DEBUG=1 for true, 0 for false
# [Navigate to bluefoot/src/UI_Integrations]
# flask run

# Now you can pull up localhost:5000 in your browser to view the webpage. Refresh to see changes.

# Note: DO NOT SET DEBUG MODE IF DEPLOYING PUBLICLY!!! ---------------------------------------------------
#   Debug mode allows for arbitrary code executions from the deployed site. log4j flashbacks...

# Disclaimer: A majority of this boilerplate was written alongside the YouTube tutorials by Corey Schafer

from flask import Flask, render_template, url_for, flash, request
from forms import registerform,Loginform
from turbo_flask import Turbo
from datetime import datetime, timedelta
from time import sleep
from flask_socketio import SocketIO, send, emit, join_room
import threading
from random import randint, randrange

app = Flask(__name__)

# WHEN DEPLOYING PUBLICLY, GENERATE A NEW ONE AND MAKE IT AN ENVIRONMENT VARIABLE OR SOMETHING INSTEAD,
#   OTHERWISE THIS KEY IS USELESS FOR PREVENTING SECURITY RISKS
app.config['SECRET_KEY'] = '1c54243c5e2a20c2fbcccee5f28ff349'
app.config['SESSION_ID'] = 'ChangeMeForSessionDifferentiation'
turbo = Turbo(app)
socketio = SocketIO(app)

def test_url(self):
    with app.app_context(), app.test_request_context():
        self.assertEqual('/', url_for('root.home'))


savestate = ["hi"]
sessions = set()

# Home page route
@app.route("/")
@app.route("/home")
@app.route("/index.html")
def home():
    return render_template("chungus.html", title='Chungus')


# smol page route
#@app.route("/smol", methods=['POST', 'GET'])
#def smol():
#    return render_template("smol.html", title='smol')


# Chungus page route
#@app.route("/chungus", methods=['POST', 'GET'])
#def chungus():
#    if request.method == 'POST':
#        # Handle scroll action request (SocketIO)
#        if 'scroll-action' in request.form.keys():
#            tokens = request.form['scroll-action'].split()
#            print("Scroll Action POST received: " + str(tokens))
#
#            # TODO: Change broadcast to a named group when sessions are implemented
#            socketio.emit('pdf-scroll-event', tokens, broadcast=True)
#    return render_template("chungus.html", title='Chungus')

#login page route
@app.route("/login")
def login():
    form = Loginform()
    return render_template("login.html", title='login',form = form)

@app.route("/register")
def register():
    form = registerform()
    return render_template("register.html", title='Register',form = form)

@app.route("/start")
def start():
    num = randint(100, 999) # randint is inclusive at both ends
    data = {'code' : str(num), 'user_in' : 1}
    return render_template("start.html", data=data)


#################################### SocketIO handlers #########################################

@socketio.on("message")
def handle_msg(msg):
    print('Msg: ' + msg)
    send(msg, broadcast=True) # broadcast off to respond to sender only instead

    #------------------------------- FROM SMOL --------------------------------------------------
@socketio.on("smol-ready")
def handle_smol_ready(session_id):
    print("smol: User has connected.")

    if session_id not in sessions:
        sessions.add(session_id)
    join_room(session_id)
    emit("smol-init")

@socketio.on("request-change-preset")
def handle_change_preset(session_id, p):
    # print(str(session_id) + " " + str(p))
    preset_name = "display_presets/preset_" + str(p) + ".html"
    emit("change-preset", {'p': p, 'elem': render_template(preset_name)}, to=session_id)

@socketio.on("smol-request-template")
def handle_smol_request_template(session_id, id, button_type):
    col = id[-3]
    row = id[-1]
    template = None
    if button_type == 'PDF':
        template = render_template("display_presets/sample_pdf.html")
    elif button_type == 'Calendar':
        template = render_template("display_presets/calendar.html")
    elif button_type == 'Spotify Pause/Play':
        template = render_template("display_presets/spotify.html")
    elif button_type == 'Discord':
        template = render_template("display_presets/discord.html")

    emit('chungus-template-response', {'content': template, 'type': button_type, 'row': row, 'col': col}, to=session_id)

@socketio.on("smol-request-pdf")
def handle_smol_request_pdf(session_id, file_URL, c, r):
    emit('chungus-handle-pdf', {'fileURL': file_URL, 'col': c, 'row': r}, to=session_id)

    #-----------------------------FROM CHUNGUS -------------------------------------------
@socketio.on("chungus-ready")
def handle_chungus_ready(session_id):
    print("Chungus: User has connected.")
    while session_id not in sessions:
        print("Chungus: smol not found")
        sleep(1)
    print("Chungus: smol found")
    join_room(session_id)
    emit("chungus-init", render_template("display_presets/preset_1.html"), to=session_id)

@socketio.on("chungus-request-template")
def handle_template_request(msg):
    print("Message: " + str(msg))
    response = render_template("display_presets/" + msg['uri'])
    emit("chungus-template-response", {'content': response, 'type':msg['type'], 'row': msg['row'], 'col': msg['col']}, to=msg['session_id'])

@socketio.on("smol-create-panel")
def handle_smol_create_panel(session_id, preset, presets):
    rows = [len(col) for col in presets[str(preset)]]
    print(rows)
    emit("create-smol-panel", {'rows': rows, 'template': render_template("display_presets/choose.html")}, to=session_id)

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app)

    