import svgwrite
import math
from math import pi
import datetime

# Author: dlee@dlee.io / enkidu on watchuseek
# Use of these files is free under the
# [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
# Enjoy!

quarter_minute = math.pi / 120
third_minute = math.pi / 90
half_minute = math.pi / 60
one_minute = math.pi / 30
one_hour = math.pi / 6

quarter_minute_tan = math.tan(quarter_minute)
third_minute_tan = math.tan(third_minute)
half_minute_tan = math.tan(half_minute)
one_minute_tan = math.tan(one_minute)
one_hour_tan = math.tan(one_hour)

quarter_minute_sin = math.sin(quarter_minute)
third_minute_sin = math.sin(third_minute)
half_minute_sin = math.sin(half_minute)
one_minute_sin = math.sin(one_minute)
one_hour_sin = math.sin(one_hour)

quarter_minute_cos = math.cos(quarter_minute)
third_minute_cos = math.cos(third_minute)
half_minute_cos = math.cos(half_minute)
one_minute_cos = math.cos(one_minute)
one_hour_cos = math.cos(one_hour)

def calc_width_and_inset(radius, angle):
  width = radius * math.sin(angle)
  inset = radius - (radius * math.cos(angle))
  return width, inset

def calc_flat_width(radius, angle):
  width = radius * math.tan(angle)
  return width

def calc_flat_inset(radius, gap):
  inset = radius - math.sqrt((radius * radius) - (gap * gap))
  return inset

def draw_tapered_index(d, g, o_radius, height, angle, flat, **opts):
  base_width, base_inset = calc_width_and_inset(o_radius, angle)
  top_width = calc_flat_width(o_radius - height, angle)
  p = []
  p.extend(['m', (500 - base_width, 1000 - o_radius + base_inset)])
  if flat:
    p.extend(['l', (2 * base_width, 0)])
  else:
    p.extend(['a', (o_radius, o_radius, 0, 0, 1, 2 * base_width, 0)])
  p.extend(['l', (top_width - base_width, height - base_inset)])
  p.extend(['l', (-2 * top_width, 0)])
  p.extend(['z'])
  g.add(d.path(p, **opts))

def draw_split_tapered_index(d, g, o_radius, gap, height, angle, flat, **opts):
  base_width, base_inset = calc_width_and_inset(o_radius, angle)
  top_width, top_inset = calc_width_and_inset(o_radius - height, angle)
  base_gap_inset = calc_flat_inset(o_radius, gap)
  pl, pr = [], []
  if flat:
    pr.extend(['m', (500 + gap, 1000 - o_radius + base_inset)])
    pl.extend(['m', (500 - gap, 1000 - o_radius + base_inset)])
    pr.extend(['l', (base_width - gap, 0)])
    pl.extend(['l', (gap - base_width, 0)])
  else:
    pr.extend(['m', (500 + gap, 1000 - o_radius + base_gap_inset)])
    pl.extend(['m', (500 - gap, 1000 - o_radius + base_gap_inset)])
    pr.extend(['a', (o_radius, o_radius,
      0, 0, 1, base_width - gap, base_inset - base_gap_inset)])
    pl.extend(['a', (o_radius, o_radius,
      0, 0, 0, gap - base_width, base_inset - base_gap_inset)])
  pr.extend(['l', (top_width - base_width, height - base_inset)])
  pl.extend(['l', (base_width - top_width, height - base_inset)])
  pr.extend(['l', (gap - top_width, 0), 'z'])
  pl.extend(['l', (top_width - gap, 0), 'z'])
  g.add(d.path(pr))
  g.add(d.path(pl))

