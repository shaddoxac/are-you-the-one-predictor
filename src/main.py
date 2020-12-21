lastIndex = 10 ## will go through at most the first {lastIndex} days

class Person:
    def __init__(self, name, isMale):
        self.name = name
        self.isMale = isMale
        self.perfectMatch = None

    def setupPartners(self, possibleMatches):
        self.possibleMatches = possibleMatches.copy()

    def hasPerfectMatch(self):
        return self.perfectMatch != None

    def becomeMatched(self, other):
        self.perfectMatch = other
        # clear other matches
        self.possibleMatches = {(other.name, other)}

    def isPerfectMatchWith(self, other):
        return self.hasPerfectMatch() and self.perfectMatch.name == other.name

    def printMatches(self):
        if (self.hasPerfectMatch()):
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
lights.append((4, [('Adam', 'Shanley'), ('Dre', 'Ashleigh'), ('Scali', 'Simone'), ('Chris T', 'Paige'), ('Dillan', 'Jess'), ('Ethan', 'Amber'), ('Joey', 'Brittany'), ('JJ', 'Jacy'), ('Ryan', 'Kayla'), ('Wes', 'Coleysia')]))
lights.append((2, [('Adam', 'Brittany'), ('Dre', 'Ashleigh'), ('Scali', 'Paige'), ('Chris T', 'Simone'), ('Dillan', 'Coleysia'), ('Ethan', 'Amber'), ('Joey', 'Shanley'), ('JJ', 'Jess'), ('Ryan', 'Kayla'), ('Wes', 'Jacy')]))

# lights.append((2, [('Adam', ''), ('Dre', ''), ('Scali', ''), ('Chris T', ''), ('Dillan', ''), ('Ethan', ''), ('Joey', ''), ('JJ', ''), ('Ryan', ''), ('Wes', '')]))



for i in range(0, min(lastIndex, len(truthBooths))):
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
        for fName in females:
            females[fName].unmatch(pairMaleName)
    else: # no match.. :(
        pairMale.unmatch(pairFemaleName)
        pairFemale.unmatch(pairMaleName)


# handle [0-lastIndex] lights
for i in range (0, min(lastIndex, len(lights))):
    (unknownLights, testedMatches) = lights[i]
    possibleMatches = 10 ## will decrement as 'wrong' matches are discovered

    toExamine = []

    for (maleMatchName, femaleMatchName) in testedMatches:
        maleMatch = males[maleMatchName]
        femaleMatch = females[femaleMatchName]

        if maleMatch.isPerfectMatchWith(femaleMatch):
            # treat this case as a known, can disregard 1 light
            unknownLights -= 1
            possibleMatches -= 1
        elif femaleMatchName in maleMatch.possibleMatches:
            # matches are reciprocal, only have to check one
            # these are possible, let's look at the odds after seeing all couples
            toExamine.append((maleMatch, femaleMatch))
        else:
            # can't be a match
            possibleMatches -= 1

    print(f'{unknownLights} of the next {len(toExamine)} are matches!')
    # print(unknownLights)
    # print(len(toExamine))
    odds = (unknownLights * 100.0) / len(toExamine) # assuming an even distribution across all matched couples
    for (maleMatch, femaleMatch) in toExamine:
        print(f'{maleMatch.name} and {femaleMatch.name} have {odds}% of being a match')
        if (odds == 0):
            male.unmatch(female.name)
            female.unmatch(male.name)


for maleName in males:
    males[maleName].printMatches()


# other notes
# secondary group (either males or females, arbitrary) doesn't need to be tracked, as all relationships are
# reciprocal and displayed on one group as the other. Primary group can track everything
