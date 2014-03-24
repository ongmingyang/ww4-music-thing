import queueHandler as qh
import os, ConfigParser
from subprocess import check_output
from flask import Flask, flash, request, redirect, url_for, render_template
from flask.ext.login import LoginManager, login_required, login_user, logout_user, UserMixin
from werkzeug.utils import secure_filename

config = ConfigParser.ConfigParser()
config.read("config")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.get("pathvars", "uploads")
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.config['TEMPLATE_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = config.get("secretvars", "key")

class User(UserMixin):
  def __init__(self, name, id, active=True):
    self.name = name
    self.id = id

  def verify_password(self, password):
    try:
      correct_password = config.get("shadow", self.name)
      valid = (correct_password == password)
    except:
      valid = False
    return valid

@login_manager.user_loader
def load_user(username):
  return User(username, qh.randomhash().strip())

@login_manager.unauthorized_handler
def unauthorized():
    flash("You're not exactly authorised, please request a username and password from Ming Yang")
    return redirect(url_for("login"))

@app.route("/roomentry", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    user = load_user(request.form['username'])
    if user.verify_password(request.form['password']):
      login_user(user)
      flash("Logged in successfully.")
      return redirect(url_for("upload_file"))
    else:
      flash("Login failed")
  return render_template("login.html")

@app.route("/roomexit")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out!")
    return redirect(url_for("login"))

@app.route('/room405', methods=['GET', 'POST'])
@login_required
def upload_file():
  currentPlaying = check_output(["cmus-remote", "-Q"]).decode('utf-8').split('\n')
  currentFile = qh.parseFilename(currentPlaying)
  if request.method == 'POST':
    file = request.files['file']
    if file and qh.allowedFile(file.filename):
      try:
        filename = qh.randomhash().strip()+secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        check_output(["cmus-remote", "-q", filepath])
        currentQueue = qh.appendAndPop(filepath, currentFile)
        flash("Successfully pushed " + filename + " to queue!")
      except:
        flash('There was an error with the upload, please try again!')
        return redirect(url_for('upload_file'))
  elif request.method == 'GET':
    filename = None
    currentQueue = qh.popFromQueue(currentFile)
  return render_template("template.html", currentPlaying = currentPlaying, currentQueue = currentQueue).encode('utf-8')

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=80)
