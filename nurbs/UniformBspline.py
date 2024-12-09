#!/usr/bin/python3
# Created: Oct, 25, 2024 15:09:53 by Wataru Fukuda

import numpy

class UniformBspline():
  @staticmethod
  def genKnotVector(ne,order):
    knots = []
    for i in range(order+1):  # repeat the same knot at the edge
      knots.append(0)
    for i in range(1,ne):
      knots.append(float(i))
    for i in range(order+1):  # repeat the same knot at the edge
      knots.append(float(ne))
    knots = numpy.array(knots,dtype="f8")
    return knots  # range : 1 ~ ne

  @staticmethod
  def genControlPoints(ne,order):
    knots = UniformBspline.genKnotVector(ne,order)
    cxyz = [0]
    dx = 0
    nc = ne + order  # the num of control points
    for i in range(1,nc):
      dx = ( knots[i+order] - knots[i] ) / ( (knots[-1] - knots[0]) * order )
      cxyz.append(cxyz[-1]+dx)
    cxyz=numpy.array(cxyz,dtype="f8") # range : 0~1
    return cxyz

