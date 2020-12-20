

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

    def filterMatches(self): ## TODO, should update to remove on matches, instead of checking repeatedly
        for match in self.possibleMatches:
            if (match.isMatched()):
                self.possibleMatches.pop(match.name)

    def remainingMatches(self):
        self.filterMatches()
        return self.possibleMatches

    def printMatches(self):
        if (self.isMatched()):
            print(f'{self.name} is a perfect match with {self.perfectMatch.name}!\n')
        else:
            self.filterMatches()
            print(f'{self.name}\'s possible matches:')
            for match in self.possibleMatches:
                print(f'{self.name} - {match.name}')
            print('')

    def truthBooth(self, partner, isMatch):
        if (isMatch):
            self.becomeMatched(partner)
            partner.becomeMatched(self)
        else:
            self.possibleMatches.pop(partner.name)
            partner.possibleMatches.pop(self.name)


# TODO, could optimize by converting males and females to map[name -> object]
def get(lst, name): ## get person from name
    for p in lst:
        if (p.name == name):
            return p
    return None

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
    print(t)
    p1.truthBooth(p2, t[2])

for male in males:
    male.printMatches()
