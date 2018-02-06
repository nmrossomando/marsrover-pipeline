#!/usr/bin/python3
#
# Some handy utilities that could (will) be useful.
#

# I hate datetime enough to implement this myself.
# Returns True if lhs > rhs, Returns False if lhs <= rhs
# Since timestamps are in uniform format in the manifests, this can be fairly inflexible.
def cmptime(lhs,rhs):
	# First check year
	if int(lhs[0:4]) > int(rhs[0:4]):
		return True
	elif int(lhs[0:4]) < int(rhs[0:4]):
		return False

	# Then month
	if int(lhs[5:7]) > int(rhs[5:7]):
		return True
	elif int(lhs[5:7]) < int(rhs[5:7]):
		return False

	# Then day...
	if int(lhs[8:10]) > int(rhs[8:10]):
		return True
	elif int(lhs[8:10]) < int(rhs[8:10]):
		return False

	# Hour...
	if int(lhs[11:13]) > int(rhs[11:13]):
		return True
	elif int(lhs[11:13]) < int(rhs[11:13]):
		return False

	# Minute...
	if int(lhs[14:16]) > int(rhs[14:16]):
		return True
	elif int(lhs[14:16]) < int(rhs[14:16]):
		return False

	# Finally seconds.
	if float(lhs[17:-1]) > float(rhs[17:-1]):
		return True
	elif float(lhs[17:-1]) < float(rhs[17:-1]):
		return False

	# If anything else, equal:
	return False

if __name__ == '__main__':
	print(cmptime('2019-02-05T12:00:00.000Z','2018-02-05T12:00:00.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2019-02-05T12:00:00.000Z'))
	print(cmptime('2018-03-05T12:00:00.000Z','2018-02-05T12:00:00.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2018-03-05T12:00:00.000Z'))
	print(cmptime('2018-02-06T12:00:00.000Z','2018-02-05T12:00:00.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2018-02-06T12:00:00.000Z'))
	print(cmptime('2018-02-05T13:00:00.000Z','2018-02-05T12:00:00.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2018-02-05T13:00:00.000Z'))
	print(cmptime('2018-02-05T12:10:00.000Z','2018-02-05T12:00:00.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2018-02-05T12:10:00.000Z'))
	print(cmptime('2018-02-05T12:00:10.000Z','2018-02-05T12:00:00.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2018-02-05T12:00:10.000Z'))
	print(cmptime('2018-02-05T12:00:00.000Z','2018-02-05T12:00:00.000Z'))




