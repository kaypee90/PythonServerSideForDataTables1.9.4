__author__ = 'Asante-PC'

import MySQLdb


class DataTablesServer:

    def __init__(self):
        # Database connection information
        self.host = None
        self.db = None
        self.user = None
        self.passwd = None

        # Database Connectivity
        self.connection = None
        self.resultData = None
        self.cadinalityFiltered = 0
        self.cadinality = 0

        # DataTables Options
        self.sEcho = None
        self.sSearch = None
        self.iSortCol = None
        self.iSortingCols = None
        self.iDisplayStart = None
        self.iDisplayLength = None
        self.sSortDir = None

        self.sTable = None
        self.columns = []
        self.indexColumn = None
        self.joincolumns = []
        self.wherecolumns = []

    # Set Database Variables
    def setServerInfo(self, host, database, username, password):
        self.host = host
        self.user = username
        self.passwd = password
        self.db = database

    # Set Table Variables
    def setDatabaseInfo(self, tablenameOrJoinQuery, columns, indexColumn):
        #self.columns = columns
        self.indexColumn = indexColumn
        self.sTable = tablenameOrJoinQuery
        for Key, Value in columns:
            self.columns.append(Key)
            self.joincolumns.append(Value + " AS " + Key)
            self.wherecolumns.append(Value)

    # Create Connection To Database
    def connect(self):
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)

    # Set Datatables Variables
    def dataTablesOptions(self, echo, sortdir, sortcol, displaystart="", search = "", sortingcols = 0, displaylength = -1):
        self.sEcho = echo
        self.sSearch = search
        self.iSortCol = sortcol
        self.iSortingCols = sortingcols
        self.iDisplayStart = displaystart
        self.iDisplayLength = displaylength
        self.sSortDir = sortdir

    def getData(self):
        self.runQueries()
        return self.outputResult()

    # outputResult
    # Output the JSON required for DataTables
    #
    def outputResult( self ):
        output = '{'
        output += '"sEcho": '+str(int(self.sEcho))+', '
        output += '"iTotalRecords": '+str(self.cardinality)+', '
        output += '"iTotalDisplayRecords": '+str(self.cadinalityFiltered)+', '
        output += '"aaData": [ '

        for row in self.resultData:
            output += '['
            for i in range( len(self.columns) ):
                if (self.columns[i] == "version" ):
            # 'version' specific formatting
                    if ( row[self.columns[i] ] == "0" ):
                        output += '"-",'
                    else:
                        output += '"'+str(row[ self.columns[i] ])+'",'
                else:
            # general formatting
                    output += '"'+str(row[ self.columns[i] ]).replace('"','\\"')+'",'

            # Optional Configuration:
            # If you need to add any extra columns (add/edit/delete etc) to the table, that aren't in the
            # database - you can do it here


            output = output[:-1]
            output += '],'
        output = output[:-1]
        output += '] }'

        return output

    # Generate the SQL needed and run queries
    def runQueries(self):
        # Get the data
        dataCursor = self.connection.cursor( cursorclass=MySQLdb.cursors.DictCursor )
        dataCursor.execute( """
            SELECT SQL_CALC_FOUND_ROWS %(columns)s
            FROM   %(table)s %(where)s %(order)s %(limit)s""" % dict(
                columns=', '.join(self.joincolumns), table=self.sTable, where=self.filtering(), order=self.ordering(),
                limit=self.paging()
            ) )
        self.resultData = dataCursor.fetchall()

        cadinalityFilteredCursor = self.connection.cursor()
        cadinalityFilteredCursor.execute( """
            SELECT FOUND_ROWS()
        """ )
        self.cadinalityFiltered = cadinalityFilteredCursor.fetchone()[0]

        cadinalityCursor = self.connection.cursor()
        cadinalityCursor.execute("SELECT COUNT("+self.indexColumn+") FROM " + self.sTable)
        self.cardinality = cadinalityCursor.fetchone()[0]


    #
    # filtering
    # Create the 'WHERE' part of the SQL string
    #
    def filtering( self ):
        filter = ""
        if (self.sSearch is not None and self.sSearch != "" ):
            filter = "WHERE "
            for i in range( len(self.wherecolumns) ):
                filter += "%s LIKE '%%%s%%' OR " % (self.wherecolumns[i], self.sSearch)
            filter = filter[:-3]
        return filter


    #
    # ordering
    # Create the 'ORDER BY' part of the SQL string
    #
    def ordering( self ):
        order = ""
        if ( self.iSortingCols != "" ) and ( self.iSortingCols > 0):
            order = "ORDER BY  "
            for i in range( int(self.iSortingCols)):
                order += "%s %s, " % (self.columns[int(self.iSortCol)], \
                    self.sSortDir)
        return order[:-2]


    #
    # paging
    # Create the 'LIMIT' part of the SQL string
    #
    def paging( self ):
        limit = ""
        if ( self.iDisplayStart != "" ) and ( self.iDisplayLength != -1 ):
            limit = "LIMIT %s, %s" % (self.iDisplayStart , self.iDisplayLength )
        return limit
#

#Example - Sample Code
#############################################################################################################
#columns = [("UserId","tbl_user.user_id"),("Username","tbl_user.user_name"),("Fullname","tbl_user.user_username"),("Password","tbl_user.user_password"),("UserRole","tbl_role.Rolename")]
#joinOrtable = " tbl_user INNER JOIN tbl_role ON tbl_user.user_role = tbl_role.Id "
#
#dt = DataTablesServer()
#dt.setServerInfo("localhost","bucketlist","root","root")
#dt.setDatabaseInfo(joinOrtable,columns,"user_id")
#dt.connect()
#dt.dataTablesOptions( 3,"asc","1",0,"",1,10)
#print(dt.getData())
###############################################################################################################
