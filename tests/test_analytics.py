import getpass
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd
import datetime

import constants as cta
import Models.Exceptions as exc
import Models.Query as query
import src.Services.database as db
import src.Services.logging as log
import src.Services.analytics as analytics


class AnalyticsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = "./tests/test_folders/test_local_DB/queries.json"
        cls.mockFileLogs = "./tests/test_folders/test_logs/queries.log"
        cls.loggingManager = log.QueryLoggerManager(cls.mockFileLogs)

        cls.analyticsManager = analytics.AnalyticsManager(cls.loggingManager, cls.mockFile)
        cls.dbManager = db.DatabaseManager(cls.mockFile)
        

        cls.queries = create_mock_queries()
        print(cls.dbManager.queriesLocalDB)
        

    def setUp(self):
        self.dbManager.clearDB()

        for query in self.queries:
            self.dbManager.addQueryToDB(query)

    
    def test_init(self):
        self.assertIsNotNone(self.analyticsManager)


    def test_get_nb_queries(self):
        res = self.analyticsManager.computeTotalQueries()

        self.assertEqual(res, len(self.queries))

    
    def test_rows_valid_data(self):
        res = self.analyticsManager.getRowsForTree()

        self.assertEqual(len(res), 5)
    
    def test_rows_invalid_data(self):
        self.dbManager.clearDB()
        res = self.analyticsManager.getRowsForTree()

        self.assertEqual(len(res), 0)


    def test_longest_exec(self):
        res = self.analyticsManager.getQueryWithLongestExecTime()

        self.assertEqual(res["execTime"], 3.15)
    
    
    def test_longest_exec_no_data(self):
        self.dbManager.clearDB()
        res = self.analyticsManager.getQueryWithLongestExecTime()

        self.assertEqual(res, {})


    def test_avg_exec(self):
        queries = self.dbManager.getQueriesFromDB()
        res = self.analyticsManager.computeAvgExecTime()
        execs = [query["execTime"] for query in queries]
        computedAvg = "{:.6f}".format(sum(execs) / 5)

        self.assertEqual(res, computedAvg)
    
    
    def test_avg_exec_no_data(self):
        self.dbManager.clearDB()
        res = self.analyticsManager.computeAvgExecTime()

        self.assertEqual(res, 0)

    
    def test_common_error(self):
        exQuery = query.Query()
        self.loggingManager.addLog("info", exQuery, "")

        self.loggingManager.addLog("error", exQuery, 
                            f"ORA-00900: invalid SQL statement Help:\nhttps://docs.oracle.com/error-help/db/ora-00900/"
                            )

        res = self.analyticsManager.getMostCommonErrorLog()

        self.assertEqual(res[1:], "ORA00900: invalid SQL statement Help:")


    # def test_common_error_empty_logs(self):
    #     self.analyticsManager.loggingManager.clearLogsFile()
    #     print(f"LOGSOGSOGOSO {self.analyticsManager.logs}")
    #     res = self.analyticsManager.getMostCommonErrorLog()

    #     self.assertEqual(res, "")


    def test_exec_times(self):
        res = self.analyticsManager.getExecTimes()

        self.assertEqual(res, [0.2, 1.0, 2.0, 1.2, 3.15])
    
    
    def test_exec_times_no_date(self):
        self.dbManager.clearDB()
        res = self.analyticsManager.getExecTimes()

        self.assertEqual(res, [])
    
    
    def test_nb_rows(self):
        res = self.analyticsManager.getNbRowsOutput()

        self.assertEqual(res, [2, 2, 2, 2, 3])
    
    
    def test_nb_rows_no_date(self):
        self.dbManager.clearDB()
        res = self.analyticsManager.getNbRowsOutput()

        self.assertEqual(res, [])


    def test_hourly_queries(self):
        res = self.analyticsManager.getNbQueriesPerHour()

        self.assertEqual(res, (
                [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            )
        )

    
    
    def test_hourly_queries_no_data(self):
        self.dbManager.clearDB()
        res = self.analyticsManager.getNbQueriesPerHour()

        self.assertEqual(res, ([], []))






def create_mock_queries() -> list:
    queries = []

    # q1
    q1 = query.Query()
    q1.initTime = datetime.datetime(2025, 8, 6, 8,  0, 0)
    # pretend these came back from the DB
    for r in [(10, "alpha"), (20, "beta")]:
        q1.rows.append(r)
    q1.endTime  = datetime.datetime(2025, 8, 6, 8,  0, 0, 200_000)  # +0.2s
    q1.execTime = q1.endTime - q1.initTime
    q1.ranBy    = getpass.getuser()
    q1.code     = "SELECT id, label FROM categories"
    q1.name     = "FetchCategories"
    q1.columns  = ["id", "label"]
    queries.append(q1)

    # q2
    q2 = query.Query()
    q2.initTime = datetime.datetime(2025, 8, 6, 9,  15, 30)
    for r in [("2025-07-01",), ("2025-07-15",)]:
        q2.rows.append(r)
    q2.endTime  = datetime.datetime(2025, 8, 6, 9,  15, 31)         # +1s
    q2.execTime = q2.endTime - q2.initTime
    q2.ranBy    = getpass.getuser()
    q2.code     = "SELECT signup_date FROM users WHERE signup_date >= '2025-07-01'"
    q2.name     = "RecentSignups"
    q2.columns  = ["signup_date"]
    queries.append(q2)

    # q3
    q3 = query.Query()
    q3.initTime = datetime.datetime(2025, 8, 6, 10, 0,  0)
    for r in [("open", 5), ("closed", 12)]:
        q3.rows.append(r)
    q3.endTime  = datetime.datetime(2025, 8, 6, 10, 0,  2)         # +2s
    q3.execTime = q3.endTime - q3.initTime
    q3.ranBy    = getpass.getuser()
    q3.code     = "SELECT status, COUNT(*) FROM tickets GROUP BY status"
    q3.name     = "TicketStatusCounts"
    q3.columns  = ["status", "count"]
    queries.append(q3)

    # q4
    q4 = query.Query()
    q4.initTime = datetime.datetime(2025, 8, 6, 11, 30, 0)
    for r in [("alice", 1001), ("bob", 1002)]:
        q4.rows.append(r)
    q4.endTime  = datetime.datetime(2025, 8, 6, 11, 30, 1, 200_000)  # +1.2s
    q4.execTime = q4.endTime - q4.initTime
    q4.ranBy    = getpass.getuser()
    q4.code     = (
        "SELECT u.username, o.order_id "
        "FROM users u JOIN orders o ON u.id = o.user_id"
    )
    q4.name     = "UserOrderJoin"
    q4.columns  = ["username", "order_id"]
    queries.append(q4)

    # q5
    q5 = query.Query()
    q5.initTime = datetime.datetime(2025, 8, 7, 12, 45, 0)
    for r in [(501, 1200.00), (502, 950.50), (503, 780.25)]:
        q5.rows.append(r)
    q5.endTime  = datetime.datetime(2025, 8, 7, 12, 45, 3, 150_000)  # +3.15s
    q5.execTime = q5.endTime - q5.initTime
    q5.ranBy    = getpass.getuser()
    q5.code     = (
        "SELECT customer_id, SUM(amount) AS total_spent "
        "FROM orders GROUP BY customer_id "
        "ORDER BY total_spent DESC FETCH FIRST 3 ROWS ONLY"
    )
    q5.name     = "TopSpenders"
    q5.columns  = ["customer_id", "total_spent"]
    queries.append(q5)

    return queries



if __name__ == '__main__':
    unittest.main(verbosity=2)