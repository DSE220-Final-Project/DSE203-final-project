class DatalogParser(object):
  """docstring for DatalogParser"""
  def __init__(self, arg):
    super(DatalogParser, self).__init__()
    self.arg = arg
  
  def parse(self, datalog_str):
    """input is datalog string & output is sql string"""
    # TODO parsing logic here!
    sql_str = "select * from gtd limit 2"
    return sql_str
    