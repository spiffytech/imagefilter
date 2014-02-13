import flask
from flask import Flask, render_template, request
app = Flask(__name__, static_path="/static")

import json
import os
import os.path

# one or more directories
MAKO_DIR = 'templates'
## optional, if specified Mako will cache to this directory
#MAKO_CACHEDIR = '/tmp/mako'
## optional, if specified Mako will respect the cache size
#MAKO_CACHESIZE = 500

dir_ = "/home/spiffytech/Dropbox/IFTTT/reddit/EarthPorn"
imgdir = "static/images"
try:
    os.unlink(imgdir)
except:
    pass
os.symlink(dir_, imgdir)

@app.route("/")
def index():
    files = os.listdir(imgdir)
    files = flask.Markup(json.dumps(files))
    return render_template("index.html", files=files)

@app.route("/delete")
def delete():
    file_ = os.path.join(imgdir, request.args.get("file"))
    os.remove(file_)
    return "success"

if __name__ == "__main__":
    app.debug = True
    app.run()
