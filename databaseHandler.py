#!/usr/bin/python
#
import MySQLdb as sql
#
class databaseHandler:
  """
  A helpful class which can manage a database connection.
  You can use class inheritance to make new specialized versions of this class.
  """
  def __init__(self,server,username,password,database):
    """
    Initialize the database and define a cursor object
    Inputs:
      server   <string> Your server name. Use localhost if running on your machine
      username <string> Your access account name. 
      password <string> Your mysql account password.
      database <string> The database you want to use.
    Outputs: None
    """
    self.db  = sql.connect(host=server,user=username,passwd=password,db=database)
    self.cur = self.db.cursor()
    return
  #
  def close_db(self):
    """
    Closes the database.
    Inputs: None
    Outputs: None
    """
    self.db.close()
    return
  #
# End Class databaseHandler
#
if __name__ == '__main__':
  print "databaseHandler.py is not a script."
  print "PYTHON STOP"
