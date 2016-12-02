import sys
import os

sys.path.append("/Users/alexegg/Development/dse/DSE203_etl/final/nrdatalog2sql/src/")

import networkx as nx
from collections import defaultdict
import itertools

from datalog.model import Variable
import datalog.yacc

def rule2sfw(rule) :
    ''' convert a rule to a SFW block '''
    # SELECT att_0, att2 FROM ... WHERE ...
    var2LiteralsMap = defaultdict(list)
    # { var : (leteral, term_index, literal_index) }
    for k,lit in enumerate(rule.body):
        for (i,t) in enumerate(lit.terms):
            var2LiteralsMap[t].append((lit,i,k))

    vars = [ 'atom_%d.att_%d ' % (rule.body.index(lit_idx[0]), lit_idx[1])
      for (lit_idx, var) in ((var2LiteralsMap[term][0], term) 
                             for term in rule.head.terms #if isinstance(term, Variable)
            )]

    vars = [ '%s AS att_%d' % (v,i) for i,v in enumerate(vars)]

    s = "\n SELECT DISTINCT %s " % ",".join(vars)

    f = "\n FROM\n%s" % ",\n".join(
        ["%s AS atom_%d" % (literal.predicate, index) 
         for index, literal in enumerate(rule.body)])

    conds = list(itertools.chain (*[["atom_%d.att_%d = atom_%d.att_%d" % 
                                     (lit_idx_lst[0][2], lit_idx_lst[0][1], 
                                      lit_idx_lst[k][2], lit_idx_lst[k][1]) 
                                for k in xrange(1, len(lit_idx_lst))]
                               for lit_idx_lst in var2LiteralsMap.values()]))

    if len(conds):
        w = "\n WHERE " + " AND ".join(conds)
    else:
        w = ""

    sfw = "(%s %s %s)" % (s, f, w)
    return sfw
    
    
def rules2cte(rules) :
    '''convert rules with a common head predicate to a cte'''
    #"%s AS (SELECT ... UNION SELECT ... UNION ... )"
    return "%s AS (%s)" % (rules[0].head.predicate, 
                           ( " UNION\n ").join(rule2sfw(rule) for rule in rules))
                           
# type_ defined in owlgres
# - 1 : concept
# - 2 : object property
# - 3 : data property
# - 4 : annotation type
def edb2sfw(predicate, encode, type_):
    if type_ == 1:
        return ('%s AS ( \n'
                '  SELECT ca.individual AS att_0 \n'
                '  FROM concept_assertion AS ca \n' 
                '  WHERE concept = %d \n'
                ')') % (predicate, encode)
    elif type_ == 2:
        return ('%s AS ( \n' 
                '  SELECT ora.a AS att_0, ora.b AS att_1 \n' 
                '  FROM object_role_assertion AS ora \n' 
                '  WHERE object_role = %d \n' 
                ')') % (predicate, encode)
    elif type_ == 3:
        return ('%s AS ( \n' 
                '  SELECT dra.a AS att_0, dra.b AS att_1 \n'
                '  FROM data_role_assertion AS dra \n'
                '  WHERE data_role = %d \n' 
                ')') % (predicate, encode)

def read_tbox_name(fname):
  print fname
  with open(fname) as f:
      f.next()
      f.next()
      # { prdicate : (id, type) }
      return { frag(sp[4].strip()) : (int(sp[0].strip()), int(sp[1].strip()))  
               for sp in (line.strip().split('|')  
                          for line in f) if len(sp)==5 if '#' in sp[4]}
                          
def frag(url):
    return url[url.rindex('#')+1:]

def main(datalog_str, lut):
    #{ predicate_name -> (encode, arity) }
    vocab =  read_tbox_name(lut)
    
    parser = datalog.yacc.parser
    datalogString = datalog_str
    program = parser.parse(datalogString)
    G = nx.DiGraph()
    for rule in program.rules:
        for body_literal in rule.body:
            G.add_edge(body_literal.predicate, rule.head.predicate)
    
    depends = nx.topological_sort(G)
    
    sql = "WITH \n %s ,\n" % ",\n".join([ edb2sfw(p, *vocab.get(p)) 
                               for p in (set(depends) & set(vocab.keys()))])

    ctes = [rules2cte(rules) for rules in 
            ([r for r in program.rules if r.head.predicate == p] # rules for p
             for p in depends) 
            if len(rules) ]

    sql += ",\n".join(ctes)

    sql += "\n SELECT * FROM %s" % depends[-1]
    
    print sql
    
datalog_query= "q1(x,y) :- GTD(x,y)."
q2="gtd(eventid,_,_,....., country_txt = 'Iraq', related)"
main(datalog_query, "/Users/alexegg/Development/dse/DSE203_etl/final/nrdatalog2sql/data/LUT.txt")