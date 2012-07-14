import re

for line in open("AAA.sub").readlines():
	m = re.match(r"(\{\d+\})(\{\d+\})(.*)", line)
	start = int(m.group(1).strip("{}"))
	end = int(m.group(2).strip("{}"))
	text = m.group(3)
	
	print "{%s}{%s}%s" % (start-600, end-600, text)

