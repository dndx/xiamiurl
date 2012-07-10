#coding: utf-8
import os
import time
import urllib2
import flask
from bs4 import BeautifulSoup

def xiami_decode(s):
    s = s.strip()
    if not s:
        return False
    result = []
    line = int(s[0])
    rows = len(s[1:]) / line
    extra = len(s[1:]) % line
    s = s[1:]
    
    for x in xrange(extra):
        result.append(s[(rows + 1) * x:(rows + 1) * (x + 1)])
    
    for x in xrange(line - extra):
        result.append(s[(rows + 1) * extra + (rows * x):(rows + 1) * extra + (rows * x) + rows])
    
    url = ''
    
    for x in xrange(rows + 1):
        for y in xrange(line):
            try:
                url += result[y][x]
            except IndexError:
                continue
    
    url = urllib2.unquote(url)
    url = url.replace('^', '0')
    return url

app = flask.Flask(__name__)
app.debug = not 'SERVER_SOFTWARE' in os.environ

@app.before_request
def record_start_time():
    flask.g.start_time = time.time()

@app.context_processor
def inject_render_time():
    return dict(render_time=time.time() - flask.g.start_time)

@app.route('/')
def index():
    return flask.render_template('index.html') 

@app.route('/song/<int:songid>')
def song(songid):
    url = 'http://www.xiami.com/widget/xml-single/uid/0/sid/%s' % songid
    content = urllib2.urlopen(url, timeout=5).read()
    xml = BeautifulSoup(content)
    result = {}
    result['url'] = xiami_decode(xml.track.location.string)
    result['song'] = xml.track.song_name.string
    result['album'] = xml.track.album_name.string
    result['album_img'] = xml.track.album_cover.string
    result['artist'] = xml.track.artist_name.string
    return flask.render_template('index.html', result=[result, ])

@app.route('/album/<int:albumid>')
def album(albumid):
    url = 'http://www.xiami.com/song/playlist/id/%s/type/1' % albumid
    content = urllib2.urlopen(url, timeout=5).read()
    xml = BeautifulSoup(content)
    result = []
    songs = xml.tracklist.find_all('track')
    for x in songs:
        result.append(dict(url=xiami_decode(x.location.string), song=x.title.string, album=x.album_name.string, album_img=x.pic.string, artist=x.artist.string))
    return flask.render_template('index.html', result=result)

@app.route('/collect/<int:collectid>')
def collect(collectid):
    url = 'http://www.xiami.com/song/playlist/id/%s/type/3' % collectid
    content = urllib2.urlopen(url, timeout=5).read()
    xml = BeautifulSoup(content)
    result = []
    songs = xml.tracklist.find_all('track')
    for x in songs:
        result.append(dict(url=xiami_decode(x.location.string), song=x.title.string, album=x.album_name.string, album_img=x.pic.string, artist=x.artist.string))
    return flask.render_template('index.html', result=result)

if __name__ == '__main__':
    app.run()
