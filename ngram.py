class NGram:

    def __init__(self):
        self._get_model()

    def _get_model(self):
        import gzip
        import pickle

        with gzip.open('model.pkl.gz', 'rb') as f:
            self._model = pickle.loads(f.read())
    
    def _get_most_likely(self, word, dic, n):
        l = list(self._model[dic][word].items())
        l.sort(key=(lambda x: x[-1]), reverse=True)
        return l[:n]

    def _refine(self, txt, s, ngrams):
        s = list(filter(
            (lambda x: x[0] not in txt[-ngrams:]),
            s
        ))

        return s

    def suggest_word(self, txt, size=1, ngrams=5):
        most_likely = []
        
        for i in range(2, ngrams+1):
            words = ' '.join(txt[-(i-1):])
            try:
                ml = self._get_most_likely(words, i, n=ngrams+1)
                most_likely.extend(ml)
            except:
                pass
        
        most_likely.sort(key=(lambda x: x[-1]), reverse=True)
        most_likely = self._refine(txt, most_likely, ngrams)

        l = [ x[0] for x in most_likely[:size] ]
        
        return(l)

    def gen_text(self, seed, size):
        txt = seed.split()

        for _ in range(size):
            n = self.suggest_word(txt, size=3)
            txt.append(n[0])
        
        return ' '.join(txt)