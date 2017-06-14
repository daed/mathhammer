import secrets
import sys
from collections import Counter

d3 = [1, 2, 3]
d6 = [1, 2, 3, 4, 5, 6]

trials = 100000


# Shamelessly stolen from https://stackoverflow.com/questions/1665511/python-equivalent-to-atoi-atof
def atof(s):
    s, _, _ = s.partition(' ')
    while s:
        try:
            return float(s)
        except:
            s = s[:-1]
    return 0.0


def statToInt(bs):
    if '+' in bs:
        bs = bs.strip("+")
        bs = int(bs)
    return bs


def calcAttacks(num):
    if isinstance(num, str):
        if 'd' in num or 'D' in num:
            num = num.lower()
            if num.find('d') == 1:  # it's a '2d6' here, not a 'd6'
                count = num[num.find('d')-1]
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


def toHit(val):
    roll = getRoll()
    return eval(val, roll)


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


def toSave(ap, sv, inv=-1):
    roll = getRoll()
    ap = int(ap)
    if ap > 0:  # Keep ap negative
        ap = ap * -1
    roll = roll + ap  # assume ap negative
    return eval(sv, roll)


def getRoll(die=d6):
    return secrets.choice(die)


def eval(target, roll):
    if roll >= target:
        return True
    else:
        return False


def main():
    # bs s ap t sv
    if len(sys.argv) < 8:
        print("Syntax: mathhammer.py <num shots> <bs/ws> <s> <ap> <t> <sv> <d>")
        print("Syntax: mathhammer.py 20 3+ 4 0 4 3+ 1")
        print("Syntax: mathhammer.py d6 3+ 4 0 4 3+ d3")
        sys.exit(1)

    num = sys.argv[1]
    bs = sys.argv[2]
    s  = sys.argv[3]
    ap = sys.argv[4]
    t  = sys.argv[5]
    sv = sys.argv[6]
    d  = sys.argv[7]

    bs = statToInt(bs)
    ap = statToInt(ap)
    sv = statToInt(sv)
    '''
    code flow needed:
    - generate large number of rolls.  number = 3 x trials desired
    - start loop
    - test to hit
    - test to wound
    - test save
    - loop
    - report
    '''

    outcomes = []
    for i in range(0, trials):
        if i % (trials/10) == 0:
            print("Main loop:", i, "out of", trials, "complete")
        totDam = 0
        atks = calcAttacks(num)
        for x in range(0, atks):
            if toHit(bs):
                if toWound(s, t):
                    if not toSave(ap, sv):
                        dam = calcAttacks(d)
                        totDam += dam
        outcomes.append(totDam)
    print("Damage", "\t", "Outcomes", "\t", "percent")
    for x in sorted(Counter(outcomes).keys()):
        percent = '%4s' % str('%.1f' % (Counter(outcomes)[x]/(trials/100)))
        print('%6s' % x, "\t", '%8s' % Counter(outcomes)[x], "\t", percent + "%")

if __name__ == "__main__":
    main()
