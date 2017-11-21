import re
pattern1 = re.compile("*Server")
if pattern1.match("AdminServer"):
    print("Match")
else:
    print("No match.")
    