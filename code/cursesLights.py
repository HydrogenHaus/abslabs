#!/usr/bin/env python

import curses
import curses.panel
import lightUtil

def cycle_list(lst, pos, dir):
    lstlen = len(lst)
    for i in range(lstlen):
        if lst[i] is pos:
            if dir=='down':
                if i==lstlen-1:
                    return lst[0]
                else:
                    return lst[i+1]
            if dir=='up':
                if i==0:
                    return lst[lstlen-1]
                else:
                    return lst[i-1]

class lightPanel:
    def __init__(self,
                 stdscr,
                 name,
                 rows, 
                 cols, 
                 ypos, 
                 xpos):
        if rows<5:
            raise Exception, 'Panel width must be atleast 5.'
        if len(name)>(cols-2):
            raise Exception, 'Name will not fit.'
        self.win = curses.newwin(rows+2,cols,ypos,xpos)
        stdscr.refresh()
        self.win.addstr(1,2,name+' '*(cols-len(name)-4),curses.color_pair(1))
        self.win.hline(2,1,'-',cols-2)
        self.win.box()
        self.panels = {}
        self.panels['main'] = curses.panel.new_panel(self.win)
        curses.panel.update_panels()
        self.total_fields = 0
        self.fields = {}
        self.rows = rows
        self.cols = cols
        self.ypos = ypos
        self.xpos = xpos
        
    def move(self,
             dir):
        dx = dy = 0
        if dir=='up':
            if self.ypos is not 3:
                dy = -1
            else:
                curses.flash()
                curses.beep()
        if dir=='down': 
            if self.ypos is not 33:
                dy = 1
            else:
                curses.flash()
                curses.beep()
        if dir=='right': 
            if self.xpos is not 82:
                dx = 2
            else:
                curses.flash()
                curses.beep()
        if dir=='left': 
            if self.xpos is not 2:
                dx = -2
            else:
                curses.flash()
                curses.beep()
        for p in self.panels:
            y, x = self.panels[p].window().getbegyx()
            self.panels[p].move(y+dy, x+dx)
            self.ypos = y+dy
            self.xpos = x+dx
        curses.panel.update_panels()

    def add_field(self,
                  key,
                  init_value=0,
                  color=0):
        self.fields[key] = [curses.newwin(1,
                                         self.cols-3,
                                         self.ypos+self.total_fields+3,
                                         self.xpos+2),
                            init_value,
                            color]
        self.panels[key] = curses.panel.new_panel(self.fields[key][0])
        self.total_fields += 1
        self.update_field(key,init_value,color)

    def update_field(self,
                     key,
                     value,
                     color):
        tot_wid = self.cols - 4
        key_wid = len(key)
        val_wid = len(str(value))
        kvc_wid = key_wid + val_wid + 1
        xtr_wid = tot_wid - kvc_wid
        if xtr_wid<=0:
            fld_str = key[:key_wid+xtr_wid] + ':' + str(value)
        else:
            fld_str = key + ':' + ' '*xtr_wid + str(value)
        self.fields[key][0].addstr(0,0,fld_str)#,curses.color_pair(color))
        self.fields[key][1] = value
        self.fields[key][2] = color
        self.fields[key][0].refresh()

    def focus_on(self,
                 key):
        for k in self.fields:
            if k is key:
                self.fields[k][0].standout()
            else:
                self.fields[k][0].standend()
            self.update_field(k,
                              self.fields[k][1],
                              self.fields[k][2])

    def remove_field(self,
                     key):
        del self.fields[key]
        self.total_fields -= 1

def main(scr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    
    room = lightUtil.lights(50)
    all = lightUtil.group(room,range(50))
    colors = {'red':127, 'green':127, 'blue':127}
    color_range = range(256)

    win = lightPanel(scr,'room',8,20,10,10)
    fields = ['red', 'green', 'blue']
    win.add_field('red',colors['red'],1)
    win.add_field('green',colors['green'],2)
    win.add_field('blue',colors['blue'],3)

    current_field = 'red'
    win.focus_on(current_field)
    all.setColor((colors['red'], colors['green'], colors['blue']))

    while True:
        c = scr.getkey()
        #scr.addstr(0,0,c)
        if c == 'KEY_UP':
            current_field = cycle_list(fields,current_field,'up')
            win.focus_on(current_field)
        if c == 'KEY_DOWN':
            current_field = cycle_list(fields,current_field,'down')
            win.focus_on(current_field)
        if c == 'KEY_RIGHT':
            colors[current_field] = cycle_list(color_range,
                                               colors[current_field],
                                               'down')
        if c == 'KEY_LEFT':
            colors[current_field] = cycle_list(color_range,
                                               colors[current_field],
                                               'up')
        if c == 'KEY_MOUSE':
            #scr.addstr(0,0,str(curses.getmouse()))
            id, x, y, z, bstate = curses.getmouse()
            for f in win.fields:
                if win.fields[f][0].enclose(y, x):
                    win.focus_on(f)
        if c == '0':
            colors[current_field] = 0
        if c == 'w':
            win.move('up')
        if c == 's':
            win.move('down')
        if c == 'a':
            win.move('left')
        if c == 'd':
            win.move('right')
        if c == 'q':
            break
        all.setColor((colors['red'], colors['green'], colors['blue']))
        win.update_field('red',colors['red'],1)
        win.update_field('green',colors['green'],2)
        win.update_field('blue',colors['blue'],3)


if __name__=="__main__":
    curses.wrapper(main)
