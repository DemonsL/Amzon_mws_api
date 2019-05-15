# coding: utf-8

def set_param_list(param_list, param_name):
    i, resp = 1, ''
    for param in param_list.split(','):
        resp += '&{pn}.{i}='.format(pn=param_name, i=i) + param
        i += 1
    return resp