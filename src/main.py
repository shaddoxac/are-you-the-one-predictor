

class Person:
    def __init__(self, name, isMale):
        self.name = name
        self.isMale = isMale
        self.perfectMatch = None

    def setupPartners(self, possibleMatches):
        self.possibleMatches = possibleMatches.copy()

    def isMatched(self):
        return self.perfectMatch != None

    def becomeMatched(self, other):
        self.perfectMatch = other

    def remainingMatches(self):
        return self.possibleMatches

    def printMatches(self):
        if (self.isMatched()):
            print(f'{self.name} is a perfect match with {self.perfectMatch.name}!\n')
        else:
            print(f'{self.name}\'s possible matches:')
            for matchName in self.possibleMatches:
                print(f'{self.name} - {matchName}')
            print('')

    def failedMatch(self, partner):
        self.unmatch(partner.name)
        partner.unmatch(self.name)

    def unmatch(self, value):
        if value in self.possibleMatches:
            self.possibleMatches.pop(value)



maleNames = ['Adam', 'Dre', 'Scali', 'Chris T', 'Dillan', 'Ethan', 'Joey', 'JJ', 'Ryan', 'Wes']
males = dict(map(lambda name: (name, Person(name, True)), maleNames))

femaleNames = ['Amber', 'Ashleigh', 'Brittany', 'Coleysia', 'Jacy', 'Jess', 'Kayla', 'Paige', 'Shanley', 'Simone']
females = dict(map(lambda name: (name, Person(name, False)), femaleNames))

for maleName in males:
    males[maleName].setupPartners(females)

for femaleName in females:
    females[femaleName].setupPartners(males)


truthBooths = []
truthBooths.append(('Chris T', 'Shanley',  False))
truthBooths.append(('Ethan',   'Jess',     False))
truthBooths.append(('Dillan',  'Jess',     False))
truthBooths.append(('JJ',      'Simone',   False))
truthBooths.append(('Dre',     'Ashleigh', False))
truthBooths.append(('Dillan',  'Coleysia', True))
truthBooths.append(('Chris T', 'Paige',    True))
truthBooths.append(('Ryan',    'Kayla',    False))

for t in truthBooths:
    p1 = males[t[0]]
    p2 = females[t[1]]

    # print(t)
    # p1.printMatches()
    # p2.printMatches()

    if (t[2]):
        p1.becomeMatched(p2)
        p2.becomeMatched(p1)
        # p1.perfectMatch(p2)
        for maleName in males:
            males[maleName].unmatch(p2)
        for femaleName in females:
            females[femaleName].unmatch(p1)
    else: # no match.. :(
        p1.failedMatch(p2)

for maleName in males:
    males[maleName].printMatches()
