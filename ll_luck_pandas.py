#!/usr/bin/env python3
import pandas as pd
import numpy  as np
import sys

df = pd.read_csv(sys.argv[1], encoding='ISO-8859-1')
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

df['xRank']      = df.groupby('Rundle')['xPts'].rank('dense', ascending=False)
df['LuckPctile'] = 100 * (df['Luck'].rank() - 1) / len(df)

df = df.sort_values('Luck', ascending=False)

columns = ['Player', 'Rundle', 'Branch', 'Wins', 'Losses', 'Ties', 'Pts',
           'xPts', 'Rank', 'xRank', 'MPD', 'FL', 'FW', 'xFW', 'PWP', 'QPct',
           'rQPct', 'PCAA', 'CAA', 'xCAA', 'MPA', 'xMPA', 'TMP', 'xTMP', 'Luck',
           'SOS', 'LuckPctile']

df[columns].to_csv(sys.argv[2], index=False)
