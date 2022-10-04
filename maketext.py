#!/usr/bin/env python3
""" Create the actual posting text """
import sys
import re

def help():
    print(
f'''Usage: {sys.argv[0]}  link [season]
    link is the Dropbox link for the full results file.
    season is the season number, unless included in the link as "/llnnn.csv"
''')

       

infile = sys.argv[1]
try:
    season = sys.argv[2]
except IndexError:
    m = re.search(r'/[lL][lL]([0-9]+)\.csv', infile)
    if m:
        season = m.group(1)
    else:
        help()
        sys.exit(1)

ltext = f"""
I implemented SheahanJ's algorithm from the first posts in this forum in Python; DengJY improved the code by using the Pandas package and added the computation of "xRank" (expected rank).  Each season, I run the code and post the top 100 and bottom 100 "lucky" LLamas to the message board.

You can find the full results for season {season} on Dropbox at [url]{infile}[/url].  The results for seasons beginning with season 70 are in this [url=https://www.dropbox.com/sh/79w2o3m2wv5txgm/AADGWDoBwQDr7HDveVMLrWPBa?dl=0]Dropbox folder[/url].

The code is available on GitHub at [url]https://github.com/dssinger/llluck[/url].

The top 100 "lucky" LLamas are listed below, and the bottom 100 will be in the next posting."""

with open(f'lucky{season}.txt', 'w') as outfile:
    outfile.write(ltext)
    outfile.write('\n\n')
    outfile.write(open(f'lucky{season}.bbcode', 'r').read())
    outfile.write('\n')

with open(f'unlucky{season}.txt', 'w') as outfile:
    outfile.write(f'Here are the 100 least lucky LLamas for season {season}.\n\n')
    outfile.write(open(f'unlucky{season}.bbcode', 'r').read())
    outfile.write('\n')

