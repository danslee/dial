# SVG Watch / Clock Dial generator

This library is based on the svgwrite library and generates an SVG file with a dial. You set up the dial by adding elements. They are:

  - top : The 12 o'clock marker (if defined)
  - major : The 3, 6, and 9 o'clock markers (if defined)
  - hour : all other hourly markers
  - minute : all minute markers
  - sub : all sub minute markers
  - substeps : the number of subdivisions of the second
  - hourhand : the hour hand
  - minhand : the hour hand
  - sechand : the second hand
  - dtime : the time to be displayed
  - track : the external circle (if defined)

You create a dial by defining svgwrite elements which correspond to the markers, creating a dial, and then calling dial.gen_dial.

The files are

  - dial.py : the dial library
  - example.py : an example svgwrite file
  - maxdial.py : a broken example
  - mission-timer-flat.py : an example dial
  - mission-timer.py : another example dial
  - ploprof.py : another example dial, generates an dial and hand set similar to the ploprof set.

I apologize for the poor state of the files, they were written for purely personal use over a few hours many years ago and I haven't actively maintained them in any way once I was able to generate my desired mission timer svg files.

Use of these files is free under the [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) license. Credit must be given to dlee@dlee.io if distributed or modified.
