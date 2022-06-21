# llluck
Luck computation for Learned League (per SheahanJ's algorithm)

This is an implementation of SheahanJ's algorithm for computing
"luck" in the [LearnedLeague](http://learnedleague.com), as described
by his [post]((http://www.learnedleague.com/viewtopic.php?f=3&t=5250)) in the LearnedLeague Forum.

Usage: ./llluck.py infile [season]

  infile: input file to read, typically with the season number as the first set of digits in the filename.
  season: the season number (required if the season number is not in the input filename)

Produces three output files:

  ll{season}.csv - a CSV including all the luck computations
  lucky{season}.bbcode - the luckiest 100 LLamas in BBCode format
  unlucky{season}.bbcode - the least lucky 100 LLamas in BBCode format


After creating these files, upload the `lucky.csv` file to Dropbox and copy its shared URL.  Then run

    ref.py {season} {URL}

to create `lucky.txt` and `unlucky.txt`, ready to cut-and-paste into the Message Board.
