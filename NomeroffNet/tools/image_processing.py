import math
import numpy as np
import cv2
from typing import List


def fline(p0: List, p1: List, debug: bool = False) -> List:
    """
    Вычесление угла наклона прямой по 2 точкам
    """
    x1 = float(p0[0])
    y1 = float(p0[1])

    x2 = float(p1[0])
    y2 = float(p1[1])

    if debug:
        print("Уравнение прямой, проходящей через эти точки:")
    if x1 - x2 == 0:
        k = math.inf
        b = y2
    else:
        k = (y1 - y2) / (x1 - x2)
        b = y2 - k*x2
    if debug:
        print(" y = %.4f*x + %.4f" % (k, b))
    r = math.atan(k)
    a = math.degrees(r)
    a180 = a
    if a < 0:
        a180 = 180 + a
    return [k, b, a, a180, r]


def distance(p0: List, p1: List) -> float:
    """
    distance between two points p0 and p1
    """
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def linearLineMatrix(p0: List, p1: List, verbode: bool = False) -> List:
    """
    Вычесление коефициентов матрицы, описывающей линию по двум точкам
    """
    x1 = float(p0[0])
    y1 = float(p0[1])

    x2 = float(p1[0])
    y2 = float(p1[1])

    A = y1 - y2
    B = x2 - x1
    C = x2*y1-x1*y2
    if verbode:
        print("Уравнение прямой, проходящей через эти точки:")
        print("%.4f*x + %.4fy = %.4f" % (A, B, C))
        print(A, B, C)
    return [A, B, C]


def findDistances(points: List) -> List:
    """
    TODO: describe function
    """
    distanses = []
    cnt = len(points)

    for i in range(cnt):
        p0 = i
        if i < cnt - 1:
            p1 = i + 1
        else:
            p1 = 0
        distanses.append({"d": distance(points[p0], points[p1]), "p0": p0, "p1": p1,
                          "matrix": linearLineMatrix(points[p0], points[p1]),
                          "coef": fline(points[p0], points[p1])})
    return distanses


def buildPerspective(img: np.ndarray, rect: list, w: int, h: int) -> List:
    """
    TODO: describe function
    """
    w = int(w)
    h = int(h)
    pts1 = np.float32(rect)
    pts2 = np.float32(np.array([[0, 0], [w, 0], [w, h], [0, h]]))
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(img, M, (w, h))


def getCvZoneRGB(img: np.ndarray, rect: list, gw: float = 0, gh: float = 0,
                 coef: float = 4.6, auto_width_height: bool = True) -> List:
    """
    TODO: describe function
    """
    if gw == 0 or gh == 0:
        distanses = findDistances(rect)
        h = (distanses[0]['d'] + distanses[2]['d']) / 2
        if auto_width_height:
            w = int(h*coef)
        else:
            w = (distanses[1]['d'] + distanses[3]['d']) / 2
    else:
        w, h = gw, gh
    return buildPerspective(img, rect, w, h)


def getMeanDistance(rect: List, start_idx: int, verbose: bool = False) -> np.ndarray:
    """
    TODO: describe function
    """
    end_idx = start_idx+1
    start2_idx = start_idx+2
    end2_idx = end_idx+2
    if end2_idx == 4:
        end2_idx = 0
    if verbose:
        print('startIdx: {}, endIdx: {}, start2Idx: {}, end2Idx: {}'.format(start_idx, end_idx, start2_idx, end2_idx))
    return np.mean([distance(rect[start_idx], rect[end_idx]), distance(rect[start2_idx], rect[end2_idx])])


def reshapePoints(target_points: List, start_idx: int) -> List:
    """
    TODO: describe function
    """
    if start_idx > 0:
        part1 = target_points[:start_idx]
        part2 = target_points[start_idx:]
        target_points = np.concatenate((part2, part1))
    return target_points


def getCvZonesRGB(img: np.ndarray, rects: list, gw: float = 0, gh: float = 0,
                  coef: float = 4.6, auto_width_height: bool = True) -> List:
    """
    TODO: describe function
    """
    dsts = []
    for rect in rects:
        h = getMeanDistance(rect, 0)
        w = getMeanDistance(rect, 1)
        if h > w and auto_width_height:
            h, w = w, h
        else:
            rect = reshapePoints(rect, 3)
        if gw == 0 or gh == 0:
            w, h = int(h*coef), int(h)
        else:
            w, h = gw, gh
        dst = buildPerspective(img, rect, w, h)
        dsts.append(dst)
    return dsts


def convertCvZonesRGBtoBGR(dsts: List) -> List:
    """
    TODO: describe function
    """
    bgr_dsts = []
    for dst in dsts:
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)
        bgr_dsts.append(dst)
    return bgr_dsts


def getCvZonesBGR(img: np.ndarray, rects: list, gw: float = 0, gh: float = 0,
                  coef: float = 4.6, auto_width_height: bool = True) -> List:
    """
    TODO: describe function
    """
    dsts = getCvZonesRGB(img, rects, gw, gh, coef, auto_width_height=auto_width_height)
    return convertCvZonesRGBtoBGR(dsts)
