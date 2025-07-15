# Oracle credentials
USERNAME = "AJWTQPRODREADONLYDEV"
CONNECTION_STRING = "AW-CA1A-QTM-P01:1521/cctl"


# Oracle Instant Client DLL files
#
########################################
#
# The current oracledb library runs on thin mode, which supports passwords verifiers 11G and later,
# but the current Oracle account was created with 10G.
#   - Option 1 : change password for the database user
#   - Option 2 (below) : Install Oracle Instant Client (https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
#                        and put the directory to be used for the connection
#
########################################
LIB_DIR = r"C:\Users\Gabriel.Louka\oracle instant client\instantclient_23_8"
