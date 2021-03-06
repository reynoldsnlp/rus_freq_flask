"""Flask webapp to sort Russian words by frequency."""
from collections import defaultdict as dd
import sys

from flask import Flask
from flask import request
from flask import render_template
# from flask import url_for

app = Flask(__name__)
application = app  # our hosting requires `application` in passenger_wsgi


def absent():
    """Used as default in defaultdict's."""
    return 0


class Sharoff_lem_freq:
    """Lemma freq data from Serge Sharoff.

    Taken from: http://www.artint.ru/projects/frqlist/frqlist-en.php
    """

    def __init__(self, path='Sharoff_lemmaFreq.txt'):
        """Initialize frequency dictionary."""
        self.freq = dd(absent)
        self.freq_w_rank_and_pos = dd(absent)
        self.ambig_freq = dd(absent)
        self.ambigs = []
        with open(path) as freq_file:
            for line in freq_file:
                rank, freq, lemma, pos = line.split()
                freq = float(freq)
                if lemma in self.freq:
                    self.ambigs.append(lemma)
                self.freq[lemma] = freq
                self.freq_w_rank_and_pos[lemma] = (freq, rank, pos)
                try:
                    self.ambig_freq[lemma].append((freq, rank, pos))
                except AttributeError:
                    self.ambig_freq[lemma] = [(freq, rank, pos)]
            print('WARNING: the following lemma names are ambiguous. Using '
                  'the ambig_freq dictionary is highly recommended:',
                  list(sorted(set(self.ambigs))), file=sys.stderr)


lem = Sharoff_lem_freq()  # lem.freq is a dict: lem.freq[<lemma>]


# @app.route('/')
# def freq_form():
#     """Start page."""
#     return render_template("freq_form.html")

# passenger sets '/' to be the path registered in cPanel
@app.route('/', methods=['GET', 'POST'])
def freq_form_post():
    """Build Russian frequency sorter page."""
    if request.method == 'GET':
        return render_template("freq_form.html")
    elif request.method == 'POST':
        wordlist = [(w.lower(), str(lem.freq[w.lower().replace('\u0301', '')]))
                    for w in request.form['text'].split()]
        html = ''.join(['<tr class="item"><td>{}</td><td>{}</td></tr>'.format(w, f)
                        for w, f in
                        sorted(wordlist, key=lambda x: float(x[1]),
                               reverse=True)])
        return render_template('freq_output.html', table=html)


if __name__ == "__main__":
    app.debug = True
    app.run()
