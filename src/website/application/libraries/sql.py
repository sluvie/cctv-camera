import pymssql


class SQL:

    server = "10.10.106.72"
    user = "appreader"
    password = "Simpang4244"

    def __init__(self) -> None:
        self.conn = pymssql.connect(server=self.server,user=self.user,password=self.password,database='master')
        pass

    def list_db(self):
        # Create a Cursor object
        cur = self.conn.cursor()

        cur.execute("SELECT name FROM master.sys.databases where is_broker_enabled = 0") 
        rows = []
        for x in cur.fetchall():
            rows.append({
                "name": x[0]
            })
        return (rows)


    def list_table(self, databasename):

        conn = pymssql.connect(server=self.server,user=self.user,password=self.password,database=databasename)

        # Create a Cursor object
        cur = conn.cursor()

        # Execute the query: To get the name of the tables from my_database
        cur.execute("select table_name, table_type from information_schema.tables order by table_type, table_name") # where table_schema = 'tableowner'
        rows = []
        for x in cur.fetchall():
            rows.append({
                "table_name": x[0],
                "table_type": x[1]
            })
        return (rows)


    def info_table(self, databasename, tablename):

        conn = pymssql.connect(server=self.server,user=self.user,password=self.password,database=databasename)

        # Create a Cursor object
        cur = conn.cursor()

        # Execute the query: To get the name of the tables from my_database
        cur.execute("select column_name, ordinal_position, is_nullable, data_type, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{}' order by ordinal_position".format(tablename)) # where table_schema = 'tableowner'
        rows = []
        for x in cur.fetchall():
            rows.append({
                "column_name": x[0],
                "ordinal_position": x[1],
                "is_nullable": x[2],
                "data_type": x[3],
                "character_maximum_length": x[4],
                "numeric_precision": x[5],
            })
        return (rows)


    def execute_query_html(self, databasename, query):

        max_row = 5
        conn = pymssql.connect(server=self.server,user=self.user,password=self.password,database=databasename)

        # split
        sqlCommands = query.split(';')

        # Create a Cursor object
        cur = conn.cursor()


        result = ""
        for command in sqlCommands:         # Execute every command
            try:
                # find column
                cur_column = conn.cursor()
                cur_column.execute("SELECT name FROM sys.dm_exec_describe_first_result_set('{}', NULL, 0) ;".format(command))
                
                table_head = ""
                table_head = table_head + "<thead>"
                for row_column in cur_column:
                    table_head = table_head + "<td style='color:black;'>" + str(row_column[0]) + "</td>"
                table_head = table_head + "</thead>"

                cur.execute(command)
                idx = 1
                result = result + "<table border='1' width='100%'>"
                result = result + table_head
                for row in cur:                    
                    if idx < max_row:
                        result = result + "<tr>"
                        for col in row:
                            result = result + "<td style='color:black;'>" + str(col) + "</td>"
                        result = result + "</tr>"
                    idx = idx + 1
                result = result + "</table>"
            except pymssql.DatabaseError as e:
                result = "<span style='color:red;'>" + result + str(e) + "</span><br /><br />"
                continue

            result = result + "<br />"

        return result