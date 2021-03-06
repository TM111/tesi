from FbIndexManager import *
from generic_pages_score import *
from categorized_pages_score import *
from age_score import *
from places_score import *

import datetime
import json
def index_data(token,solr, IndexManager,count):
    print 'indicizzando dati...',token
    try:
        IndexManager.takeANDindexFriends(token)
        IndexManager.takeANDindexPosts(token)
        IndexManager.takeANDindexPages(token)
        IndexManager.takeANDindexAge(token)
        
        response=solr.search(q='doc_type:friends_list OR doc_type:age',rows=pow(10,6),wt='python')
        id_list=[]
        for doc in response:
            if str(doc['user_id'][0]) not in id_list:
                id_list.append(str(doc['user_id'][0]))
        
        update_places_score(solr,id_list)
        update_age_distance(solr,id_list)
        update_generic_pages_score(solr,id_list)
        update_categorized_pages_score(solr,id_list,'music')
        update_categorized_pages_score(solr,id_list,'movies')
        update_categorized_pages_score(solr,id_list,'television')
        update_categorized_pages_score(solr,id_list,'books')
        
    except Exception as ex:
        print ex
        if count==5:
            return
        print 'riprovo!'
        index_data(token,solr, IndexManager,count+1)
    print 'finito!'
    return

def fix(time):
    time=str(time)
    if len(time)<2:
        return '0'+time
    else:
        return time
    
def update_query_history(user,query,filter,solr,count):
    if count==10:
        return
    if query=='*':
        return
    now=datetime.datetime.now()
    t=str(now.year)+'-'+fix(now.month)+'-'+fix(now.day)+'  '+fix(now.hour)+':'+fix(now.minute)
    try:
        try:
            response=solr.search(q='doc_type:history AND user:'+user,rows=1000000,wt='python')
        except:
            response=''
        solr.add([{"doc_type":"history","user":user,"type":"query","num":len(response)+1,"f":filter,'title':query,"time":t}])
    except:
        time.sleep(1)
        update_query_history(user,query,filter,solr,count+1)
    
def update_file_history(user,name,type,solr,count):
    if count==10:
        return
    now=datetime.datetime.now()
    t=str(now.year)+'-'+fix(now.month)+'-'+fix(now.day)+'  '+fix(now.hour)+':'+fix(now.minute)
    try:
        try:
            response=solr.search(q='doc_type:history AND user:'+user,rows=1000000,wt='python')
        except:
            response=''
        solr.add([{"doc_type":"history","user":user,"type":"file","num":len(response)+1,"f":type,"title":name,"time":t}])
    except:
        time.sleep(1)
        update_file_history(user,name,format,solr,count+1)
    

