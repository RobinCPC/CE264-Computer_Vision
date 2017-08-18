'''# -*- coding: utf-8 -*-'''
"""
Implement Levenshtein Distance
Source: https://en.wikipedia.org/wiki/Levenshtein_distance
"""


def unicodetoascii(text):
    """
    Source: http://stackoverflow.com/questions/27996448/python-encoding-decoding-problems
    """
    uni2ascii = {
            ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
            ord('\xc3\xa9'.decode('utf-8')): ord('e'),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),
            # ===
            ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),
            # ===
            ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),
            # ===
            ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
            ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
            ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
            ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
            ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),

                            }
    try:
        return text.decode('utf-8').translate(uni2ascii).encode('ascii') 
    except Exception, e:
        print e
        return text
        #raise e:
    #return text.decode('utf-8').translate(uni2ascii).encode('ascii')


def read_file(f_name):
    """
    open, read file and put
    into a string
    :type f_name: str
    :rtype : string
    """
    file_object = open(f_name, 'r')
    out_str = file_object.read()
    if '\xe2' in out_str:
        out_str = unicodetoascii(out_str)
    while len(out_str) != 0  and out_str[-1] == '\n':
        out_str = out_str[:-1]
    return out_str


def read_file_split(f_name):
    """
    open, read file and put
    into a list of string
    :type f_name: str
    :rtype inps_list: list of string
    """
    inps_list = []
    with open(f_name, 'r') as f:
        for line in f:
            # preporcess some unicode characters
            if '\xe2' in line:
                line = unicodetoascii(line)

            #print line
            if (len(line) == 1 and line[0] == '\n') or len(line) == 0:
                continue
            elif line[-1] == '\n':
                inps_list.append(line[:-1])
            else:
                inps_list.append(line)
    return inps_list


def levenshteinDistanceRecursive(src, res):
    """
    Computeing Levenshtein distance by recursive
    :type src: string
    :type res: string
    :rtype cost: int
    """
    cost = 0

    # base case: empty string
    if len(src) == 0:
        return len(res)
    if len(res) == 0:
        return len(src)

    # test if last characters of th strings match
    if src[-1] == res[-1]:
        cost = 0
    else:
        cost = 1

    # return minimum of delete char from src, delete char from res, and both
    return min(levenshteinDistance(src[:-1], res     ) + 1,
               levenshteinDistance(src     , res[:-1]) + 1,
               levenshteinDistance(src[:-1], res[:-1]) + cost)


def levenshteinDistance(src, res):
    """
    Computer Levenshtein distance by iterative with two rows
    :type src: string
    :type res: string
    :rtyep cost: int
    """
    # print 'src len: ' + str(len(src))
    # print 'res len: ' + str(len(res))

    # degerate cases
    if (src == res):
        return 0
    if len(src) == 0:
        return len(res)
    if len(res) == 0:
        return len(src)

    # create two works vectors of integer distance
    # and initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty src
    # the distance is just the number of characters to delete from res
    v0 = [i for i in xrange(len(res)+1)]
    v1 = [0] * (len(res) + 1)

    for i in xrange(len(src)):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty res
        v1[0] = i + 1

        # use formula to full in the rest of the row
        for j in xrange(len(res)):
            cost = 0 if src[i] == res[j] else 1
            v1[j+1] = min(v1[j] + 1, v0[j+1] + 1, v0[j] + cost)

        # copy v1 (current row to v0 (previous row) for next iteration
        for j in xrange(len(v0)):
            v0[j] = v1[j]

    return v1[len(res)]



if __name__ == '__main__':
    # Input files
    src_text = 'IMG_0535-1_src.txt'      #'IMG_0538_src.txt'
    src_list = read_file(src_text)

    abb_list = read_file('IMG_0535-1.txt')    # 'IMG_0538.txt'
    tess_list = read_file('r_535-1.txt')      # 'r_538.txt'

    print src_list
    print abb_list
    print tess_list

    #for s in src_list:
    #    print s, len(s)
    #    #ss = s.decode('string_escape')
    #    #print ss, len(ss)

    #count = levenshteinDistance('sitting', 'kitten')
    #print count

    # Compute Levenshtein Distance

    count = 0
    print '\nCompare Source and Abby result'
    for s, t in zip(src_list, abb_list):
        print s
        print t
        count += levenshteinDistance(s, t)
    print 'number of different characters for Abby:'
    print count


    count = 0
    print '\nCompare Source and Tesseract result'
    for s, t in zip(src_list, tess_list):
        print s
        print t
        count += levenshteinDistance(s, t)
    print 'number of different characters for Tesseract:'
    print count
