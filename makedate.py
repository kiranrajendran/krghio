#!/usr/bin/python

##
 
 # makedate.py: creates comma separated file for use as a date dimension
 
 # The MIT License (MIT)

 # Copyright (c) 2015 Kiran Rajendran <kiran.rajendran@gmail.com>

 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:

 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.

 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
##

import datetime,csv,sys,calendar,getopt

argv = sys.argv[1:]
v_start = ''
v_ytc = ''
v_fn = ''
v_totaldays=0
if len(sys.argv) != 4:
 print 'makedate.py -s<startyear> -n<numberofyears> -o<outputfilename>\n NOTE: output includes 19000101 record'
 sys.exit(2)
try:
  opts, args = getopt.getopt(argv,"hs:n:o:")
except getopt.GetoptError:
  print 'makedate.py -s<startyear> -n<numberofyears> -o<outputfilename>\n NOTE: output includes 19000101 record'
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
     print 'makedate.py -s<startyear> -n<numberofyears> -o<outputfilename>\n NOTE: output includes 19000101 record'
     sys.exit()
  elif opt in ("-s"):
     v_start = int(arg)
  elif opt in ("-n"):
     v_ytc = int(arg)
  elif opt in ("-o"):
     v_fn = arg   

for x in range(0,v_ytc):
 v_totaldays +=  366 if  calendar.isleap(v_start+x) else 365 
#print "Total number of days: ", v_totaldays

startDate = datetime.datetime.strptime(str(v_start)+"0101","%Y%m%d")
hour_codes = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

# change outfile name to make it more descriptive
outfile=csv.writer(open(v_fn,"wb"))
# write header
# will change depending on how many fewer/addtl columns you want to output
outfile.writerow(["KEY_DATE","YYYY_CD","MM_CD","DATE_NR", \
"MNTH_SHORT_NM","MONTH_LONG_NM","MM_YYYY_CD","MMM_YYYY_CD", \
"YYYY_MM_CD","YYYY_MMM_CD","DAY_OF_WEEK","YYYY_MMM_DD_CD","QTR_CD","YYYY_QTR_CD","HALF_CD","YYYY_HALF_CD","MONTH_NR","YEAR_NR","DAY_OF_WEEK_NR","WEEK_NR"])

# output "NO VALUE" row reference
# modify this if columns in output row change
outfile.writerow([
"19000101",
"1900",
"01",
"01",
"Jan",
"January",
"01/1900",
"Jan-1900",
"1900/01",
"1900-Jan",
"Monday",
"1900-Jan-01",
"Q1",
"1900/Q1",
"H1",
"1900/H1",
"1",
"1900",
"1",
"1"])

# calculate from 1800 to the year 2999
# to figure out second #, calculate how far into the future (in days) you want to go out
# 365 x numOfYearsRetention
for x in range(1,v_totaldays) :
  # add X days
  td = startDate+datetime.timedelta(days=x)

  # isolate year month and day
  year_code  = str(td.year)
  month_code = str(td.month)
  day_code = str(td.day)
  wk_nr = str(td.isocalendar()[1])

  # calculate day of week
  # print td.weekday() 0 through 6
  dayofweek = { 6:'Sunday',0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday'}
  dayofweeknr = { 6:1,0:2,1:3,2:4,3:5,4:6,5:7}
  # fix short dates and months
  if td.month < 10 : month_code = '0' + month_code
  if td.day < 10 : day_code = '0' + day_code 

  # calculate short, long names, quarter
  shortname = { '01':"Jan" , '02':"Feb" , '03':"Mar" , '04':"Apr" , '05':"May" ,\
             '06':"Jun" , '07':"Jul" , '08':"Aug",'09':"Sep",  '10':"Oct", '11':"Nov", '12':"Dec" }
  longname = { '01':"January" , '02':"February" , '03':"March" , '04':"April" , '05':"May" ,\
             '06':"June" , '07':"July" , '08':"August",'09':"September",  '10':"October", '11':"November", '12':"December" }
  quarter = { '01':"Q1" , '02':"Q1" , '03':"Q1" , '04':"Q2" , '05':"Q2" ,\
             '06':"Q2" , '07':"Q3" , '08':"Q3",'09':"Q3",  '10':"Q4", '11':"Q4", '12':"Q4" }
  halfcode = { '01':"H1" , '02':"H1" , '03':"H1" , '04':"H1" , '05':"H1" ,\
             '06':"H1" , '07':"H2" , '08':"H2",'09':"H2",  '10':"H2", '11':"H2", '12':"H2" }

  KEY_DATE = year_code+month_code+day_code
  YYYY_CD = year_code
  # shortname[month_code]  + "    this is the long name ---> " + longname[month_code]
  #for hour_code in hour_codes: 
   # write csv
  outfile.writerow(
  [year_code+month_code+day_code,
   year_code,
   month_code,
   day_code,
   shortname[month_code],
   longname[month_code],
   month_code + "/"+year_code,
   shortname[month_code]+ "-"+year_code,
   year_code+"/"+month_code,
   year_code+"-"+shortname[month_code],
   dayofweek[td.weekday()],
   year_code+"-"+shortname[month_code]+"-"+day_code,   
   quarter[month_code],
   year_code+"/"+quarter[month_code],
   halfcode[month_code],
   year_code+"/"+halfcode[month_code],
   td.month,
   td.year,
   dayofweeknr[td.weekday()],
   wk_nr
   ])

  # uncomment this to see stop time of script print datetime.datetime.now()
print 'COMPLETED writing file', v_fn