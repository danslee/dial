import dial
import math
import svgwrite

# Author: dlee@dlee.io / enkidu on watchuseek
# Use of these files is free under the
# [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
# Enjoy!

min_or = 975.0
min_h = 150.0
min_w = 8.0

hour_or = min_or
hour_h = min_h
hour_angle = dial.quarter_minute

major_or = min_or
major_h = 2.5 * min_h
major_angle = dial.quarter_minute

top_or = min_or
top_gap = 7.0
top_h = 2.5 * min_h
top_angle = dial.one_minute

def calc_width_and_inset(radius, angle):
  width = radius * math.sin(angle)
  inset = radius - (radius * math.cos(angle))
  return width, inset

def draw_tapered_index(d, g, outer_radius, height, angle):
  base_width, base_inset = calc_width_and_inset(outer_radius, angle)
  top_width, top_inset = calc_width_and_inset(outer_radius - height, angle)
  g.add(d.path(['m', (500 - base_width, 1000 - outer_radius + base_inset),
    'l', (2 * base_width, 0),
    'l', (top_width - base_width, height - base_inset + top_inset),
    'l', (-2 * top_width, 0),
    'z']))

def draw_split_tapered_index(d, g, outer_radius, gap, height, angle):
  base_width, base_inset = calc_width_and_inset(outer_radius, angle)
  top_width, top_inset = calc_width_and_inset(outer_radius - height, angle)
  g.add(d.path(['m', (500 + gap, 1000 - outer_radius + base_inset),
    'l', (base_width - gap, 0),
    'l', (top_width - base_width, height - base_inset + top_inset),
    'l', (gap - top_width, 0),
    'z']))
  g.add(d.path(['m', (500 - gap, 1000 - outer_radius + base_inset),
    'l', (gap - base_width, 0),
    'l', (base_width - top_width, height - base_inset + top_inset),
    'l', (top_width - gap, 0),
    'z']))

def main():
  centerx, centery, radius = 1200, 1200, 1000
  drawing = svgwrite.Drawing('mission-timer.svg',
          size=(centerx*2, centery*2),
          profile='full', fill='black')

  top_dx = drawing.g()
  draw_split_tapered_index(drawing, top_dx, top_or, top_gap, top_h, top_angle)

  hour_dx = drawing.g()
  draw_tapered_index(drawing, hour_dx, hour_or, hour_h, hour_angle)

  major_dx = drawing.g()
  draw_tapered_index(drawing, major_dx, major_or, major_h, major_angle)

  minute_dx = drawing.rect((496,25),(8,150))

  track = drawing.g()
  track.add(drawing.rect((800,999),(400,2)))
  track.add(drawing.rect((999,800),(2,400)))
  track.add(drawing.circle((1000,1000),10))
  track.add(drawing.circle((1000,1000),1000,stroke_width=1, stroke='black', fill='none'))

  mydial = dial.dial(drawing, (centerx, centery), radius,
      track=track,
      sub=None,
      minute_skip=[1,59],
      top=top_dx,
      hour=hour_dx,
      major=major_dx,
      minute=minute_dx,
      sechand=None,
      minhand=None,
      hourhand=None)

  mydial.gen_dial()


if __name__ == '__main__':
  main()


