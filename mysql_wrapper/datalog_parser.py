import re
  
class DatalogParser(object):
  """Datalog parser & SQL generator"""
  
  columns = ["eventid", "iyear", "imonth", "iday", "approxdate", "extended", "resolution", "country", "country_txt", "region", "region_txt", "\
      provstate", "city", "latitude", "longitude", "specificity", "vicinity", "location", "summary", "crit1", "crit2", "crit3", "doubtterr", "\
      alternative", "alternative_txt", "multiple", "success", "suicide", "attacktype1", "attacktype1_txt", "attacktype2", "\
      attacktype2_txt", "attacktype3", "attacktype3_txt", "targtype1", "targtype1_txt", "targsubtype1", "targsubtype1_txt", "\
      corp1", "target1", "natlty1", "natlty1_txt", "targtype2", "targtype2_txt", "targsubtype2", "targsubtype2_txt", "corp2", "target2", "\
      natlty2", "natlty2_txt", "targtype3", "targtype3_txt", "targsubtype3", "targsubtype3_txt", "corp3", "target3", "natlty3", "\
      natlty3_txt", "gname", "gsubname", "gname2", "gsubname2", "gname3", "ingroup", "ingroup2", "ingroup3", "gsubname3", "motive", "\
      guncertain1", "guncertain2", "guncertain3", "nperps", "nperpcap", "claimed", "claimmode", "claimmode_txt", "claim2", "claimmode2", "\
      claimmode2_txt", "claim3", "claimmode3", "claimmode3_txt", "compclaim", "weaptype1", "weaptype1_txt", "weapsubtype1", "\
      weapsubtype1_txt", "weaptype2", "weaptype2_txt", "weapsubtype2", "weapsubtype2_txt", "weaptype3", "weaptype3_txt", "\
      weapsubtype3", "weapsubtype3_txt", "weaptype4", "weaptype4_txt", "weapsubtype4", "weapsubtype4_txt", "weapdetail", "\
      nkill", "nkillus", "nkillter", "nwound", "nwoundus", "nwoundte", "property", "propextent", "propextent_txt", "propvalue", "\
      propcomment", "ishostkid", "nhostkid", "nhostkidus", "nhours", "ndays", "divert", "kidhijcountry", "ransom", "ransomamt", "\
      ransomamtus", "ransompaid", "ransompaidus", "ransomnote", "hostkidoutcome", "hostkidoutcome_txt", "nreleased", "addnotes", "\
      scite1", "scite2", "scite3", "dbsource", "INT_LOG", "INT_IDEO", "INT_MISC", "INT_ANY", "related"]
  def __init__(self, arg):
    super(DatalogParser, self).__init__()
    self.arg = arg
  
  def parse(self, datalog_str):
    """input is datalog string & output is sql string"""
    
    separator = ":-"
    dummy = "_"
    allowed_comparisons = '=|!=|>|<|<=|>='

    #seperate the left and right side of the datalog string input
    left = datalog_str.split(separator )[0]
    right = datalog_str.split(separator )[1]

    return_table = left[:left.find("(")]
    return_select = [c.strip() for c in left[left.find("(")+1:left.find(")")].split(',')]

    from_table = right.split('(')[0]
    query = [q.strip() for q in right[right.find("(")+1:right.find(")")].split(',')]
    predicates_constraint_all = [q.strip() for q in right[right.find(")"):].split(',')][1:]
    predicates_constraint_dict= {}
    predicates_constraint_dict= {}
    i=0
    for p in predicates_constraint_all:
        i+=1
        operator = re.findall(r'(['+allowed_comparisons + ']+)',p)[0].strip()
        key = p[:p.find(operator)].strip()
        value =  p[p.find(operator)+len(operator):].strip()
        predicates_constraint_dict[key+'_'+str(i)] = [operator, value]
    

    predicates= {}
    select = {}
    index=0
    for q in query:
        if (q!=dummy and (q not in return_select)):
            predicates[DatalogParser.columns[index]]= q
        if (q!=dummy and (q in return_select)):
            select[DatalogParser.columns[index]]= q
        index+=1
    
    ## DN added this    
    def iserror(value):
        try:
            isinstance(int(value), (int,float))
            return True
        except ValueError:
            return False
        
    where_equality ={}
    where_inequality = {}
    for key, value in predicates.iteritems():
        if (value[0]=="'"):
            where_equality [key] = value
        elif iserror(value): ## DN added this
            where_equality [key] = value
        else:
            where_inequality [value] = key
            
    create_view_clause = "CREATE VIEW "+return_table+ " AS"
    select_clause = "SELECT "+ ", ".join(x+" AS "+y for x,y in select.iteritems())
    from_clause = "FROM "+ from_table


    if len(where_inequality)>0: ## DN added this
        where_clause = "WHERE "+", ".join(x+" = "+y for x,y in where_equality.iteritems())+ ', '+\
        ", ".join(where_inequality[x[:x.find('_')]]+y+z for x,[y,z] in predicates_constraint_dict.iteritems())
    else: ## DN added this
        where_clause = "WHERE "+", ".join(x+" = "+y for x,y in where_equality.iteritems())
        
    if len(where_equality)>0 or len(where_inequality)>0: ## DN added this
        sql_str = select_clause +" "+ from_clause +" "+ where_clause ## DN removed create view
    else: ## DN added this
        sql_str = select_clause +" "+ from_clause ## DN added this and removed create view
            
    return sql_str
    
if __name__ == '__main__':
  parser = DatalogParser("asf")
  dl_query = "DB1(s1) :- GTD(_, 2013, 12, _, _, _, _, _,'Iraq', _, _, _, _, _, _, _, _, _, s1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _)"
  sql_query =  parser.parse(dl_query)
  print sql_query