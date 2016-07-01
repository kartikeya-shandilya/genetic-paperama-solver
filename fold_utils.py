from Polygon import *
from Polygon.IO import writeSVG
from copy import deepcopy
from numpy import arctan2, pi


def reducePoly(poly):
    poly.simplify()
    try:
        pts = poly[0]
    except:
        return Polygon()
    pts = [(round(i, 3), round(j, 3)) for (i, j) in pts]
    tmp = Polygon(pts)
    return tmp


def fold(poly, chromosome):
    xm, xM, ym, yM = poly.boundingBox()
    (x1, y1), (x2, y2), dirn = chromosome
    lpoly = Polygon()
    if x1 == x2 and y1 == y2:
        return [poly]
    if poly.nPoints() > 20:
        return [poly]
    if (abs(x1 - x2) > 0.3 or (y1 == y2)) and x1 != x2:
        m = (y2 - y1) * 1. / (x2 - x1)
        c = y1 - m * x1
        l_y = m * xm + c
        r_y = m * xM + c
        mny = min(l_y, r_y, ym)
        line_poly = []
        line_poly.append((xm, l_y))
        line_poly.append((xm, mny))
        line_poly.append((xM, mny))
        line_poly.append((xM, r_y))
        lpoly = Polygon(line_poly)
        outer = []
        outer.append((xm, ym))
        outer.append((xM, ym))
        outer.append((xM, mny))
        outer.append((xm, mny))
        outpoly = Polygon(outer)
        lpoly = lpoly - outpoly
    else:
        m = (x2 - x1) * 1. / (y2 - y1)
        c = x1 - m * y1
        t_x = m * yM + c
        b_x = m * ym + c
        mnx = min(t_x, b_x, xm)
        line_poly = []
        line_poly.append((b_x, ym))
        line_poly.append((t_x, yM))
        line_poly.append((mnx, yM))
        line_poly.append((mnx, ym))
        lpoly = Polygon(line_poly)
        outer = []
        outer.append((xm, ym))
        outer.append((xm, yM))
        outer.append((mnx, yM))
        outer.append((mnx, ym))
        outpoly = Polygon(outer)
        lpoly = lpoly - outpoly
    try:
        part1 = poly - lpoly
        part2 = poly - part1
    except:
        return [poly]
    if not (part1.nPoints() and part2.nPoints()):
        return [poly]
    if dirn:
        part1, part2 = part2, part1
    part1 = reducePoly(part1)
    part2 = reducePoly(part2)
    part2_clone = deepcopy(part2)
    if not (part1.nPoints() and part2.nPoints()):
        return [poly]
    pts1 = set(part1[0])
    pts2 = set(part2[0])
    cpts = sorted(list(pts1.intersection(pts2)))
    if not len(cpts):
        return [poly]
    pivot = list(cpts)[-1]
    part2.flip(pivot[0])
    angle = pi + 2 * arctan2(y2 - y1, x2 - x1)
    part2.rotate(angle, pivot[0], pivot[1])
    part2 = reducePoly(part2)
    # union after fold
    flip = part1 + part2
    #flip = reducePoly(flip)
    #return [poly,lpoly,part2,part1,flip]
    return [part2_clone, part2, flip]


def multiFold(poly, chromosome, location=(0, 0)):
    chromosome = tuple(chromosome)
    poly = deepcopy(poly)
    intermediates = [poly]
    prefolded = []
    folded = []
    for i in xrange(len(chromosome)):
        tmp = deepcopy(poly)
        val = fold(tmp, chromosome[i])
        poly = val[-1]
        ftmp1 = Polygon()
        ftmp2 = Polygon()
        if len(val) > 1:
            ftmp1 = val[0]
            ftmp2 = val[1]
        prefolded.append(ftmp1)
        folded.append(ftmp2)
        intermediates.append(poly)
    return intermediates, prefolded, folded


def printBigChromosome(source, target, chromosome):
    ans, prefolded, folded = multiFold(source, chromosome)
    for i in xrange(1, len(ans)):
        ans[i].shift(1.5 * i, 0)
        prefolded[i - 1].shift(1.5 * i, 0)
        folded[i - 1].shift(1.5 * i, 0)
    last = deepcopy(ans[-1])
    last.shift(1.5, 0)
    ans.append(last)
    tmp = deepcopy(target)
    tmp.shift(1.5 * len(ans) - 1.5, 0)
    ans.append(tmp)
    tmp2 = deepcopy(target)
    ans.append(tmp2)
    colors = ['blue'] * (len(ans) - 2) + ['red', 'red'] + ['grey'] * (
        len(prefolded)) + ['green'] * (len(folded))
    ans = ans + prefolded + folded
    return ans, colors


def printMultiBigChromosome(source, target, chromosomes):
    ans = []
    colors = []
    for i, chromosome in enumerate(chromosomes):
        tmp1, tmp2 = printBigChromosome(source, target, chromosome)
        for j in xrange(len(tmp1)):
            tmp1[j].shift(0, -1.5 * i)
        ans += tmp1
        colors += tmp2
    writeSVG('testing4.svg',
             ans,
             height=(50 / len(chromosome)) * len(ans),
             fill_color=tuple(colors),
             fill_opacity=[0.3] * len(ans))
    return None
