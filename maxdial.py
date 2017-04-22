import svgwrite
import dial
from dial import dial

# Author: dlee@dlee.io / enkidu on watchuseek
# Use of these files is free under the
# [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
# Enjoy!

def main():
  centerx, centery, radius = 1200, 1200, 1000
  #centerx, centery, radius = 600, 600, 500
  drawing = svgwrite.Drawing('maxdial.svg',
          size=(centerx*2, centery*2),
          profile='full', fill='black')

  top_dx = drawing.g()
  top_dx.add(drawing.path(['m', (505,0), 'h', 45, 'v', 200, 'h', -45, 'z']))
  top_dx.add(drawing.path(['m', (450,0), 'h', 45, 'v', 200, 'h', -45, 'z']))
  top_dx.add(drawing.rect((498,0), (4, 50)))
  hour_dx = drawing.circle(center=(500,100), r=80)
  major_dx = drawing.rect((450,20),(100,250), rx=10, ry=10)

  mydial = dial(drawing, (centerx, centery), radius,
      top=top_dx, hour=hour_dx, major=major_dx)

  mydial.gen_dial()


if __name__ == '__main__':
  main()
