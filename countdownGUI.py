#!/usr/bin/env python

import gtk, gobject
import os.path as path
from datetime import datetime
from threading import Thread
from time import sleep
import sys

gtk.gdk.threads_init()

def resource(*args):
    resourcePath = path.join(*args)
    if hasattr(sys,'_MEIPASS'):
        return path.join(sys._MEIPASS,resourcePath)
    else:
        return path.join(path.dirname(path.abspath(sys.argv[0])),
                         resourcePath)

class GUI(object):
    def __init__(self):
        #uiFile = path.join(path.dirname(path.abspath(__file__)),'countdownGUI.ui')
        uiFile = resource('countdownGUI.ui')
        self.b = gtk.Builder()
        self.b.add_from_file(uiFile)
        self.window = self.b.get_object('mainWindow')
        self.window.connect('delete_event',gtk.main_quit)
        
        self.start = None
        self.end = None
        self.format = '%Y-%m-%d %H:%M:%S'
        t = Thread(target=self.RegularUpdate)
        t.daemon = True
        t.start()

        self.startBox = self.b.get_object('startTime')
        self.startBox.connect('changed',self.FromCellEdit)
        self.endBox = self.b.get_object('endTime')
        self.endBox.connect('changed',self.FromCellEdit)
    def FromCellEdit(self,*args):
        try:
            self.start = datetime.strptime(self.startBox.get_text(),self.format)
            self.b.get_object('outStart').set_text(self.start.strftime(self.format))
        except ValueError:
            pass
        try:
            self.end = datetime.strptime(self.endBox.get_text(),self.format)
            self.b.get_object('outEnd').set_text(self.end.strftime(self.format))
        except ValueError:
            pass
    def RegularUpdate(self):
        while True:
            self.Update()
            sleep(1)
    def Update(self,*args):
        now = datetime.now()
        if self.start is not None:
            s = str(now-self.start)
            s = s[:s.index('.')]
            gobject.idle_add(self.b.get_object('timeSpent').set_text,s)
        if self.end is not None:
            s = str(self.end-now)
            s = s[:s.index('.')]
            gobject.idle_add(self.b.get_object('timeRemaining').set_text,s)
        if (self.start is not None and
            self.end is not None):
            frac = (now-self.start).total_seconds()/(self.end-self.start).total_seconds()
            gobject.idle_add(self.b.get_object('progress').set_fraction,
                             frac)
            gobject.idle_add(self.b.get_object('progress').set_text,
                             '{0:.4f}%'.format(100*frac))
                             
    def Show(self):
        self.window.show_all()

if __name__=='__main__':
    g = GUI()
    g.window.set_keep_above(True)
    g.startBox.set_text('2013-06-02 14:00:00')
    g.endBox.set_text('2014-07-12 14:00:00')
    g.Show()
    gtk.main()
