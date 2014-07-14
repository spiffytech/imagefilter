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

hstore = "choice_history.json"
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
    to_delete = filter(lambda f: get_img_size(os.path.join(dir_, f))[0] < 1280 or get_img_size(os.path.join(dir_, f))[1] < 720, files)
    map(os.remove, (os.path.join(imgdir, f) for f in to_delete))

    files = os.listdir(imgdir)
    files = flask.Markup(json.dumps(files))
    return render_template("index.html", files=files)

@app.route("/delete")
def delete():
    file_ = os.path.join(imgdir, request.args.get("file"))
    import time
    t1 = time.time()
    hash_ = dhash(Image.open(file_))
    store_hash(hash_, False)
    print time.time() - t1
    print hash_
    os.remove(file_)
    return "success"

@app.route("/save")
def save():
    file_ = os.path.join(imgdir, request.args.get("file"))
    hash_ = dhash(Image.open(file_))
    store_hash(hash_, True)
    savedfile = os.path.join(savedir, request.args.get("file"))
    os.rename(file_, savedfile)
    return "success"

@app.route("/check_hash")
def check_hash():
    file_ = os.path.join(imgdir, request.args.get("file"))
    hash_ = dhash(Image.open(file_))
    return str(read_hash(hash_))

def read_hash(hash_):
    with open(hstore) as f:
        j = json.load(f)
        if hash_ in j[dir_]:
            return j[dir_][hash_]
        else:
            return None

def store_hash(hash_, b):
    with open(hstore, "rw") as f:
        try:
            j = json.load(f)
        except ValueError:
            j = {}

    if not dir_ in j:
        j[dir_] = {}
    j[dir_][hash_] = b

    with open(hstore, "w") as f:
        json.dump(j, f)

def get_img_size(file_):
    try:
        img=Image.open(file_)
        return img.size  # (width,height) tuple
    except IOError:
        return (0,0)

def dhash(image, hash_size = 16):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = list(image.getdata())

    # Compare adjacent pixels.
    difference = []
    for row in xrange(hash_size):
        for col in xrange(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

if __name__ == "__main__":
    store_hash("bogus", False)
    app.debug = True
    app.run()
