import pymysql
import pandas as pd
import numpy as np

class Census_Demos(object):
    '''queries SQL server and processes requested Data'''
    def __init__(self):
            #initialize constants for sql retrieval 
            self.incomeEstimateColumns = [
            '0_10_est',
            '10_15_est',
            '15_25_est',
            '25_35_est',
            '35_50_est',
            '50_75_est',
            '75_100_est',
            '100_150_est',
            '150_200_est',
            '200_g_est'
            ]

            self.ageEstimateColumns = [
            '0_5_est',
            '5_9_est',
            '10_14_est',
            '15_19_est',
            '20_24_est',
            '25_34_est',
            '35_44_est',
            '45_54_est',
            '55_59_est',
            '60_64_est',
            '65_74_est',
            '75_84_est',
            '85_g_est'
            ]

            self.ageMedColumns = [
            '0_5_med',
            '5_9_med',
            '10_14_med',
            '15_19_med',
            '20_24_med',
            '25_34_med',
            '35_44_med',
            '45_54_med',
            '55_59_med',
            '60_64_med',
            '65_74_med',
            '75_84_med',
            '85_g_med'
            ]

            self.ageMuColumns = [
            '0_5_mu',
            '5_9_mu',
            '10_14_mu',
            '15_19_mu',
            '20_24_mu',
            '25_34_mu',
            '35_44_mu',
            '45_54_mu',
            '55_59_mu',
            '60_64_mu',
            '65_74_mu',
            '75_84_mu',
            '85_g_mu'
            ]
            self.ageSigmaColumns = [
            '0_5_sigma',
            '5_9_sigma',
            '10_14_sigma',
            '15_19_sigma',
            '20_24_sigma',
            '25_34_sigma',
            '35_44_sigma',
            '45_54_sigma',
            '55_59_sigma',
            '60_64_sigma',
            '65_74_sigma',
            '75_84_sigma',
            '85_g_sigma'
            ]


    def getSqlData(self, ageRange, incomeRange):
        '''Top layer function.  Finds income and age values in the range of queries. 
        For range bounds inside census bins, a uniform distribution is assumed
        across age/income and sliced according to range percentage.   
        ----
        Inputs:  ageRange, incomeRange = [lower bound, upper bound]
        Outputs:  df_age:  corrected age bins and medians for each county, 
                         df_income:  corrected income bins and medians for each county,
                         df_total_people:  total people in each county (index) '''


        # Return appropriate columns and fractions for end 
        # values for income and ages before SQL query 

        age_col_names, age_end_Fractions, mu_col_names, sigma_col_names \
        = self.getAgeBinIDX(ageRange)

        inc_col_names, inc_end_Fractions = self.getIncomeBinIDX(incomeRange)

        # insert 'county_id' to find county_id values.  
        age_col_names.insert(0, 'county_id2')
        inc_col_names.insert(0, 'county_id2')
        mu_col_names.insert(0, 'county_id2')
        sigma_col_names.insert(0, 'county_id2')

        # concatenate strings of column names for pymysql
        age_col_names = ','.join(age_col_names)
        inc_col_names = ','.join(inc_col_names)
        mu_col_names = ','.join(mu_col_names)
        sigma_col_names = ','.join(sigma_col_names)

        # if queries are from the same bin, change preprossing 
        if age_col_names[0]==age_col_names[1]:
            sameColAge = True
            age_end_Fractions = age_end_Fractions[1] - age_end_Fractions[0]
        else:
            sameColAge = False

        if inc_col_names[0]==inc_col_names[1]:
            sameCol_Inc = True
            inc_end_Fractions = inc_end_Fractions[1] - inc_end_Fractions[0]
        else:
            sameCol_Inc = False

        # assign database origin
        db = pymysql.connect(host="104.236.210.19",  
            user = 'root',
            passwd = 'advark79',
            db = 'census_county_demos')

        # query SQL database  for age values and adjust fractional bins
        df_age = pd.read_sql(
            'SELECT %s FROM census_county_age_dist' %age_col_names,
             db, index_col = 'county_id2')
        df_age.iloc[:, 0] = df_age.iloc[:, 0].apply( lambda x: x*age_end_Fractions[0])

        # query SQL database  for median age values
        df_mu_age = pd.read_sql(
            'SELECT %s FROM census_county_age_dist' %mu_col_names,
             db, index_col = 'county_id2')

        df_sigma_age = pd.read_sql(
            'SELECT %s FROM census_county_age_dist' %sigma_col_names,
             db, index_col = 'county_id2')
        
        # if queries are from the same bin, change preproccesing 
        if not sameColAge:
            df_age.iloc[:, -1] = df_age.iloc[:, -1].apply( lambda x: x*age_end_Fractions[1])    

        # query SQL database  for age values and adjust fractional bins
        df_income = pd.read_sql(
            'SELECT %s FROM census_county_income_dist' %inc_col_names,
             db, index_col = 'county_id2')
        df_income.iloc[:, 0] = df_income.iloc[:, 0].apply( lambda x: x*age_end_Fractions[0])


        # if queries are from the same bin, change preprossing 
        if not sameCol_Inc:
            df_income.iloc[:, -1] = df_income.iloc[:, -1].apply( lambda x: x*age_end_Fractions[1])    

        # Find total number of people for each county 
        allAgeCols = self.ageEstimateColumns
        allAgeCols.insert(0, 'county_id2')
        df_total_people = pd.read_sql(
             'SELECT %s FROM census_county_age_dist' 
             % ','.join(allAgeCols),
              db, index_col = 'county_id2').sum(axis=1)
        df_age = pd.concat([df_age, df_mu_age, df_sigma_age], axis=1)
        
        return df_age, df_income, df_total_people

    def getAgeBinIDX(self, ageRange):
        '''Finds index of bins that contain the range of the query 
           input: ageRange = [<lower bound>,<upper bound>]
           output:'''
        #Initialize constants
        Range_high = ageRange[1]
        Range_low = ageRange[0]

        Age_Lower_Edges = np.array(
            [0,5,10,15,20,25,35,45,55,60,65,75,85])

        Age_Higher_Edges = Age_Lower_Edges[1:]-1

        Age_Higher_Edges = np.append(Age_Higher_Edges, 100)


        #find bin for low bound
        if Range_low==0:
            firstBin = 0;
        else:
            firstBin = np.flatnonzero(Age_Lower_Edges <= Range_low)[-1] 


        #find bin for high bound
        lastBin = np.flatnonzero(Age_Higher_Edges >= Range_high)[0]


        high_edge = Age_Lower_Edges[lastBin]    
        low_edge = Age_Higher_Edges[firstBin]


        lowBinWidth = Age_Higher_Edges[firstBin] - Age_Lower_Edges[firstBin] 
        highBinWidth = Age_Higher_Edges[lastBin] - Age_Lower_Edges[lastBin] 

        lowFraction = (low_edge-Range_low)/float(lowBinWidth)
        highFraction = (Range_high-high_edge)/float(highBinWidth)

        sql_Column_names = []
        sql_Column_names.extend(self.ageEstimateColumns[ firstBin: lastBin+1])
        # med_Column_names = self.ageMedColumns[ firstBin: lastBin+1]
        mu_Column_names = self.ageMuColumns[ firstBin: lastBin+1]
        sigma_Column_names = self.ageSigmaColumns[ firstBin: lastBin+1]
        

        return sql_Column_names, [lowFraction, highFraction], \
                    mu_Column_names, sigma_Column_names

    def getIncomeBinIDX(self, incomeRange):
        '''Finds index of bins that contain the range of the query 
           input: incomeRange = [<lower bound>,<upper bound>]
           output:'''
        #Initialize constants
        Range_high = incomeRange[1]/1000
        Range_low = incomeRange[0]/1000

        Income_Lower_Edges = np.array(
            [0,10,15,25,35,50,75,100,150,200])

        Income_Higher_Edges = Income_Lower_Edges[1:]-.0001
        Income_Higher_Edges = np.append(Income_Higher_Edges, 500)

        
        #find bin for low bound
        if Range_low==0:
            firstBin = 0;
        else:
            firstBin = np.flatnonzero(Income_Lower_Edges <= Range_low)[-1] 


        #find bin for high bound
        lastBin = np.flatnonzero(Income_Higher_Edges >= Range_high)[0]
        
        high_edge = Income_Lower_Edges[lastBin]    
        low_edge = Income_Higher_Edges[firstBin]

        lowBinWidth = Income_Higher_Edges[firstBin] - Income_Lower_Edges[firstBin] 
        highBinWidth = Income_Higher_Edges[lastBin] - Income_Lower_Edges[lastBin] 

        lowFraction = (low_edge-Range_low)/float(lowBinWidth)
        highFraction = (Range_high-high_edge-1)/float(highBinWidth)



        sql_Column_names = []
        sql_Column_names.extend(self.incomeEstimateColumns[firstBin: lastBin+1])
        return sql_Column_names, [lowFraction, highFraction]






        
        
        
        

