from __future__ import print_function
import sys
import os

sys.path.append("/Users/alexegg/Development/dse/DSE203_etl/final/yadi/")
from yadi.datalog2sql.datalog2sqlconverter import Datalog2SqlConverter
from yadi.sql_engine.query_evaluator import QueryEvaluator
from yadi.sql_engine.db_state_tracker import DBStateTracker
from colorama import *
from yadi.interpreter.interpreter_parse import *
from yadi.interpreter.syntax_highlighter import SyntaxHighlight
import sys
import os

qe = QueryEvaluator()
db_state_tracker = DBStateTracker(qe)
converter = Datalog2SqlConverter(db_state_tracker)

input_line = "tweets_by_nishara(T) :- tuser(UID, 'nishara'), tweet(_, T, _, UID)."

is_assertion = False
sql_queries = converter.convertDatalog2Sql(input_line, is_assertion)

print(sql_queries)