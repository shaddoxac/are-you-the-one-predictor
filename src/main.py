

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

    def printMatches(self):
        if (self.isMatched()):
            print(f'{self.name} is a perfect match with {self.perfectMatch.name}!\n')
        else:
            print(f'{self.name}\'s possible matches:')
            for matchName in self.possibleMatches:
                print(f'{self.name} - {matchName}')
            print('')

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

lights = []
lights.append((2, [('Adam', 'Brittany'), ('Dre', 'Jacy'), ('Scali', 'Ashleigh'), ('Chris T', 'Jess'), ('Dillan', 'Coleysia'), ('Ethan', 'Shanley'), ('Joey', 'Paige'), ('JJ', 'Simone'), ('Ryan', 'Amber'), ('Wes', 'Kayla')]))

# lights.append((2, [('Adam', ''), ('Dre', ''), ('Scali', ''), ('Chris T', ''), ('Dillan', ''), ('Ethan', ''), ('Joey', '') ('JJ', ''), ('Ryan', ''), ('Wes', '')]))


lastIndex = 1 ## will go through the first {lastIndex} days

for i in range(0, lastIndex):
    (pairMaleName, pairFemaleName, isPerfectMatch) = truthBooths[i]
    pairMale = males[pairMaleName]
    pairFemale = females[pairFemaleName]
    # male.printMatches()
    # female.printMatches()

    if isPerfectMatch:
        pairMale.becomeMatched(pairFemale)
        pairFemale.becomeMatched(pairMale)

        for mName in males:
            males[mName].unmatch(pairFemaleName)
        for femaleName in females:
            females[fName].unmatch(pairMaleName)
    else: # no match.. :(
        pairMale.unmatch(pairFemaleName)
        pairFemale.unmatch(pairMaleName)


for maleName in males:
    males[maleName].printMatches()


# other notes
# secondary group (either males or females, arbitrary) doesn't need to be tracked, as all relationships are
# reciprocal and displayed on one group as the other. Primary group can track everything
