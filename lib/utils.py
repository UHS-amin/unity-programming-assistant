from typing import List

def getTotalOf2D(l: List):
    _sum = 0
    for sl in l:
        if isinstance(sl, List):
            _sum += len(sl)
        else:
            _sum = _sum
    return _sum

def getResultsNumFrom2D(res: List, pos = 1):
    _sum = 0
    if isinstance(res, List):
        total = getTotalOf2D(res)
        for i in range(0, pos if pos > 0 and pos <= len(res) else len(res)):
            _sum += len(res[i]) if res[i] is not None and isinstance(res[i], List) else 0
        return [total, _sum]
    else:
        return 0

def gt2d(l: List):
    return getTotalOf2D(l)

def grnf2d(res: List, pos: int = 1):
    return getResultsNumFrom2D(res, pos)