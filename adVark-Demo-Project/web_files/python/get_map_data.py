#!/usr/bin/env python

import sys
import json
import cgi
import csv
import numpy as np
import pandas as pd
import scipy.stats
import pickle
import pymysql
import censusDemos

# CGI setup
fs = cgi.FieldStorage()

# Get age and income ranges from client
age_high = int(fs.getlist(fs.keys()[0])[1])
age_low = int(fs.getlist(fs.keys()[0])[0])
income_high = int(fs.getlist(fs.keys()[1])[1]) * 1000
income_low = int(fs.getlist(fs.keys()[1])[0]) * 1000

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

	elif len(income_range) == 0:
		return sum(pop_counts) / float(total_pop)

	else:
		# Numer of people for a given age bin within income range
		joint_pops = []

		for i, pop in enumerate(pop_counts):
			max_cdf = scipy.stats.lognorm.cdf( income_range[1], scale=np.exp( mu[i] ), s=sigma[i] )
			min_cdf = scipy.stats.lognorm.cdf( income_range[0], scale=np.exp( mu[i] ), s=sigma[i] )
			joint_prob_bin = max_cdf - min_cdf
			joint_pops.append( pop * joint_prob_bin )

		# Calculate joint probability of being in age and income ranges
		joint_prob_age_inc = sum( joint_pops ) / float( total_pop )

		# Return joint probability
		return joint_prob_age_inc


## Calculation

# Get binned data from server
cd = censusDemos.Census_Demos()
ages_df, incomes_df, total_pop_df = cd.getSqlData([age_low, age_high], [income_low, income_high])

# General metrics from binned data
num_counties = len(ages_df)
num_age_bins = len(ages_df[0:1].columns) / 3
num_inc_bins = len(incomes_df[0:1].columns)

# Iterate through counties and calculate joint probability for each
return_df = {}
max_val = 0

for i in range(0, (num_counties - 1)):
	# Get county id
	county_id = int(ages_df[i:(i+1)].index.item())
	
	# Calculate necessary metrics
	pop_counts = [ ages_df[i:(i+1)].ix[:,bin_index][0] for bin_index in range(0, num_age_bins) ]
	mu = [ ages_df[i:(i+1)].ix[:,num_age_bins + bin_index][0] for bin_index in range(0, num_age_bins) ]
	sigma = [ ages_df[i:(i+1)].ix[:,(num_age_bins*2) + bin_index][0] for bin_index in range(0, num_age_bins) ]
	total_pop = int(total_pop_df[i:(i+1)][0])
	income_range = [income_low, income_high]
	total_in_inc_range = sum([ incomes_df[i:(i+1)].ix[:,bin_index][0] for bin_index in range(0, num_inc_bins) ])

	# Calculate joint probability
	joint_prob = get_joint_prob_age_inc(pop_counts, mu, sigma, total_pop, income_range, total_in_inc_range)
	return_df[county_id] = joint_prob

	# Update max value for scaling
	if joint_prob > max_val:
		max_val = joint_prob

# Rescale return dataframe
return_df_scaled = {}
for county, prob in return_df.items():
	new_prob = float(prob) / max_val
	return_df_scaled[county] = new_prob

# Print to TSV file
with open('../csv/mapping_data_live.tsv', mode='wb') as csv_file:
	w = csv.writer(csv_file, delimiter='\t')
    	w.writerow(['id', 'rate'])
    	for id_df, rate_df in return_df_scaled.items():
    		w.writerow([id_df, rate_df])




# Print return value
print "Content-Type: application/text"
print "\n"
print max_val



