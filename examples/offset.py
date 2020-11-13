#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cavaliercontours as cavc
from PyQt5 import QtGui
import pyqtgraph as pg
import numpy as np
import math

def polyline2segments(polyline):
    precision = 1e-3
    points = []
    vertex_data = polyline.vertex_data()
    n = vertex_data.shape[1]
    for i in range(n - int(not polyline.is_closed())):
        a = vertex_data[:2,i]
        b = vertex_data[:2,(i+1)%n]
        bulge = vertex_data[2,i]
        if points:
            points.pop(-1)
        if math.isclose(bulge, 0):
            points += [a, b]
        else:
            rot = np.array([[0,-1],
                            [1, 0]])
            on_right = bulge >= 0
            if not on_right:
                rot = -rot
            bulge = abs(bulge)
            ab = b-a
            chord = np.linalg.norm(ab)
            radius = chord * (bulge + 1. / bulge) / 4
            center_offset = radius - chord * bulge / 2
            center = a + ab/2 + center_offset / chord * rot.dot(ab)

            a_dir = a - center
            b_dir = b - center
            rad_start = math.atan2(a_dir[1], a_dir[0])
            rad_end   = math.atan2(b_dir[1], b_dir[0])

            if not math.isclose(rad_start, rad_end):
                if on_right != (rad_start < rad_end):
                    if on_right:
                        rad_start -= 2*math.pi
                    else:
                        rad_end -= 2*math.pi

                rad_len = abs(rad_end - rad_start)
                if radius > precision:
                    max_angle = 2 * math.acos(1.0 - precision / radius)
                else:
                    max_angle = math.pi
                nb_segments = max(2, math.ceil(rad_len / max_angle) + 1)

                angles = np.linspace(rad_start, rad_end, nb_segments + 1)
                arc_data = (center.reshape(2,1) + radius *
                            np.vstack((np.cos(angles), np.sin(angles))))
                points += np.transpose(arc_data).tolist()
    return  np.transpose(np.array(points))

if __name__ == '__main__':
    vertex_data = np.load('polyline.npy')
    polyline = cavc.Polyline(vertex_data, is_closed=True)

    # create a list of polylines for different offset values
    polylines = [polyline]
    for i in range(10, 50, 10):
        polylines += polyline.parallel_offset(i, False)

    # transform polylines with bulge into straight lines only
    line_arrays = [polyline2segments(p) for p in polylines]

    # aggregate all line arrays for display with 'connect' array
    all_lines = np.empty((2,0), dtype=np.float)
    connect = np.empty(0, dtype=np.bool)
    for arr in line_arrays:
        connected = np.ones(arr.shape[1], dtype=np.bool)
        connected[-1] = False
        connect = np.concatenate((connect, connected))
        all_lines = np.concatenate((all_lines, arr), axis=1)

    # pyqtgraph display
    pg.setConfigOption('antialias', True)
    app = QtGui.QApplication([])
    plot = pg.PlotWidget()
    plot.setAspectLocked()
    curve = pg.PlotCurveItem([], [], pen=pg.mkPen(color=(80, 200, 255), width=2))
    plot.addItem(curve)
    curve.setData(all_lines[0], all_lines[1], connect=connect)
    plot.show()
    app.exec_()
