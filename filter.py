import flask
from flask import Flask, render_template, request
app = Flask(__name__, static_path="/static")

import json
import os
import os.path
from PIL import Image
from pprint import pprint

# one or more directories
MAKO_DIR = 'templates'
## optional, if specified Mako will cache to this directory
#MAKO_CACHEDIR = '/tmp/mako'
## optional, if specified Mako will respect the cache size
#MAKO_CACHESIZE = 500

dir_ = "/home/spiffytech/Dropbox/IFTTT/reddit/EarthPorn"
savedir = "/home/spiffytech/Dropbox/IFTTT/reddit/earthporn_filtered"
imgdir = "static/images"
try:
    os.unlink(imgdir)
except:
    pass
os.symlink(dir_, imgdir)

@app.route("/")
def index():
    files = os.listdir(imgdir)
    to_delete = filter(lambda f: get_img_size(os.path.join(dir_, f))[0] < 1024 and get_img_size(os.path.join(dir_, f))[1] < 768, files)
    #pprint([(get_img_size(os.path.join(dir_, f)), f) for f in to_delete])
    map(os.remove, (os.path.join(imgdir, f) for f in to_delete))

    files = os.listdir(imgdir)
    files = flask.Markup(json.dumps(files))
    return render_template("index.html", files=files)

@app.route("/delete")
def delete():
    file_ = os.path.join(imgdir, request.args.get("file"))
    os.remove(file_)
    return "success"

@app.route("/save")
def save():
    file_ = os.path.join(imgdir, request.args.get("file"))
    savedfile = os.path.join(savedir, request.args.get("file"))
    os.rename(file_, savedfile)
    return "success"

def get_img_size(file_):
    try:
        img=Image.open(file_)
        return img.size  # (width,height) tuple
    except IOError:
        return (0,0)

if __name__ == "__main__":
    app.debug = True
    app.run()
