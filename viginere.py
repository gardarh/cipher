import string
import collections
import fractions
import operator

def main():
    tst_plaintext = 'ATTACKATDAWN'
    tst_key = 'SALMON'
    tst_cipher = viginere_cipher(tst_plaintext, tst_key, 'encipher')
    if tst_plaintext != viginere_cipher(tst_cipher, tst_key, 'decipher'):
        raise ValueError("deciphering enciphered does not give plaintext!")

    cipher = open('cipher_viginere','r').read().strip()
    # find longest repeated string
    found_words = collections.defaultdict(set)
    cipherlen = len(cipher)
    testcount = 0
    for trial in xrange(cipherlen-10, cipherlen):
        #print "**** TRIAL %d ****" % (trial,)
        strlen = cipherlen - trial
        for startpos in xrange(cipherlen - strlen + 1):
            test_str = cipher[startpos:startpos+strlen]
            offset = 0
            find_count = 0
            findpos = -1
            while True:
                findpos = cipher.find(test_str, findpos+1)
                testcount +=1
                if findpos == -1:
                    break
                find_count += 1
            if find_count > 1 and strlen > 3:
                found_words[strlen].add(test_str)

    alldiffs = set()
    for wordlen in found_words.keys():
        for word in found_words[wordlen]:
            findpos = -1
            positions = []
            while True:
                findpos = cipher.find(word, findpos+1)
                if findpos > -1:
                    positions.append(findpos)
                else:
                    break
            if positions < 2:
                print "weird, found less than 2 pos"
                continue
            posdiffs = [positions[i+1] - positions[i] for i in xrange(len(positions)-1)]
            alldiffs = alldiffs.union(posdiffs)
            # print "Word %s, numpos: %d, posdiffs: %s" % (word, len(positions), ', '.join(str(posdiff) for posdiff in posdiffs))
    print "Positions disparity between common words:",sorted(alldiffs)
    gcd = min(alldiffs)
    for diff in alldiffs:
        gcd = fractions.gcd(gcd, diff)

    print '**** GUESSING CODEWORD LENGTH %d ****' % (gcd,)

    alphabets = collections.defaultdict(list)
    for i,ch in enumerate(cipher):
        alphabets[i%gcd].append(ch)

    freq_analyses = {}
    for i,alphabet in alphabets.iteritems():
        freq_analyses[i] = frequency_analysis(alphabet)

    codeword = ''
    for i,freq in freq_analyses.iteritems():
        sorted_c = sorted(freq.items(), key=operator.itemgetter(1))
        #print "** FREQ FOR ALPHABET %d **" % (i,)
        #print '; '.join(["%s (%d)" % (item[0], item[1]) for item in sorted_c])
        # Guess E is always most common
        most_common_c = sorted_c[-1][0]
        print 'Guessing offset %d (%s is E)' % (ord(most_common_c) - ord('E'), most_common_c)
        
        codeword += chr(ord('A') + (ord(most_common_c) - ord('E')) % 26)

    print "*** CODEWORD: %s ***" % (codeword,)

    print '*** RESULT: ***'
    print viginere_cipher(cipher, codeword, 'decipher')


def frequency_analysis(text):
    freqs = collections.defaultdict(int)
    for ch in text:
        freqs[ch] += 1
    return dict(freqs)

def viginere_cipher(plaintext, key, direction):
    """
    direction should be "encipher" or "decipher"
    """
    if direction not in ('encipher','decipher'):
        raise ValueError('direction should be "encipher" or "decipher"')

    out = []
    for i, plainsymbol in enumerate(plaintext):
        alphabet_offset = ord(key[i%len(key)].upper()) - ord('A')
        d = collections.deque(list(string.ascii_uppercase))
        d.rotate(alphabet_offset * -1 if direction == 'encipher' else alphabet_offset)
        #print "offset for %i (key: %s): %d, first char: %s" % (i, key, alphabet_offset, d[0])
        plainsymbol_offset = ord(plainsymbol.upper()) - ord('A')
        out.append(d[plainsymbol_offset])
    return ''.join(out)

if __name__ == "__main__":
    main()
