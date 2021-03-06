#!/usr/bin/env python
import os,sys
from datetime import timedelta,datetime
os.environ['DJANGO_SETTINGS_MODULE']='tacc_stats.site.tacc_stats_site.settings'
from tacc_stats.site.stampede import views
import tacc_stats.cfg as cfg
import tacc_stats.analysis as analysis

try:
    start = datetime.strptime(sys.argv[1],"%Y-%m-%d")
    end   = datetime.strptime(sys.argv[2],"%Y-%m-%d")
except:
    start = datetime.now() - timedelta(days=1)
    end   = start

for root,dirnames,filenames in os.walk(cfg.pickles_dir):
    for directory in dirnames:

        date = datetime.strptime(directory,'%Y-%m-%d')
        if max(date.date(),start.date()) > min(date.date(),end.date()): continue
        print 'Run update for',date.date()

        views.update(directory)
        
        cpi_test = analysis.HighCPI(threshold=1.0,processes=1)
        views.update_test_field(directory,cpi_test,'cpi')#,rerun=True)
        
        mbw_test = analysis.MemBw(threshold=0.5,processes=1)               
        views.update_test_field(directory,mbw_test,'mbw')   
        
        idle_test = analysis.Idle(threshold=0.999,processes=1,min_hosts=2)
        views.update_test_field(directory,idle_test,'idle')#,rerun=True)   
        
        cat_test = analysis.Catastrophe(threshold=0.001,processes=1,min_hosts=2)
        views.update_test_field(directory,cat_test,'cat')   
        
    break
