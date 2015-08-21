__author__ = 'ronfe'


tableFile = '1415results/esp1.csv'

f = open(tableFile).readlines()

# fetch teams list
teams = []
for each in f:
    teams.append(each.split(',')[0])

results = []
for each in f:
    matches = each.strip().split(',')
    teamName = matches[0]
    matches = matches[1:]
    rivals = list(teams)
    rivals.remove(teamName)
    tempStrings = []
    for i in range(0, len(matches)):
        tempStrings.append(teamName + ',' + rivals[i] + ',' + matches[i] + '\n')

    results = results + tempStrings

f = open(tableFile, 'w')
for each in results:
    f.write(each)

f.close()