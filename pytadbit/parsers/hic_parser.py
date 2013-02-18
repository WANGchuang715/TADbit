"""
19 Dec 2012


"""

from math import sqrt

def _read_matrix(f_h):
    """
    reads from file
    """
    nums = []
    while True:
        values = f_h.next().split()
        if values[0].startswith('#'):
            # skip comments
            continue
        break
    # check if we have headers/row-names in the file
    start = 1
    if values[0].isdigit():
        try:
            nums.append([int(v) for v in values])
        except ValueError:
            nums.append([int(float(v)) for v in values])
        start = 0
    # parse the rest of the file
    for line in f_h:
        values = line.split()[start:]
        try:
            nums.append([int(v) for v in values])
        except ValueError:
            nums.append([int(float(v)) for v in values])
    f_h.close()
    size = len(nums)
    return tuple([nums[j][i] for i in xrange(size) for j in xrange(size)]), size


def read_matrix(things, parser=None):
    """
    reads and checks matrix from file or list

    :param things: might be either a file name, a file handler, a list of them
        or a list of list (all with same length)
    :param None parser: a parser function that returns a tuple of lists representing the data matrix,
        with this file example.tsv:
        ::
        
          chrT_001	chrT_002	chrT_003	chrT_004
          chrT_001	629	164	88	105
          chrT_002	86	612	175	110
          chrT_003	159	216	437	105
          chrT_004	100	111	146	278

        the output of parser('example.tsv') might be:
        ``([629, 86, 159, 100, 164, 612, 216, 111, 88, 175, 437, 146, 105, 110,
        105, 278])``


    :returns: the corresponding matrix concatenated into a huge list, also
        returns number or rows

    """
    parser = parser or _read_matrix
    if type(things) is not list:
        things = [things]
    matrices = []
    sizes    = []
    for thing in things:
        if type(thing) is file:
            matrix, size = parser(thing)
            matrices.append(matrix)
            sizes.append(size)
        elif type(thing) is str:
            matrix, size = parser(open(thing))
            matrices.append(matrix)
            sizes.append(size)
        elif type(thing) is list:
            if all([len(thing)==len(l) for l in thing]):
                matrices.append(reduce(lambda x, y: x+y, thing))
                sizes.append(len(thing))
            raise Exception('must be list of lists, all with same length.')
        elif type(thing) is tuple:
            # case we know what we are doing and passing directly list of tuples
            matrices.append(thing)
            siz = sqrt(len(thing))
            if int(siz) != siz:
                raise Exception('Error: matrix should be square.')
            sizes.append(int(siz))
        elif 'matrix' in str(type(thing)):
            try:
                r, c = thing.shape
                if r!=c:
                    raise Exception('matrix needs to be square.')
                matrices.append(thing.reshape(-1).tolist()[0])
                sizes.append(r)
            except Exception as e:
                print 'Error found:', e
                pass
        else:
            raise Exception('Unable to read this file or whatever it is :)')
    if all([s==sizes[0] for s in sizes]):
        return matrices, sizes[0]
    raise Exception('All matrices must have the same size ' +
                    '(same slice and same bins).')