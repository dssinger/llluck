#!/usr/bin/env python3
import pandas as pd
import numpy  as np
import sys
from io import StringIO
import re

def help():
    print('Usage:', sys.argv[0], 'infile [season]', file=sys.stderr)
    print(file=sys.stderr)
    print('  infile: input file to read, typically with the season number as the first set of digits in the filename.', file=sys.stderr)
    print('  season: the season number (required if the season number is not in the input filename)', file=sys.stderr)
    print('', file=sys.stderr)
    print('Produces three output files:', file=sys.stderr)
    print('', file=sys.stderr)
    print('  ll{season}.csv - a CSV including all the luck computations', file=sys.stderr)
    print('  lucky{season}.bbcode - the luckiest 100 LLamas in BBCode format', file=sys.stderr)
    print('  unlucky{season}.bbcode - the least lucky 100 LLamas in BBCode format', file=sys.stderr)
    sys.exit(1)

infile = sys.argv[1]
try:
    season = sys.argv[2]
except IndexError:
    m = re.search(r'[0-9]+', infile)
    if m:
        season = m.group()
    else:
        help()
        sys.exit(1)
outfile = f'll{season}.csv'
luckfile = f'lucky{season}.bbcode'
unluckfile = f'unlucky{season}.bbcode'


df = pd.read_csv(infile, encoding='ISO-8859-1')
df = df.rename(columns={'Rundle Rank':'Rank'})

count_stats = ['Rundle', 'Player']
sum_stats   = ['Rundle', 'FL', 'FW', 'TCA', 'Q']

df['Matches'] = df['Wins'] + df['Losses'] + df['Ties']
df['Played']  = df['Matches'] - df['FL']
df['FPct']    = df['FL'] / df['Matches']
df['Q']       = 6 * df['Played']
df['MPA']     = df['TMP'] - df['MPD']

count = df[count_stats].groupby('Rundle', as_index=False).count()
sum   = df[sum_stats].groupby('Rundle', as_index=False).sum()

count = count.rename(columns={'Player':'Players'})
sum   = sum.rename(columns={'FL':'rFL', 'FW':'rFW', 'TCA':'rTCA', 'Q':'rQ'})

df = df.merge(count)
df = df.merge(sum)

df['oFL']  = df['rFL'] - df['FL']
df['aoFL'] = df['oFL'] / (df['Players'] - 1)
df['oFR']  = df['aoFL'] / df['Matches']
df['xFW']  = df['oFR'] * df['Played']

df['rQPct'] = (df['rTCA'] - df['TCA']) / (df['rQ'] - df['Q'])
df['xCAA']  = df['rQPct'] * 6 * (df['Played'] - df['xFW'])
df['xMPA']  = df['PCAA'] * df['xCAA']
df['SOS']   = df['CAA'] / (6 * (df['Matches']-df['FW']) * df['rQPct'])
df['xTMP']  = df['TMP'] * (df['Played'] - df['xFW']) / df['Played']
df['PWP']   = 1 / (1 + (df['xMPA'] / df['xTMP'])**1.93)
df = df.replace([np.inf, -np.inf, np.nan], 0)

df['xPts'] = (2*df['PWP']*(df['Played']-df['xFW'])) + (2*df['xFW']) - df['FL']
df['Luck'] = (df['Pts'] - df['xPts']) / 2

df['xRank'] = df.groupby('Rundle')['xPts'].rank('dense', ascending=False).astype(int)
df['LuckPctile'] = 100 * (df['Luck'].rank() - 1) / len(df)

df = df.sort_values('Luck', ascending=False)

columns = ['Player', 'Rundle', 'Branch', 'Wins', 'Losses', 'Ties', 'Pts',
           'xPts', 'Rank', 'xRank', 'MPD', 'FL', 'FW', 'xFW', 'PWP', 'QPct',
           'rQPct', 'PCAA', 'CAA', 'xCAA', 'MPA', 'xMPA', 'TMP', 'xTMP', 'Luck',
           'SOS', 'LuckPctile']

df[columns].to_csv(outfile, index=False)

tblcols = ['Player', 'Rundle', 'Wins', 'Losses', 'Ties', 'Pts', 'MPD', 'xPts', 'Luck', 'Rank', 'xRank', 'SOS']


# Now build the tables for the discussion board.  Each table has to be exactly ONE line
#   to avoid problems with the table formatter on the site.
def maketable(frame):
    s = StringIO()
    zeta = 'ζ'
    frame.to_csv(s, columns=tblcols, index=False, sep=zeta, float_format=lambda x:f'{x:.2f}')

    lines = s.getvalue().split('\n')

    out = ['[table]']
    out.append('[tr][th]')
    out.append(lines[0].replace(zeta, '[/th][th]'))
    out.append('[/th][/tr]')
    for line in lines[1:]:
        out.append('[tr][td]')
        out.append(line.replace(zeta, '[/td][td]'))
        out.append('[/td][/tr]')
    out.append('[/table]')
    return ''.join(out)

with open(luckfile, 'w') as f:
    f.write(maketable(df[0:100][tblcols]))
    f.write('\n')

with open(unluckfile, 'w') as f:
    f.write(maketable(df[-100:][tblcols]))
    f.write('\n')