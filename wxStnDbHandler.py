#!/usr/bin/python
#
from databaseHandler import databaseHandler
#
class wxStnDbHandler(databaseHandler):
  """
  wxStnDbHandler extends databaseHandler
  """
  def wxStnEnter(self,d):
    """
    Enters data into the database. Takes a specific format for this specialized purpose.
    Inputs:
      d <tuple> Tuple with data as in: (date,tmax,tmin,qpe,accsn,desn)
        date:  The date of the observation, formatted for MySQL
        tmax:  Max temperature from the observation
        tmin:  Min temperature from the observation
        qpe:   Quantitative Precipitation Estimate - observed precipitation
        accsn: Accumulated Snow - Snow/Pellets observation
        desn:  Depth of Snow - Snow depth observation
    Outputs:
      return <tuple> Tuple with data as in: (code_number,message)
        code_number: 1 or 0, 1 Means that an error occurred in writing data in the database, 0 for success.
        message:     <string> or <None>, Holds error message if an error occurs.
    """
    sql_command  = 'insert into psuWxStn (date,tmax,tmin,qpe,accsn,desn) values (%s,%s,%s,%s,%s,%s)'
    values       = (d[0],d[1],d[2],d[3],d[4],d[5])
    full_command = 'insert into psuWxStn (date,tmax,tmin,qpe,accsn,desn) values (%s,%s,%s,%s,%s,%s)' % (d[0],d[1],d[2],d[3],d[4],d[5])
    try:
      self.cur.execute(sql_command,values)
      self.db.commit()
    except:
      self.db.rollback()
      error = 'Problems! Command is below:\n%s\n' % (full_command)
      return (1,error)
    return (0,None)
  #
# End class wxStnDbHandler
#
if __name__ == '__main__':
  print 'wxStnDbHandler is not a script!'
  print 'PYTHON STOP'
#
#
#
#
# EOF