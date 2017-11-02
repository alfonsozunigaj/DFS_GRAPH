# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 18:58:13 2017

@author: ALFONSO
"""
from numpy import random
#import inspect

class node:
    v = None
    cons = []
    father = None
    def __init__(self, v, father):
        self.v = v
        self.cons = []
        self.father = father

    def add_conn(self, Node):
        self.cons.append([self.v, Node.v])
        Node.cons.append([self.v, Node.v])

#""" Retorna la linea del programa actual """        
#def lineno():
#    return inspect.currentframe().f_back.f_lineno
        
""" Retorna el valor (key) del nodo con el que 'actual' puede formar un back edge """ #None en caso de que no exista dicho nodo
def search_for_back(actual, ancestor):
    if ancestor == None:
        return None
    elif [actual.v, ancestor.v] not in actual.cons:
        return ancestor.v
    elif ancestor.father is None:
        return None
    return search_for_back(actual, ancestor.father)
    
""" Retorna el valor (key) del nodo que puede formar un forward edge con el actual""" #None en caso de que no exista dicho nodo
def search_for_forward(actual, ancestor):
    if ancestor == None or actual.father.v == ancestor.v:
        return None
    elif [actual.v, ancestor.v] not in actual.cons:
        return ancestor.v
    elif ancestor.father is None:
        return None
    return search_for_forward(actual, ancestor.father)

""" Retorna el nodo que puede hacer cross edge con el nodo actual """     #None en caso de que no exista dicho nodo
def search_for_cross(actual, ancestor, nodes, stack):
    if ancestor == None:
        return None, None
    aux_node = ancestor
    ancestors = []
    ancestors_values = []
    while aux_node != None:
        ancestors.append(aux_node)
        ancestors_values.append(aux_node.v)
        aux_node = aux_node.father
    for i in stack:
        if i not in ancestors and i != actual and [actual.v, i.v] not in actual.cons and [i.v, actual.v] not in actual.cons:
            #print str(i.v), "ENCONTRE UN NO ANCESTRO DE", str(actual.v)
            return i, None
    return random.choice(ancestors), -1
    
""" Toma el ultimo nodo visto y hace tree edge con el, creando un nuevo nodo para el grafo """
def enlarge_graph(nodes, stack, t): 
    if t > 0:
        new = node(stack[-1].v+1, stack[-1])
        nodes[-1].add_conn(new)
        #print "se creo el nodo "+str(new.v)+" en la linea", lineno() - 1
        nodes.append(new)
        stack.append(new)
        return None   
    print -1
    exit(1)
    
def enlarge_graph_cross(nodes, stack, t, root): 
    if t > 0:
        new = node(stack[-1].v+1, root)
        root.add_conn(new)
        #print "se creo el nodo "+str(new.v)+" en la linea", lineno() - 1
        nodes.append(new)
        stack.append(new)
        return None   
    print -1
    exit(1)
    
def print_state(message, nodes, stack, t, b, f, c):
    print "\n"+message
    for i in nodes:
        print i.v, ":", i.cons
    print "actual:", stack[-1].v, "\tt:", t, "\tb:", b, "\tf:", f, "\tc:", c


data_in = raw_input().split()
t = int(data_in[0])
b = int(data_in[1])
f = int(data_in[2])
c = int(data_in[3])
initial = True
nodes=[]
stack = []
nodes.append(node(1,None))
stack.append(nodes[-1])
accion = ""
while t+b+f+c > 0:
    accion = random.randint(1,4)
    if accion == 1 and b > 0:
        for i in range(2):
            go_to_node = search_for_back(stack[-1], stack[-1].father)
            if go_to_node == None:
                enlarge_graph(nodes, stack,t)
                t -= 1
                continue
            stack[-1].add_conn(nodes[go_to_node-1])
            #print "se unio el nodo "+str(stack[-1].v)+" a "+str(nodes[go_to_node-1].v)+" en la linea", lineno() - 1
            b -= 1
            break
        #print_state("Se agreego un back edge", nodes, stack, t, b, f, c)
    
    elif accion == 2 and f > 0:
        go_to_node = search_for_forward(stack[-1], stack[-1].father)
        while go_to_node == None:
            enlarge_graph(nodes, stack,t)
            t -= 1
            go_to_node = search_for_forward(stack[-1], stack[-1].father.father)
        nodes[go_to_node-1].add_conn(stack[-1])
        #print "se unio el nodo "+str(nodes[go_to_node-1].v)+" a "+str(stack[-1].v)+" en la linea", lineno() - 1
        f -= 1
        #print_state("Se agrego un forward edge", nodes, stack, t, b, f, c)
        
    elif accion == 3 and c > 0:
        go_to_node = search_for_cross(stack[-1], stack[-1].father, nodes, stack)
        if go_to_node[0] == None:
            enlarge_graph(nodes, stack, t)
            t -= 1
            go_to_node = search_for_cross(stack[-1], stack[-1].father, nodes, stack)
        if go_to_node[1] == -1:
            enlarge_graph_cross(nodes, stack, t, go_to_node[0])
            t-= 1
            go_to_node = search_for_cross(stack[-1], stack[-1].father, nodes, stack)
        stack[-1].add_conn(go_to_node[0])
        #print "se unio el nodo "+str(stack[-1].v)+" a "+str(go_to_node[0].v)+" en la linea", lineno() - 1
        c -= 1
        #print_state("Se agrego un cross edge", nodes, stack, t, b, f, c)
    else:
        if b+f+c > 0:
            continue
        while t > 0:
            enlarge_graph(nodes, stack,t)
            t -= 1

print len(nodes)
for i in nodes:
    connections = 0
    for k in i.cons:
        if k[0] == i.v:
            connections += 1
    print connections,
    for j in i.cons:
        if j[0] == i.v:
            print j[1],
    print ""
#print "actual:", stack[-1].v, "\tt:", t, "\tb:", b, "\tf:", f, "\taccion:", accion