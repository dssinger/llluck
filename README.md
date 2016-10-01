# llluck
Luck computation for Learned League (per SheahanJ's algorithm)

This is an implementation of SheahanJ's algorithm for computing
"luck" in the [LearnedLeague](http://learnedleague.com), as described
by his post at in the [LearnedLeague Forum](http://www.learnedleague.com/viewtopic.php?f=3&t=5250)

The program expects to receive a CSV of player records on STDIN, 
in the format of the "all players" file from the LL site.

It generates three output files in the current directory:

lucky.csv - a CSV with player names, records, Rundle, 
   expected points, luck, and strengh-of-schedule as defined by SheahanJ

lucky.bbcode - a BBCode table showing the same information for the 
   luckiest 100 LLamas (all output rounded to 2 decimal places)

unlucky.bbcode - a BBCode table showing the same information for the
   unluckiest 100 LLamas 
