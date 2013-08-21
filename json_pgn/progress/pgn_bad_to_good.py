#!/usr/bin/env python3

import json
import re
from fractions import Fraction

litteral = False

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

def parse_json(f):
    
        content = f.read()

        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)


        #print(content)

        # Return json file
        return json.loads(content)
    
def opt_litteralise(i):
    if litteral:
        if '/' in i:
            return float(Fraction(i))
        if 'B' in i or 'b' in i:
            t = re.split('B|b', i)
            return int(t[0]) * 8 + int(t[1])
        if '0x' in i:
            return int(i)
    return i
    
j = None

with open('pgns_bad.json') as f:
    #print(f.read())
    j = parse_json(f)
    
#print(j)
pgns = []
for p in j:
    #print(p)
    try:
        pgn = {}
        pgn["dsc"] = p[0]
        pgn["pgn"] = p[1]
        pgn["known"] = [2]
        pgn["size"] = p[3]
        pgn["reptFld"] = p[4]
        tfl = p[5]
        fieldList = []
        for fld in tfl:
            if fld != [0]:
                tfl = {}
                tfl['name'] = fld[0]
                tfl['size'] = opt_litteralise(fld[1])
                tfl['res'] = opt_litteralise(fld[2])
                tfl['sign'] = fld[3]
                if len(fld) > 4: tfl['units'] = fld[4]
                if len(fld) > 5: tfl['dsc'] = fld[5]
                if len(fld) > 6:
                    tfl['ofst'] = fld[6]
                fieldList.append(tfl)
        pgn["fldLst"] = fieldList
        pgns.append(pgn)
    except:
        print(p)
        raise SystemExit

print(pgns)
out = json.dumps(pgns, sort_keys=True, indent=4, separators=(',', ': '))
print(out)
with open('../pgn.json','w') as f:
    f.write(out)
    
    
    
    
    
    
    
    
    