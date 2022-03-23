#!/usr/bin/env python3
""" Clean up the output of llluck to avoid newlines that will confuse
    the LearnedLeague site """

import sys

def help():
  print(f'Usage: {sys.argv[0]}  season  dropbox_URL')
  sys.exit(1)

def dofile(infile):
  infile.readline()
  l = infile.readline()
  all = []
  def accum(s):
    all.append(s)
  accum('[table]')
  accum('[tr]')
  n = ''
  for word in l.split('|'):
    accum(f'[th]{n}{word}{n}[/th]')
  accum('[/tr]')
  while l := infile.readline():
    words = l.split('|')
    if len(words) > 1:
      accum(f'[tr]')
      for word in words:
        accum(f'[td]{n}{word}{n}[/td]')
      accum(f'[/tr]')
  accum('[/table]')
  return(''.join(all))

# We expect exactly two arguments: season and dropbox URL
if len(sys.argv[1:]) != 2:
  help()
try:
  season = int(sys.argv[1])
except:
  help()

url = sys.argv[2]
if 'dropbox' not in url:
  help()

# OK, now we know what to put into the prefatory text

infile = open(f'lucky{season}.bbcode', 'r')
outfile = open(f'lucky{season}.txt', 'w')
outfile.write('')
outfile.write('I implemented SheahanJ\'s algorithm from the first posts in this forum in Python; DengJY improved'
              ' the code by using the Pandas package and added the computation of "xRank" (expected rank).  Each'
              ' season, I run the code and post'
              ' the top 100 and bottom 100 "lucky" LLamas to the message board.'
              '\n\n'
              f'You can find the full results for season {season} on Dropbox at [url]{url}[/url].  The results for'
              ' seasons beginning with season 70 are in this'
              ' [url=https://www.dropbox.com/sh/79w2o3m2wv5txgm/AADGWDoBwQDr7HDveVMLrWPBa?dl=0]Dropbox folder[/url].'
              '\n\n'
              'The code is available on GitHub at [url]https://github.com/dssinger/llluck[/url].'
              '\n\n')

outfile.write('The top 100 "lucky" LLamas are listed below, and the bottom 100 will be in the next posting.\n\n')


outfile.write(infile.read())
outfile.close()

infile = open(f'unlucky{season}.bbcode', 'r')
outfile = open(f'unlucky{season}.txt', 'w')
outfile.write(f'Here are the 100 least lucky LLamas for Season {season}.\n\n')
outfile.write(infile.read())
outfile.close()


