#!/usr/bin/env python
""" LearnedLeague Luck

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
"""

import csv, os, sys, math

def normalize(s):
    s = s.replace(' ','')
    if not s[0].isalpha():
        s = '_' + s
    abbrevs = {'Wins': 'W', 'Losses': 'L', 'Ties': 'T'}
    if s in abbrevs:
        s = abbrevs[s]
    return s
    
def mean(l):
    return sum(l) / len(l)
    
class Rundle(object):
    rundles = {}
    
    @classmethod
    def get(self, name):
        if name not in self.rundles:
            self.rundles[name] = self(name)
        return self.rundles[name]
            
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.tFL = 0
        self.tFW = 0
        self.tTCA = 0
        self.tQ = 0
        self.pcount = 0
        
    def addPlayer(self, player):
        self.players[player.Player] = player
        self.tFL += player.FL
        self.tFW += player.FW
        self.tTCA += player.TCA
        self.tQ += player.Q
        self.pcount += 1
            
                    
        
        
    
    
class Player(object):
    players = {}
    @classmethod
    def get(self, name):
        return self.players[name]
    
    def __init__(self, dict):
        # Clean up the data from the spreadsheet and put it into the object
        for key in dict: 
            newkey = normalize(key)
            value = dict[key]
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
                
            
            self.__dict__[newkey] = value
            
        # Compute additional stats
        self.played = self.W + self.L + self.T
        self.forfeitRate = self.FL / self.played
        self.Q = 6 * (self.played - self.FL)
        self.MPA = self.TMP - self.MPD
        
        # Link into the rundle
        self.realRundle = Rundle.get(self.Rundle)
        self.realRundle.addPlayer(self)
        
        # And save
        self.players[self.Player] = self
        
    def computeStats(self):
        rr = self.realRundle
        oFL = rr.tFL - self.FL  # Games forfeited by others
        aoFL = oFL / (rr.pcount - 1)  # Average games forfeited by others
        self.oFR = (1.0 * oFL) / (self.played * (rr.pcount - 1))  # Other forfeit rate
        self.xFW = self.oFR * (self.played - self.FL) # Expected Forfeit Wins
       

        self.rQPCT = 1.0 * (rr.tTCA - self.TCA)/(rr.tQ - self.Q)
        self.xCAA = self.rQPCT * 6 * (25-self.xFW-self.FL)
        self.xMPA = self.PCAA * self.xCAA
        self.SOS = (self.CAA / (6.0 * (self.played - self.FW))) / self.rQPCT
        

        try:
            self.xTMP = self.TMP*(25.0-self.xFW-self.FL)/(25.0-self.FL)
        except ZeroDivisionError:
            self.xTMP = 0

        try:
            self.pwp = 1/(1+(self.xMPA/self.xTMP)**1.93)
        except ZeroDivisionError:
            self.pwp = 0

        self.xPts = 2*self.pwp*(25-self.xFW-self.FL) + (2*self.xFW) - self.FL
            
        self.luck = (self.Pts- self.xPts) / 2
        
        
        
    def out(self, stats):
        ans = [self.__dict__[normalize(t)] for t in stats]
        return ans
    
def output(filename, data, stats, fmts):
    # Unfortunately, the BBCode implementation on LearnedLeague doesn't properly
    # handle tables (it puts a huge amount of whitespace above the table), so we
    # have to use pre-formatted text instead.  We replace spaces with underscores
    # for purposes of clarity.
    outfile = open(filename, 'w')
    outfile.write('[code]\n')
    
    res = []
    outline = ['Rank']
    # We need to figure out how wide to make each column.
    # Start by leaving enough room for the item names
    widths = {}     
    for item in stats:
        outline.append(item)
        widths[item] = len(item)
    res.append(outline)
    
    
    
    linenum = 0
    for line in data:
        linenum += 1
        outline = ['%4d' % linenum]
        for item in stats:
            if 's' in fmts[item]:
                value = fmts[item] % line.__dict__[item].strip()
            else:
                value = fmts[item] % line.__dict__[item]
            outline.append(value)
            widths[item] = max(widths[item],len(value))
        res.append(outline)
        
    # Now, we have all of the results in outline, and widths tells us how wide each
    #   column must be, so we can output the results
    
    fmtline  = '%4s | ' + ' | '.join([('%%%ds' if 's' not in fmts[item] else '%%-%ds') % widths[item] for item in stats])
    for line in res:
        outfile.write(fmtline % tuple(line))
        outfile.write('\n')
        
    outfile.write('[/code]\n')
        
   
   
    outfile.close()
    
 

if __name__ == '__main__': 
    # Get the data
    reader = csv.DictReader(sys.stdin)
    for row in reader:
        Player(row)
    
    # Now we can compute all statistics
    for p in Player.players.values():
        p.computeStats()
        
    # Sort the players from luckiest to least lucky
    sortedlist = sorted(Player.players.values(), key=lambda x:0-x.luck)

    # Establish columns for output
    stats = [
        'Player', 'W', 'L', 'T', 'Pts', 'MPD', 'Rundle', 'xPts', 'luck', 'SOS'
    ]
    fmts = {'Player': '%s', 'W': '%2d', 'L': '%2d', 'T':'%2d', 'Pts':'%3d',
            'MPD': '%4d', 'Rundle': '%s', 'xPts': '%7.2f', 'luck': '%7.2f', 'SOS' : '%5.2f'}

    # The spreadsheet gets more information
    ssstats = ['Player', 'Rundle', 'Wins', 'Losses', 'Ties', 'Pts', 'xPts', 'MPD', 'FL', 'FW', 'xFW', 'pwp', 'QPct', 'rQPCT', 'PCAA', 'CAA', 'xCAA', 'MPA', 'xMPA', 'TMP', 'xTMP', 'luck', 'SOS']

        
    # Generate the total list
    writer = csv.writer(open('lucky.csv','wb'))
    writer.writerow(ssstats)
    
    for p in sortedlist:
        writer.writerow(p.out(ssstats))
    
    # And now, let's generate the luckiest and unluckiest 100 LLamas
    output('lucky.bbcode', sortedlist[0:100], stats, fmts)
    
    # For unlucky LLamas, we need to ignore Pavanos.
    index = -1

    while sortedlist[index].FL == 25:
        index -= 1
    
    output('unlucky.bbcode', sortedlist[index:index-100:-1], stats, fmts)
    
