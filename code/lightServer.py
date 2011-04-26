#!/usr/bin/env python


import types
import rpyc
from rpyc.utils.server import ThreadedServer
import lightUtil


N = 7


def expose_module(module):
	temp1 = module.__dict__.copy()
	for name, member in temp1.iteritems():
		if type(member) == types.FunctionType:
			print "Found function:",name
			module.__dict__["exposed_"+name] = member
		if type(member) == types.ClassType:
			print "Found class:",name
			module.__dict__["exposed_"+name] = member
			temp2 = member.__dict__.copy()
			for nam, method in temp2.iteritems():
				print "   found method:", nam
				member.__dict__["exposed_"+nam] = method

def expose_object(obj):
	temp = obj.__dict__.copy()
	for name, field in temp.iteritems():
		print "Found field:", name
		obj.__dict__["exposed_"+name] = field


expose_module(lightUtil)

room = lightUtil.lights(N)
all = lightUtil.group(room,range(N))
odd = lightUtil.group(room, range(1,N,2))
even = lightUtil.group(room, range(0,N,2))

expose_object(room)
expose_object(all)
expose_object(odd)
expose_object(even)


class lightService(rpyc.Service):

	exposed_room = room
	exposed_all = all
	exposed_odd = odd
	exposed_even = even


ls = ThreadedServer(lightService, port=1337)
ls.start()