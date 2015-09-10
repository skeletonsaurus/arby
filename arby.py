# -*- coding:utf-8 -*-

import math
import operator
from functools import reduce
#import time
import urllib2
import ast
import networkx as nx

G = nx.DiGraph()

currencies = ['btc_usd',
              'btc_rur',
              'btc_eur',
              'ltc_usd',
              'ltc_btc',
              'ltc_rur',
              'ltc_eur',
              'nmc_btc',
              'nmc_usd',
              'nvc_btc',
              'nvc_usd',
              'usd_rur',
              'eur_usd',
              'eur_rur',
              'ppc_btc',
              'ppc_usd',]

price_dict = {}

#pair = 'btc_usd'
for i in currencies:
    base, alt = i.split("_")
    response = urllib2.urlopen('https://btc-e.com/api/2/' + i + '/ticker')
    html = response.read()
    current_price = ast.literal_eval(html)
    #print current_price
    #print base, alt
    ds = current_price['ticker']['sell']
    db = current_price['ticker']['buy']
    #print ds
    #print db
    p = (base, alt, {'weight': -1.0 * math.log(float(db))})
    b = (alt, base, {'weight': -1.0 * math.log(1/float(ds))})
    conj1 = base + '_' + alt
    conj2 = alt + '_' + base
    price_dict[conj1] = float(db)
    price_dict[conj2] = 1 / float(ds)
    #print p
    #print b
    G.add_edges_from([p])
    G.add_edges_from([b])

print 'price_dict', price_dict
neg_check = nx.negative_edge_cycle(G)
print neg_check

ub_grow = nx.astar_path(G, 'usd', 'btc')
print 'ub_grow', ub_grow
print ub_grow[-1] + '_' + ub_grow[0]

ub_moneyWalk = []

if neg_check == True:
    for i in ub_grow[1:]:
        key_finder = ub_grow[
            ub_grow.index(i) - 1] + '_' + ub_grow[(ub_grow.index(i))]
        key = price_dict[key_finder]
        print key
        #print 'key_finder', key_finder
        print price_dict[key_finder]
        ub_moneyWalk.append(key)
        print ub_moneyWalk
    end_stop = ub_grow[-1] + '_' + ub_grow[0]
    print 'end_stop', end_stop
    ub_moneyWalk.append(price_dict[end_stop])
    print 'ub_moneyWalk',  ub_moneyWalk
        #key =
    #tf = .002 * len(ub_moneyWalk)
    #print 'tf', tf
    pg = ((reduce(operator.mul, ub_moneyWalk, 1) -1) * 100)
    print 'pg * .002', pg * .002
    tf = pg - (pg * .002)
    print 'pg - tf', tf
    pgm = 100 * reduce(operator.mul, ub_moneyWalk, 1)
    print pg
    print pgm
else:
    print 'Sorry, you suck. No money for you.'
