import re

#text = "C) Od 18 let."
#first_letter = re.search(r'\b([A-Za-z])', text).group(1)

#print(first_letter)

text = "Správná odpověď: C"
last_letter = re.search(r'\b([A-Za-z])\b', text).group(1)

print(last_letter)