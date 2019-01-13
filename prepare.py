import pandas as pd

df = pd.read_csv('scrapped.csv', encoding='utf-8')

df = df[df.group != 'Non inscrits']
df['group'] = df.group.replace('\s', ' ', regex=True)

changes = pd.read_csv('group_changes.csv', encoding='utf-8')
for row in changes.itertuples():
    df.loc[df.group == row.old_group, 'group'] = row.has_become

df.loc[(df.pour > df.contre) & (df.pour > df.abstention), 'consigne'] = 'pour'
df.loc[(df.abstention > df.contre) & (df.abstention > df.pour), 'consigne'] = 'abstention'
df.loc[(df.contre > df.abstention) & (df.contre > df.pour), 'consigne'] = 'contre'

df.loc[df.consigne == 'pour', 'dissent'] = 1 - (df.pour / (df.pour + df.contre + df.abstention))
df.loc[df.consigne == 'contre', 'dissent'] = 1 - (df.contre / (df.pour + df.contre + df.abstention))
df.loc[df.consigne == 'abstention', 'dissent'] = 1 - (df.abstention / (df.pour + df.contre + df.abstention))

df = df[['date', 'group', 'dissent']]
df.to_csv('prepared.csv', index=False)
