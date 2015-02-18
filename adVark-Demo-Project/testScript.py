from censusDemos import *

cD = Census_Demos()
ageRange = [23,54]
incomeRange =[22000, 43000]
# a,b = cD.getIncomeBinIDX(incomeRange)
# print a
# print b

# print '----------'
# print '----------'

# c,d = cD.getAgeBinIDX(ageRange)   
# print c
# print d

print cD.getSqlData(ageRange, incomeRange)