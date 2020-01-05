from itertools import imap, ifilter


class BKTree:
    def __init__(self, distfn, words):

        self.distfn = distfn

        it = iter(words)
        root = it.next()
        self.tree = (root, {})

        for i in it:
            self._add_word(self.tree, i)

    def _add_word(self, parent, word):
        pword, children = parent
        d = self.distfn(word, pword)
        if d in children:
            self._add_word(children[d], word)
        else:
            children[d] = (word, {})

    def query(self, word, n):
        def rec(parent):
            pword, children = parent
            d = self.distfn(word, pword)
            results = []
            if d <= n:
                results.append( (d, pword) )
                
            for i in range(d-n, d+n+1):
                child = children.get(i)
                if child is not None:
                    results.extend(rec(child))
            return results

        # sort by distance
        return sorted(rec(self.tree))
    


def brute_query(word, words, distfn, n):

    return [i for i in words
            if distfn(i, word) <= n]


def maxdepth(tree, count=0):
    _, children = t
    if len(children):
        return max(maxdepth(i, c+1) for i in children.values())
    else:
        return c


def levenshtein(s, t):
    m, n = len(s), len(t)
    d = [range(n+1)]
    d += [[i] for i in range(1,m+1)]
    for i in range(0,m):
        for j in range(0,n):
            cost = 1
            if s[i] == t[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, # deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
    return d[m][n]


def dict_words(dictfile="aymara"):

    return ifilter(len,
                   imap(str.strip,
                        open(dictfile)))


def timeof(fn, *args):
    import time
    t = time.time()
    res = fn(*args)
    print ("time: ", (time.time() - t))
    return res



if __name__ == "__main__":

    tree = BKTree(levenshtein,
                  dict_words('aymara'))

    print (tree.query("Achu", 0))
    
