
s = "hello"
total  = 0
for i in range(len(s) - 1):
	current = abs(ord(s[i]) - ord(s[i+1]))
	total += current

print(total) 
