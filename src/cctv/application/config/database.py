import pyodbc

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=10.10.101.2;'
    'Database=MPM_IT;'
    'uid=appreader;'
    'pwd=Simpang4244;'
    'Trusted_Connection=yes;'
)