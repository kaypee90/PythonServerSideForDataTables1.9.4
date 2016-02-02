__author__ = 'Asante-PC'

from datatables import DataTablesServer

# Database connection information
_databaseInfo = dict(
  host   = "localhost",
  user   = "",
  passwd = "",
  db     = "bucketlist")

# Indexed column (used for fast and accurate table cardinality)
_indexColumn = "user_id"

#Tupple of database columns with their alias (for JOIN feature) which should be read and sent back to DataTables
columns = [("Username","tbl_user.user_name"),("Fullname","tbl_user.user_username"),("Password","tbl_user.user_password"),("UserRole","tbl_role.Rolename"),("UserId","tbl_user.user_id")]

# DB table to use Or a join query if table is more than one.
joinOrtable = "tbl_user INNER JOIN tbl_role ON tbl_user.user_role = tbl_role.Id"

class ServerProcessing:

    dataTableData = None

    def __init__(self):
        self.dataTableData = DataTablesServer()
        self.dataTableData.setServerInfo(_databaseInfo['host'], _databaseInfo['db'], _databaseInfo['user'], _databaseInfo['passwd'])
        self.dataTableData.setDatabaseInfo(joinOrtable,columns,_indexColumn)
        self.dataTableData.connect()

    def setDataTableOptions(self, echo, sortdirection, sortcolumn, displaystart="", search = "", sortingcolumns = 0, displaylength = -1):
        self.dataTableData.dataTablesOptions(echo, sortdirection, sortcolumn, displaystart, search, sortingcolumns, displaylength)

    def getDataTableData(self):
        if(self.dataTableData is not None):
            return self.dataTableData.getData()
        else:
            return None


#Sample Code#
################################################################
#data = ServerProcessing()
#data.setDataTableOptions( 3,"asc","1",0,"",1,10) #echo sortdir sortcol displaystart search sortingcolumns displaylength
#print(data.getDataTableData())