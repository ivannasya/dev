#!/usr/bin/python3
#
# License: CC0
#

import os, re, sys, math

UNITS_SRC = "inch"
UNITS_DST = "mm"

# inch to mm
#
def _i2m(inch):
  return float(inch)*25.4

# mm to inch
#
def _m2i(mm):
  return float(mm)/25.4

# convert src unit to destination unit
#
def _u(x):
  _x = float(x)
  if UNITS_SRC != UNITS_DST:
    if UNITS_DST == "mm":
      _x = _i2m(_x)
    elif UNITS_DST == "inch":
      _x = _m2i(_x)
  return _x

# mm to units
#
def _m2u(x):
  if UNITS_DST == "mm":
    return float(x)
  else:
    return _m2i(float(x))

# inch to units
#
def _i2u(x):
  if UNITS_DST == "inch":
    return float(x)
  else:
    return _i2m(float(x))

# format float
#
def _s(x):
  return "{:.8f}".format(x)


Z_UP = _m2u(10)
Z_DOWN = _m2u(-2.5)
Z_STEP = _m2u(-0.4)
Z_ZERO = _m2u(0.0)

G0_SPEED = _m2u(800)
G1_SPEED = _m2u(50)

HOLE_R = _m2u(1.0/2.0)

TOOL_R = _m2u(0.8/2.0 )
#TOOL_R = _m2u(3.175/2.0 )
fn = sys.argv[1]

MAX_ITER = 100


def _circle(r,cx=0.0, cy=0.0, n=32):
  v = []
  for ii in range(n):
    a = 2.0 * math.pi * (float(ii) / float(n))
    v.append( [r*math.cos(a) + cx, r*math.sin(a)  + cy] )
  v.append([cx + r,cy])
  return v

def _printv(v):
  for ii in range(len(v)):
    print( _s(v[ii][0]), _s(v[ii][1]) )

def _printg(v, z_up = Z_UP, z_down = Z_DOWN):
  if len(v)==0: return
  print("G1 Z" + _s(z_up))
  print("G0 X" + _s(v[0][0]) + " Y" + _s(v[0][1]))
  print("G1 Z" + _s(z_down))
  for ii in range(len(v)):
    print( "G1 X" + _s(v[ii][0]) + " Y" + _s(v[ii][1]) )
  print("G1 Z" + _s(z_up))


with open(fn) as fp:
  for line in fp:

    pos = [0,0]

    m = re.match('X(\-?\d*(\.\d*)) *Y(\-?\d*(\.\d*))$', line)
    if m:
      pos[0] = _u(float(m.group(1)))
      pos[1] = _u(float(m.group(3)))
    else:
      continue

    print("G0 Z" + _s(Z_UP))
    print("G0 X" + _s(pos[0]) + " Y" + _s(pos[1]))

    print("G0 Z" + _s(Z_ZERO) + " F" + _s(G0_SPEED))

    cur_iter = 0
    cur_z = Z_ZERO
    prv_z = Z_ZERO
    while (cur_z >= Z_DOWN) and (cur_iter < MAX_ITER):

      print("G1 Z" + _s(cur_z) + " F" + _s(G1_SPEED))

      # if the hole is smaller than the drill bit, skip
      # circle creation
      #
      if HOLE_R > TOOL_R:
        _printg(_circle(HOLE_R - TOOL_R, pos[0], pos[1]), prv_z, cur_z)
        print()

      prv_z = cur_z
      cur_z += Z_STEP
      cur_iter += 1


    print()

