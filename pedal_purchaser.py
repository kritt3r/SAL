# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:26:56 2019

@author: prana
"""
#
#import pandas as pd
#import win32 as pyapp
#import os as os
#import time
#import tkinter as tk
#

    
import os as os 
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import urllib.request as urlreq
import time
import win32com.client as win32
import pandas as pd


outlook = win32.Dispatch('outlook.application')

#Change Directory
os.chdir('C://SAL')
os.getcwd()
os.listdir()

the_url = 'https://messages.google.com/web/conversations/236?redirected=true'
bike_frame = 'https://standert.de/collections/umlaufbahn/products/umlaufbahn-ep-3-frameset-deep-space-black-1'
pedals = 'https://heusinkveld.com/products/sim-pedals/sim-pedals-sprint/?v=7516fd43adaa'

me = 'pranav_singh@live.com'
kyle = 'Kpgmccabe@gmail.com'


#Opens a specific page
def page_get(url):
    r = rq.get(url)
    return r 

def search(words):
    words = words.split()
    url = 'https://duckduckgo.com\?q=' + '+'.join(words)
    return page_get(url)

def links(url):
    page = page_get(url).content
    soup = bs(page, 'html.parser')
    for link in soup.findAll('a', attrs={'href': re.compile('^https://')}):
        print(link.get('href'))
        
def snippet(req, text, extra_char = 1000):
    loc = req.text.find(text)
    return req.text[loc-100:loc +extra_char]

#def main(url = the_url, wait_time = 180,rec = kyle):
#    splitter = '}'
#    page_before = page_get(url).text
#    page_before_split = page_before.split(splitter)
#    
#    page_now = page_before
#    while page_now == page_before:
#        print('Not yet...')
#        page_now= page_get(url).text
#        page_now_split = page_now.split(splitter)
#        print('Now length: %s\nBefore length: %s' % (len(page_now_split),len(page_before_split)))
#        time.sleep(wait_time)
#    emailer(rec)   
#    range_beg = min([len(page_now_split),len(page_before_split)])
#    range_end = min([10, abs(len(page_now_split) - len(page_before_split))])
#    print('Now length: %s\nBefore length: %s' % (len(page_now_split),len(page_before_split)))
#    for line in range(range_beg,range_end):
##        print('Now on line %s' % line)
#        line = line + 1
#    for print_lines in range(10):
#        if print_lines + 1 == len(page_now_split):
##            print(len(page_now_split))
#            return('FIN')
#        print('before line %s: %s' % (line,page_before_split[line + print_lines ] ))
#        print('now line %s: %s' % (line,page_now_split[line + print_lines ] ))


def main():
    while True:
        look_up()
        emailer()
        emailer(rec = me)
                
    
def emailer(rec = kyle, body = 'YOUR SHIT IS HERE'):
    mail = outlook.CreateItem(0)
    mail.To = rec
    mail.Subject = 'Stock Alert'
    mail.Body  = body
    mail.Send()
    
def look_up(url = pedals,search_word = 'stock',wait_time = 180):
    df = pd.DataFrame()
    splitter = '}'
    page = page_get(url).text
    df['before'] = page.split(splitter)
    df['now'] = df['before']
    
    df['keyword'] = df.apply(lambda x: search_word in x['before'], axis = 1)
    df['match'] = df.apply(lambda x: x['before'] == x['now'],axis = 1)
    print(df[df['keyword'] == True]['match'].head())
    while df[df['keyword'] == True]['match'].any():
        print('Not yet...')
        page = page_get(url).text
        df['now'] = page.split(splitter)
        df['match'] = df.apply(lambda x: x['before'] == x['now'],axis = 1)
        time.sleep(wait_time)
    print(df[df['keyword'] == True])