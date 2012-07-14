#!/usr/bin/env python

#
# invoked like this:
#   move_srt.py original.srt +13
#
# will move subtitles 13 seconds "later" - ie delay
#
# original:      00:03:11,755 --> 00:03:15,004
# after rewrite: 00:03:24,755 --> 00:03:28,004
# 

import sys, os

if len(sys.argv) != 3:
	print sys.argv[0] + " original.srt +13"
	sys.exit(1)


original = sys.argv[1]
offset = int(sys.argv[2])
temp = original + ".new"

out = open(temp, "w")
inn = open(original, "r")

def debug(a):
	if False:
		print a


class T:
	def __init__(self):
		self.seconds = 0
		self.minutes = 0
		self.hours = 0
		self.millis = 0


def parse(s):
	debug(s)
	t = T()
	parts = s.split(",")
	debug(parts)
	t.millis = int(parts[1])

	parts = parts[0].split(":")
	t.hours = int(parts[0])
	t.minutes = int(parts[1])
	t.seconds = int(parts[2])
	return t


def formt(t):
	return "%02d:%02d:%02d,%03d" % (t.hours, t.minutes, t.seconds, t.millis)
	

def update(t):
	t.seconds += offset
	if t.seconds < 0:
		t.minutes += -1
		t.seconds %= 60
	if t.minutes < 0:
		t.hours += -1
		t.minutes %= 60
	if t.hours < 0:
		print "warning, times offset to before start of movie - setting to zero"
		t = T()

	if t.seconds > 59:
		t.minutes += 1
		t.seconds %= 60
	if t.minutes > 59:
		t.hours += 1
		t.minutes %= 60
	
	return t

for line in inn.readlines():
	if not "-->" in line:
		out.write(line)
	else:
		parts = line.strip().split(" ")
		start = update(parse(parts[0]))
		end = update(parse(parts[2]))
		converted = "%s --> %s\r\n" % (formt(start), formt(end))
		print line, converted
		out.write(converted)

out.flush()
out.close()

os.rename(temp, original)
