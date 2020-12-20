

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
                self.possibleMatches.remove(match)

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
            self.possibleMatches.remove(partner)
            partner.possibleMatches.remove(self)


# TODO, could optimize by converting males and females to map[name -> object]
def get(lst, name): ## get person from name
    for p in lst:
        if (p.name == name):
            return p
    return None

maleNames = ['Adam', 'Dre', 'Scali', 'Chris T', 'Dillan', 'Ethan', 'Joey', 'JJ', 'Ryan', 'Wes']
males = list(map(lambda name: Person(name, True), maleNames))

femaleNames = ['Amber', 'Ashleigh', 'Brittany', 'Coleysia', 'Jacy', 'Jess', 'Kayla', 'Paige', 'Shanley', 'Simone']
females = list(map(lambda name: Person(name, False), femaleNames))

for male in males:
    male.setupPartners(females)

for female in females:
    female.setupPartners(males)


truthBooths = [('Chris T', 'Shanley', False), ('Ethan', 'Jess', False), ('Dillan', 'Jess', False), ('JJ', 'Simone', False), ('Dre', 'Ashleigh', False), ('Dillan', 'Coleysia', True), ('Chris T', 'Paige', True), ('Ryan', 'Kayla', False)]

for t in truthBooths:
    p1 = get(males, t[0])
    p2 = get(females, t[1])
    p1.truthBooth(p2, t[2])

for male in males:
    male.printMatches()
