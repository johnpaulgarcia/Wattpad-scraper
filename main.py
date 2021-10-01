import tempfile
import flask
import os
from wattpad_scraper import get_story, parse_soup
from flask import request, render_template, send_file
from flask_sock import Sock

app = flask.Flask(__name__)
sock = Sock(app)

@sock.route('/download-txt')
def download_txt(ws):
    while True:
        try:
            url = ws.receive()
            soup = parse_soup(url)
            title, story = get_story(url, soup)
            with tempfile.NamedTemporaryFile('w', encoding='utf8', delete=False) as temp:
                temp.writelines(story)
                temp.flush()
                temp.close()
            ws.send(story)
            #ws.send(temp.name,as_attachment=True,mimetype='text/plain;charset=UTF-8',attachment_filename=title + ".txt")

        except Exception as e: print(e)




@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port, debug=True)