class dial:
  '''
  Indexes are defined in a box 0,0 - 1000,1000 with the center edge of the
  dial being at 500,0 and the center of the dial at 500, 1000. Hands are
  defined by a larger box 0,0 - 2000,2000
  with the center of the dial at 500,1000
  and the outermost edge of the dial at 500,2000
  '''
  def __init__(self, dwg, center, radius, **dict):
    self.dwg = dwg
    self.center = center
    self.radius = radius
    self.defaults = {
        'track':self.dwg.circle(center=(1000,1000),r=1000,stroke='black',fill='none'),
        'dtime':datetime.time(10,9,29,200000),
        'top':   self.dwg.rect((475,0), (50, 250)),
        'major': self.dwg.rect((480,0), (40, 250)),
        'hour':  self.dwg.rect((490,0), (20, 125)),
        'minute':self.dwg.rect((498,0), (4, 50)),
        'sub':   self.dwg.rect((499,0), (2, 25)),
        'substeps':4,
        'hourhand':self.dwg.rect((480,980), (40, 370)),
        'minhand': self.dwg.rect((490,980), (20, 720)),
        'sechand': self.dwg.rect((495,950), (10, 975)),
        'minute_skip':None,
        }
    self.set_params(**dict)

  def set_param(self, key, **dict):
    self.__dict__[key] = dict.get(key, self.defaults[key])

  def set_params(self, **dict):
    for k in self.defaults.keys():
      if not self.__dict__.get(k):
        self.set_param(k, **dict)
      elif dict.has_key(k):
        self.set_param(k, **dict)

  def gen_dial(self):
    self.define_track()
    self.gen_track()

    self.define_indices()
    self.gen_indices()

    self.define_hands()
    self.gen_hands()
    self.dwg.save()

  def define_track(self):
    self.add_name_to_drawing_defs('track')

  def gen_track(self):
    if not self.track:
      return
    track = self.dwg.use(self.track)
    track.translate(
        self.center[0] - self.radius,
        self.center[1] - self.radius
        )
    track.scale(1.0 * self.radius / 1000)
    self.dwg.add(track)


  def define_indices(self):
    '''Adds definitions to the dial for top, major, hour, minute and sub
    indices'''
    previous=None
    for index_name in ['sub', 'minute', 'hour', 'major', 'top']:
      self.add_name_to_drawing_defs(index_name, previous)
      previous = index_name

  def gen_indices(self):
    '''
    draw dial indices.
      top at the 12 o'clock position,
      major at the 3,6,9 positions,
      hour at the remaining hour positions,
      minute at the remaining minute positions,
      sub at the sub-minute positions.
    '''
    substeps = self.substeps
    for i in range(0, 60 * substeps):
      angle = 6.0 * i / substeps;
      hour, minute = get_hour_minute_from_angle(angle)
      if (i == 0):
        # top marker
        self.gen_index(self.top, angle)
        continue
      elif (i % (3 * 5 * substeps) == 0):
        # 3-6-9 case
        self.gen_index(self.major, angle)
        continue
      elif (i % (5 * substeps) == 0):
        # hour case
        self.gen_index(self.hour, angle)
        continue
      elif (i % substeps == 0):
        # min case
        if int(minute) in self.minute_skip:
          continue
        self.gen_index(self.minute, angle)
        continue
      else:
        self.gen_index(self.sub, angle)
        continue

  def gen_index(self, unit, angle):
    '''
    draw a single index on the dial. (500,0) is the edge of the dial at the
    center of the angle. (500, 1000) is the center of the dial.
    '''
    if not unit:
      return
    unit = self.dwg.use(unit)
    unit.translate(
        self.center[0] - self.radius/2,
        self.center[1] - self.radius
        )
    unit.rotate(angle, (self.radius/2,self.radius))
    # if vertical is set, need to do an additional rotation here
    unit.scale(1.0 * self.radius / 1000)
    self.dwg.add(unit)

  def define_hands(self):
    for hand_name in ['hourhand', 'minhand', 'sechand']:
      self.add_name_to_drawing_defs(hand_name)

  def gen_hands(self):
    hand_angles = time_to_hand_angles(self.dtime)
    self.gen_hand(self.hourhand, hand_angles[0])
    self.gen_hand(self.minhand, hand_angles[1])
    self.gen_hand(self.sechand, hand_angles[2])

  def gen_hand(self, hand, angle):
    if not hand:
      return
    hand = self.dwg.use(hand)
    hand.translate(
        self.center[0] - self.radius/2,
        self.center[1] - self.radius
        )
    hand.rotate(angle+180, (self.radius/2, self.radius))
    hand.scale(1.0 * self.radius / 1000)
    self.dwg.add(hand)

  def add_name_to_drawing_defs(self, name, override=None):
    element = self.__dict__.get(name)
    if not element:
      element = self.__dict__.get(override)
    if not element:
      self.__dict__[name] = None
      return
    self.__dict__[name] = self.dwg.defs.add(self.dwg.g(id=name))
    self.__dict__[name].add(element)

def time_to_hand_angles(in_time, full_circle=360.0):
  '''returns a triple of degrees, indicating the angle from 0 of the hour,
  minute and seconds hand based on the passed in time'''
  hour = in_time.hour
  min = in_time.minute
  sec = in_time.second
  usec = in_time.microsecond
  usec_angle = (usec / (60.0 * 1000000)) * full_circle 
  sec_angle = (sec / 60.0) * full_circle + usec_angle
  min_angle = (min / 60.0) * full_circle + (sec_angle / 60.0)
  hour_angle = (hour / 12.0) * full_circle + (min_angle / 12.0)
  return (hour_angle, min_angle, sec_angle)

def get_hour_minute_from_angle(angle):
  minute = math.floor(angle / 6)
  hour = math.floor(minute / 5)
  return hour, minute

def main():
  centerx, centery, radius = 1200, 1200, 1000
  drawing = svgwrite.Drawing('test.svg',
          size=(centerx*2, centery*2),
          profile='full', fill='black', stroke='black')
  mydial = dial(drawing, (centerx, centery), radius)
  mydial.gen_dial()

if __name__ == '__main__':
  main()
