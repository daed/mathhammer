#!/usr/bin/python3

import secrets
import sys
from collections import Counter

d3 = [1, 2, 3]
d6 = [1, 2, 3, 4, 5, 6]

'''
You can change this value if it takes too long to do a calculation.  A larger number takes longer
but will give a more 'average' list of outcomes, while a smaller number will be faster but give a
list of outcomes that are more probable to have spikes in them.
'''
trials = 10000


# Shamelessly stolen from https://stackoverflow.com/questions/1665511/python-equivalent-to-atoi-atof
# Converts ascii to floats
def atof(s):
    s, _, _ = s.partition(' ')
    while s:
        try:
            return float(s)
        except:
            s = s[:-1]
    return 0.0

# Converts BS, WS, or Sv to an int for math.  E.x. 3+ to 3
def statToInt(bs):
    if '+' in bs:
        bs = bs.strip("+")
    bs = int(bs)
    return bs

# Turns dice notation into something useful.
# e.x. 2d6 into some value from 2-12
def calcAttacks(num):
    if isinstance(num, str):
        if 'd' in num or 'D' in num:
            num = num.lower()
            if num.find('d') == 1:  # it's a '2d6' here, not a 'd6'
                count = int(num[num.find('d')-1])
            else:
                count = 1
            size = num[num.find('d')+1]
            x = 0
            attacks = 0
            # print("calcAttacks(): number of d6s counted:", count)
            while x < count:
                if size == '6':
                    die = d6
                else:
                    die = d3
                attacks += getRoll(die)
                x += 1
        else:
            attacks = int(num)
    else:
        attacks = num
    # print("calcAttacks(): number of attacks:", attacks)
    return attacks

# Rolls a die and tells you if you hit.  Opt will let you reroll 1s, reroll any,
# or none of the above.
def toHit(val, opt=""):
    roll = getRoll()
    # Reroll 1s
    if opt == "-r1":
        if roll == 1:
            roll = getRoll()
    # Reroll all failed
    elif opt == "-r":
        if not eval(val, roll):
            roll = getRoll()
    return eval(val, roll)

# Rolls a die and compares the die to toughness and tells you if you hit.
def toWound(s, t):
    roll = getRoll()
    if s >= 2 * t:    # s = 10 t = 5
        val = 2
    elif s > t:       # s = 9  t = 5
        val = 3
    elif s == t:      # s = 5  t = 5
        val = 4
    elif s <= t / 2:  # s = 3  t = 6
        val = 6
    elif s < t:       # s = 4  t = 5
        val = 5
    else:
        print("toWound(): Unexpected Value!")
    return eval(val, roll)

# Rolls a die and tells you if you saved.  Invulnerable saves accepted as parameter
# but not currently implemented.
def toSave(ap, sv, inv=-1):
    roll = getRoll()
    ap = int(ap)
    if ap > 0:  # Keep ap negative
        ap = ap * -1
    roll = roll + ap  # assume ap negative
    return eval(sv, roll)

# Basic die roll.  Also accepts d3 as a value.
def getRoll(die=d6):
    return secrets.choice(die)

# All math in 40k is based on rolling higher than something else.
def eval(target, roll):
    if roll >= target:
        return True
    else:
        return False


def main():
    if len(sys.argv) < 8:
        print("Syntax: mathhammer.py <num shots> <bs/ws> <s> <ap> <t> <sv> <d> <opt>")
        print("Syntax: mathhammer.py 20 3+ 4 0 4 3+ 1")
        print("Syntax: mathhammer.py d6 3+ 4 0 4 3+ d3")
        print("Syntax: mathhammer.py d6 3+ 4 0 4 3+ d3 -r1")
        print("Syntax: <opt> can be blank, -r or -r1")
        print("Syntax: -r allows to reroll all failed to-hit")
        print("Syntax: -r1 allows to reroll all 1s to-hit")
        sys.exit(1)

    # check for optional reroll parameter
    if len(sys.argv) >= 9:
        opt = sys.argv[8]
    else:
        opt = ""

    num = sys.argv[1]
    bs_org = sys.argv[2]
    s  = sys.argv[3]
    ap = sys.argv[4]
    t  = sys.argv[5]
    sv_org = sys.argv[6]
    d  = sys.argv[7]

    # Sanitize inputs
    s = statToInt(s)
    t = statToInt(t)
    bs = statToInt(bs_org)
    ap = statToInt(ap)
    sv = statToInt(sv_org)

    # Roll some pretend dice and store outcomes.
    outcomes = []
    for i in range(0, trials):
        if i % (trials/10) == 0:
            print("Main loop:", i, "out of", trials, "complete")
        totDam = 0
        atks = calcAttacks(num)
        for x in range(0, atks):
            if toHit(bs, opt):
                if toWound(s, t):
                    if not toSave(ap, sv):
                        dam = calcAttacks(d)
                        totDam += dam
        outcomes.append(totDam)

    # Formulate a nice report.
    # TODO: consider altering report to something more forum friendly.
    desc = ""
    if opt == "-r1":
        desc = "Reroll 1s to hit"
    elif opt == "-r":
        desc = "Reroll all to hit"
    print("\n\n")
    print("A: %s S: %s AP: %s D: %s @ BS or WS: %s  %s" % (num, s, ap, d, bs_org, desc))
    print("vs T: %s sv %s" % (t, sv_org))
    print("Damage", "\t", "Outcomes", "\t", "percent")
    for x in sorted(Counter(outcomes).keys()):
        percent = '%4s' % str('%.1f' % (Counter(outcomes)[x]/(trials/100)))
        print('%6s' % x, "\t", '%8s' % Counter(outcomes)[x], "\t", percent + "%")


# Run main loop (above)
if __name__ == "__main__":
    main()
