from flask import Flask, Response
app = Flask(__name__)
from picture import simulateDay, monoColor
from threading import Thread

run_simulation = False

@app.route('/')
def page():
  content = open('index.html').read()
  return Response(content, mimetype="text/html")
  
@app.route('/switch/<mode>')
def switchPicMode(mode):
  if (mode == 'quicksim'):
    # TODO: Cannot yet stop the simulation once started
    simulateDay(True)
  elif (mode == 'off'):
    monoColor('off')
  elif (mode == 'on'):
    monoColor('on')
  return 'switched mode: %s' % mode

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
