import re
str='10x+4=7x+7'
l=re.split('[+=-]',str)
print(l)
words=[(w,i)for i,w in enumerate (l)]
print(words)