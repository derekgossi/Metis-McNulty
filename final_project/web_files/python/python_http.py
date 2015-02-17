#!/usr/bin/env python

import sys
import json
import cgi
import numpy as np
import pandas as pd
import scipy.stats
import pickle
import pymysql

# CGI
fs = cgi.FieldStorage()

# Get age and income ranges from client
age_high = int(fs.getlist(fs.keys()[0])[1])
age_low = int(fs.getlist(fs.keys()[0])[0])
income_high = int(fs.getlist(fs.keys()[1])[1])
income_low = int(fs.getlist(fs.keys()[1])[0])

income_range = [income_high, income_low]


# Get joint probability of a target age and income range for a geographic unit
def get_joint_prob_age_inc(pop_counts, mu, sigma, total_pop, income_range, total_in_inc_range):
	# pop_counts = list of ints (or floats)
	# mu = list of floats
	# sigma = list of floats
	# total_pop is int (or float)
	# inc_range is list of exactly two ints (or floats)
	# total_in_inc_range is int (or float)

	# If pop_counts is empty or inc_range is empty, no need for joint prob
	if len(pop_counts) == 0:
		return float(total_in_inc_range) / total_pop

	elif len(inc_range) == 0:
		return sum(pop_counts) / float(total_pop)

	else:
		# Numer of people for a given age bin within income range
		joint_pops = []

		for i, pop in enumerate(pop_counts):
			max_cdf = scipy.stats.lognorm.cdf( inc_range[1], scale=np.exp( mu[i] ), s=sigma[i] )
			min_cdf = scipy.stats.lognorm.cdf( inc_range[0], scale=np.exp( mu[i] ), s=sigma[i] )
			joint_prob_bin = max_cdf - min_cdf
			joint_pops.append( pop * joint_prob_bin )

		# Calculate joint probability of being in age and income ranges
		joint_prob_age_inc = sum( joint_pops ) / float( total_pop )

		# Return joint probability
		return joint_prob_age_inc


# Test case
pop_counts = [150000, 150000, 200000]
mu = [np.log(25000), np.log(35000), np.log(55000)]
sigma = [0.8738124, 0.6553073, 0.76944741]
total_pop = 500000
inc_range = [0, 10000]
total_in_inc_range = 1000000


x = get_joint_prob_age_inc(pop_counts, mu, sigma, total_pop, inc_range, total_in_inc_range)








# Print JSON results
print "Content-Type: application/text"
print "\n"

print x
print age_high
print age_low
print income_high
print income_low



