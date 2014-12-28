import collections
import operator
import re
import string
#[('S', 1), ('E', 2), ('D', 2), ('F', 5), ('Q', 6), ('U', 6), ('L', 7), ('H', 8), ('I', 9), ('A', 11), ('Y', 11), ('W', 13), ('G', 17), ('N', 20), ('V', 22), ('B', 27), ('R', 36), ('C', 37), ('T', 40), ('P', 42), ('M', 44), ('J', 49), ('X', 56), (' ', 106)]
# initial
#ALPH = {'A':'A', 'B':'B', 'C':'C', 'D':'C', 'E':'E', 'F':'F', 'G':'G', 'H':'H', 'I':'I', 'J':'J', 'K':'K', 'L':'L', 'M':'M', 'N':'N', 'O':'O', 'P':'P', 'Q':'Q', 'R':'R', 'S':'S', 'T':'T', 'U':'U', 'V':'V', 'W':'W', 'X':'X', 'Y':'Y', 'Z':'Z',' ':' '}

ALPH = {'A':'c', 'B':'i', 'C':'o', 'D':'v', 'E':'y', 'F':'b', 'G':'l', 'H':'k', 'I':'f', 'J':'t', 'K':'q', 'L':'m', 'M':'a', 'N':'d', 'O':'z', 'P':'h', 'Q':'p', 'R':'s', 'S':'j', 'T':'n', 'U':'u', 'V':'r', 'W':'g', 'X':'e', 'Y':'w', 'Z':'x',' ':' '}

def main():
    f = open('cipher_monoalphabetic','r')
    cipher = f.read().strip()
    f.close()
    print '*** CIPHERTEXT ***'
    print cipher

    collected = set()
    print 
    print '*** DUPLICATE MAPPINGS (if any)  ***'
    for v in ALPH.values():
        if v == v.upper():
            continue
        if v in collected:
            print "duplicate entries for ",v
        collected.add(v)

    print
    print '*** MISSING MAPPINGS (if any)  ***'
    alph_key_set = set([k.lower() for k in ALPH.keys()])
    alph_val_set = set(ALPH.values())
    missing_set = alph_key_set - alph_val_set
    print ', '.join(list(missing_set))

    freq = collections.defaultdict(int)
    first_freq = collections.defaultdict(int)
    word_freq = collections.defaultdict(int)
    for i in xrange(len(cipher)):
        if cipher[i].isalnum():
            freq[cipher[i]] += 1

    stripped_cipher = ''.join([ch for ch in cipher if ch.isalnum() or ch == ' '])
    split_cipher = stripped_cipher.split(' ')

    for cipher_word in split_cipher:
        if len(cipher_word) > 0:
            first_freq[cipher_word[0]] += 1
            word_freq[cipher_word] += 1

    deciphered = decipher(cipher, ALPH)

    print '*** DECIPHERED  ***'
    print deciphered
    print
    print '*** CHAR FREQUENCY ***'
    sorted_x = sorted(freq.items(), key=operator.itemgetter(1))
    print ';'.join(["%s:%s (%d)" % (item[0], decipher(item[0], ALPH), item[1]) for item in sorted_x])
    print
    print '*** FIRST LETTER FREQUENCY ***'
    sorted_f = sorted(first_freq.items(), key=operator.itemgetter(1))
    print ';'.join(["%s:%s (%d)" % (item[0], decipher(item[0], ALPH), item[1]) for item in sorted_f])
    print
    print '*** WORD FREQUENCY ***'
    sorted_w = sorted(word_freq.items(), key=operator.itemgetter(1))
    print '; '.join(["%s:%s (%d)" % (item[0], decipher(item[0], ALPH), item[1]) for item in sorted_w])

def decipher(cipher, mapping):
    out = []
    for i in xrange(len(cipher)):
        out.append(ALPH[cipher[i]] if cipher[i] in ALPH else cipher[i])
    return ''.join(out)

if __name__ == "__main__":
    main()
