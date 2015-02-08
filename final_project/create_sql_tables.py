
### CREATE TABLES IN THE ADVARK SQL DB

import pymysql

# Connect to Advark DB (unsecure root password usage used here in test case only)
db = pymysql.connect(host="104.236.210.19",user='root',passwd='advark79', database='advark')
cursor = db.cursor()

# Create table with UCI income training data 
cursor.execute('CREATE TABLE UCI_data ( \
               obs_id INT AUTO_INCREMENT PRIMARY KEY, \
               age INT, \
               workclass VARCHAR(255), \
               fnlwgt BIGINT, \
               education VARCHAR(255), \
               education_weight INT, \
               marital_status VARCHAR(255), \
               occupation VARCHAR(255), \
               relationship VARCHAR(255), \
               race VARCHAR(255), \
               sex VARCHAR(255), \
               capital_gain INT, \
               capital_loss INT, \
               hrs_per_wk INT, \
               native_country VARCHAR(255), \
               gt_50k TINYINT \
               )'
               )

# Create age distribution table
cursor.execute('CREATE TABLE census_county_age_dist ( \
                county_id VARCHAR(255), \
                county_id2 VARCHAR(255), \
                county_name VARCHAR(255), \
                0_5_est INT, \
                0_5_pct DOUBLE, \
                5_9_est INT, \
                5_9_pct DOUBLE, \
                10_14_est INT, \
                10_14_pct DOUBLE, \
                15_19_est INT, \
                15_19_pct DOUBLE, \
                20_24_est INT, \
                20_24_pct DOUBLE, \
                25_34_est INT, \
                25_34_pct DOUBLE, \
                35_44_est INT, \
                35_44_pct DOUBLE, \
                45_54_est INT, \
                45_54_pct DOUBLE, \
                55_59_est INT, \
                55_59_pct DOUBLE, \
                60_64_est INT, \
                60_64_pct DOUBLE, \
                65_74_est INT, \
                65_74_pct DOUBLE, \
                75_84_est INT, \
                75_84_pct DOUBLE, \
                85_g_est INT, \
                85_g_pct DOUBLE, \
                median_est DOUBLE \
               )'
               )

# Create income distribution table
cursor.execute('CREATE TABLE census_county_income_dist ( \
                county_id VARCHAR(255), \
                county_id2 VARCHAR(255), \
                county_name VARCHAR(255), \
                0_10_est INT, \
                0_10_pct DOUBLE, \
                10_15_est INT, \
                10_15_pct DOUBLE, \
                15_25_est INT, \
                15_25_pct DOUBLE, \
                25_35_est INT, \
                25_35_pct DOUBLE, \
                35_50_est INT, \
                35_50_pct DOUBLE, \
                50_75_est INT, \
                50_75_pct DOUBLE, \
                75_100_est INT, \
                75_100_pct DOUBLE, \
                100_150_est INT, \
                100_150_pct DOUBLE, \
                150_200_est INT, \
                150_200_pct DOUBLE, \
                200_g_est INT, \
                200_g_pct DOUBLE, \
                median_est DOUBLE \
               )'
               )

