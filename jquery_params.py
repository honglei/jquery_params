# -*- coding: utf-8 -*-
'''
orgin from https://bitbucket.org/k_bx/jquery-unparam
now sparsed to a more json-like struct. 
make it work with list well!

    sort[0][field]:tKeywords
    sort[0][dir]:desc
    sort[1][field]:tTitle
    sort[1][dir]:asc
now become: {'sort': [{'field': 'tKeywords', 'dir': 'desc'}, {'field': 'tTitle', 'dir': 'asc'}] }

auther: jhonglei@gmail.com 
'''

import re
import urlparse
from itertools import izip_longest
def parse_key_pair(key, val):
    groups = re.findall(r"\[.*?\]", key)
    groups_joined =  ''.join(groups)
    if key[-len(groups_joined):] == groups_joined:
        key = key[:-len(groups_joined)]
        for group in reversed(groups):
            index = re.match("\d+", group[1:-1])
            if group == '[]':
                val = [val]
            elif index:
                index = int(index.group())
                res = [None]*(index+1)
                res[index] =  val
                val = res            
            else:
                val = {group[1:-1]: val}
    return {key: val}  

def merge_two_structs(s1, s2):
    if isinstance(s1, list) and isinstance(s2, list):
        new_array =[]
        for item,item2 in izip_longest(s1,s2):
            if(item):
                if(item2):
                    new_item = merge_two_structs(item,item2)
                    new_array.append(new_item)
                else:
                    new_array.append(item)
            else:
                new_array.append(item2) 
        return new_array
    if isinstance(s1, dict) and \
       isinstance(s2, dict):
        
        retval = s1.copy()
        for key, val in s2.iteritems():
            if retval.get(key) is None:
                retval[key] = val
            else:
                retval[key] = merge_two_structs(retval[key], val)
        return retval
    return s2

def merge_structs(structs):
    if len(structs) == 0:
        return None
    if len(structs) == 1:
        return structs[0]
    first, rest = structs[0], structs[1:]
    return merge_two_structs(first, merge_structs(rest))

def jquery_unparam_unquoted(jquery_params):
    pair_strings = jquery_params.split('&')
    key_pairs = [parse_key_pair(x) for x in pair_strings]
    return merge_structs(key_pairs)

def jquery_unparam(jquery_params):   
    key_value_pairs= urlparse.parse_qsl(test_str)
    struct_list = [parse_key_pair(key, val) for key,val in key_value_pairs]
    result  = merge_structs(struct_list)    
    return result

def _part_test1():
    ##test1
    key,val  =  'filter[filters][0][value]', 'XXX'
    k = parse_key_pair(key,val)
    key2,value2 =  'filter[filters][2][operator]', 'TTT'    
    k2 = parse_key_pair(key2,value2)
    ##test2 join list
    from itertools import izip_longest
    a = [1, None, None, {'a':22}]
    b = [None, None,2, {'b':11},6,5]
    new_array =[]
    for item,item2 in izip_longest(a,b):
        if(item):
            if(item2):
                new_item = merge_two_structs(item,item2)
                new_array.append(new_item)
            else:
                new_array.append(item)
        else:
            new_array.append(item2)    
        #print item,item2
    print new_array
    
if __name__ == '__main__':
    '''
    take:2
    skip:0
    page:1
    pageSize:2
    sort[0][field]:tKeywords
    sort[0][dir]:desc
    sort[1][field]:tTitle
    sort[1][dir]:asc
    filter[logic]:and
    filter[filters][0][field]:EmployeeID
    filter[filters][0][operator]:eq
    filter[filters][0][value]:XXX
    group[0][field]:tTitle
    group[0][dir]:desc
    '''
    test_str = "take=2&skip=0&page=1&pageSize=2&sort%5B0%5D%5Bfield%5D=tKeywords&sort%5B0%5D%5Bdir%5D=desc&sort%5B1%5D%5Bfield%5D=tTitle&sort%5B1%5D%5Bdir%5D=asc&filter%5Blogic%5D=and&filter%5Bfilters%5D%5B0%5D%5Bfield%5D=EmployeeID&filter%5Bfilters%5D%5B0%5D%5Boperator%5D=eq&filter%5Bfilters%5D%5B0%5D%5Bvalue%5D=XXX&group%5B0%5D%5Bfield%5D=tTitle&group%5B0%5D%5Bdir%5D=desc"
    print jquery_unparam(test_str)
    # {'sort': [{'field': 'tKeywords', 'dir': 'desc'}, {'field': 'tTitle', 'dir': 'asc'}], 'group': [{'field': 'tTitle', 'dir': 'desc'}], 'pageSize': '2', 'skip': '0', 'filter': {'filters': [{'operator': 'eq', 'field': 'EmployeeID', 'value': 'XXX'}], 'logic': 'and'}, 'take': '2', 'page': '1'}



    
 
    
