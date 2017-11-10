"""Flask webapp to sort Russian words by frequency."""
from collections import defaultdict as dd

from flask import Flask
from flask import request
from flask import render_template

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
        ambigs = []
        with open(path) as freq_file:
            for line in freq_file:
                rank, freq, lemma, pos = line.split()
                freq = float(freq)
                if lemma in self.freq:
                    ambigs.append(lemma)
                self.freq[lemma] = freq
                self.freq_w_rank_and_pos[lemma] = (freq, rank, pos)
                try:
                    self.ambig_freq[lemma].append((freq, rank, pos))
                except AttributeError:
                    self.ambig_freq[lemma] = [(freq, rank, pos)]
            print('WARNING: the following lemma names are ambiguous. Using '
                  'the ambig_freq dictionary is highly recommended:',
                  list(sorted(set(ambigs))))


lem = Sharoff_lem_freq()  # lem.freq is a dict: lem.freq[<lemma>]


@app.route('/')  # passenger sets '/' to be the path registered in cPanel
def freq_form():
    """Start page."""
    return render_template("freq_form.html")


@app.route('/', methods=['POST'])
def freq_form_post():
    """POST script."""
    return '\n'.join([w + '\t' + str(lem.freq[w]) for w in request.form['text'].split()])  # noqa


if __name__ == "__main__":
    app.debug = True
    app.run()
