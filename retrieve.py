#!/usr/bin/python
#
import re
import urllib2 as www
import MySQLdb as sql
from databaseHandler import databaseHandler
from wxStnDbHandler import wxStnDbHandler
from datetime import date,timedelta,datetime
#
pretext = '[psuWxStn]'
#
# Begin Script Function Definitions
#
def parse_data_page(date,page):
  """
  Available keys:
    TMAX   TMIN   QPE   ACCSN   DESN
  """
  # Not sure where I was going with raw_regex, but I left it here for posterity.
  #raw_regex = 'High Temperature\s*:\s*(\d{2})?\s.*\n\s+Low Temperature\s*:\s*(\d{2})?\s.*\n\s+.*\n+\sRain or Liquid Equivalent\s*:\s*((?:\d\.\d{1,2})|(?:TRACE))?\s.*\n\s+Snow and\/or Ice Pellets\s*:\s*((?:\d{1,2}\.\d{1,2})|(?:TRACE))?\s.*\n\s+Snow Depth\s*:\s*((?:\d{1,2})|(?:TRACE))?\s.*\n'
  #
  # Here is the actual regular expression we will use to scan the web pages.
  regex = 'High Temperature\s*:\s*(?P<TMAX>-?\d{1,2})?\s.*\n\s+Low Temperature\s*:\s*(?P<TMIN>-?\d{1,2})?\s.*\n\s+.*\n+\sRain or Liquid Equivalent\s*:\s*(?P<QPE>(?:\d\.\d{1,2})|(?:TRACE))?\s.*\n\s+Snow and\/or Ice Pellets\s*:\s*(?P<ACCSN>(?:\d{1,2}\.\d{1,2})|(?:TRACE))?\s.*\n\s+Snow Depth\s*:\s*(?P<DESN>(?:\d{1,2})|(?:TRACE))?\s.*\n'
  match = re.search(regex,page)
  # We check if the regular expression matched, if so it must have found our information.
  if match is not None:
    # We take out variables in a dictionary from our regular expression, which is what the ?P<> tags are for.
    obs        = match.groupdict()
    max_temp   = obs['TMAX']
    min_temp   = obs['TMIN']
    precip     = obs['QPE']
    snow_ice   = obs['ACCSN']
    snow_depth = obs['DESN']
	# The regular expression gives us strings only, we need to convert to other datatypes.
    if max_temp is not None:
      max_temp_out = int(max_temp)
    else:
      max_temp_out = max_temp
    if min_temp is not None:
      min_temp_out = int(min_temp)
    else:
      min_temp_out = min_temp
    if precip is not None:
      precip_out = 0.001 if precip == "TRACE" else float(precip)
    else:
      precip_out = precip
    if snow_ice is not None:
      snow_ice_out = 0.001 if snow_ice == "TRACE" else float(snow_ice)
    else:
      snow_ice_out = snow_ice
    if snow_depth is not None:
      snow_depth_out = 0.001 if snow_depth == "TRACE" else int(snow_depth)
    else:
      snow_depth_out = snow_depth
  else:
    # If we didn't match, we can still insert nulls into the database, but we will need the date.
	# In this case we return a 1 as an error code and can use this to print to a log file.
    return (1,date,None,None,None,None,None)
  return (0,date,max_temp_out,min_temp_out,precip_out,snow_ice_out,snow_depth_out)
#
def main():
  """
  Main function of program.
  *****Note 1 *****:
    %02d tells python that I want numbers to be formatted with 
      2 places and to give me a 0 if a place is empty, so 2 becomes 02
  """
  import warnings as warn
  print pretext,'BEGIN'
  # You can insert your own MySQL information here.
  server   = <server>
  user     = <user>
  password = <password>
  database = <database>
  #
  # Getting started with our database
  _x = wxStnDbHandler(server,user,password,database)
  # We define the start and end dates, and find the difference in days between them.
  #   This difference will be used to loop across the days.
  start_date  = date(year=1896,month=1,day=1)
  end_date    = date(year=2014,month=3,day=31)
  date_diff   = end_date - start_date
  total_days  = date_diff.days
  # We start timing the function to see how long it takes to run.
  timer_start = datetime.now()
  # Anywhere we see g.write(), we are writing to the log file.
  with open('RETRIEVE.log','w') as g:
    g.write('%s: We started writing to the database.\n' % (str(datetime.now())))
	# Start looping across days, the + 1 because range() is 0-based and we need the last date as well.
    for i in range(0,total_days + 1):
	  # We are going to update the user periodically on our progress.
      if i % 500 == 0:
        print '%s: Command %s of %s issued.' % (str(datetime.now()),str(i),str(total_days + 1))
        g.write('%s: Command %s of %s issued.\n' % (str(datetime.now()),str(i),str(total_days + 1)))
      # To find our next date, we can add a length of time to our start date. Thanks drboyer
      my_date     = start_date + timedelta(days=i)
      url_to_open = 'http://www.meteo.psu.edu/~wjs1/wxstn/getsummary.php'
	  # There are different formats for posting to the website and for inserting into MySQL, we need both of them.
      web_str     = '%02d%02d%02d' % (my_date.year,my_date.month,my_date.day) # See note 1
      sql_str     = '%02d-%02d-%02d' % (my_date.year,my_date.month,my_date.day) # See note 1
      post        = 'dtg=' + web_str
      web_page    = www.urlopen(url_to_open,post)
	  # Read the web page and parse the data, we will receive a tuple from parse_data_page() which will include the MySQL date.
      full_page   = web_page.read()
      dat         = parse_data_page(sql_str,full_page)
	  # We set up the warning value in the return statement in parse_data_page(), we use that here.
      if dat[0] == 1:
	    # Going to throw a runtime warning out at you if something didn't match at all.
		#   Bill and I fixed all but one instance where this occurs.
        warn.warn("MISSING DATA at %s\n" % (sql_str),RuntimeWarning)
        g.write('%s MISSING DATA at %s\n' % (str(datetime.now()),sql_str))
      enter_this = (dat[1],dat[2],dat[3],dat[4],dat[5],dat[6])
      db_result  = _x.wxStnEnter(enter_this)
	  # Our DbHandler will return an error code and the error for us, we just have to grab it if it happens.
      if db_result[0] == 1:
        g.write('%s:%s\n' % (str(datetime.now()),db_result[1]))
    g.write('%s: We finished writing to the database. Elapsed time: %s' % (str(datetime.now()),str(datetime.now()-timer_start)))
  _x.close_db()
  return
#
# Script of file, this is only run if this file is used as a stand-alone script
#
if __name__ == "__main__":
  # Run the function main()
  main()
  # Tell the user the program ended.
  print pretext,'PYTHON STOP'
#
#
#
#
# EOF
