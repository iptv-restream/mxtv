#!/usr/bin/python3
# -*- coding: utf-8 -*-

### based on hypnotix 
### https://github.com/linuxmint/hypnotix

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys
import warnings
import mpv
import threading
from os import path as fpath, linesep

warnings.filterwarnings("ignore")

        
class MyWindow(Gtk.Window):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
    
        
    def my_zoom(self, widget, event):
        if not self.sidebar.is_visible():                  
            w, h = self.win.get_size()
            direction = event.get_scroll_deltas()[2]
            if direction < 0:
                if not w > 1250:
                    self.win.resize(w + 30, (w + 30) / 1.777777778)
            elif direction > 0:
                if not w < 260:
                    self.win.resize(w - 30, (w - 30) / 1.777777778)
                    
    def msgbox(self, message):
        dialog = Gtk.Dialog(title="Message", flags=0)
        dialog.set_name("msgbox")
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        dialog.set_default_size(250, 200)

        label = Gtk.Label()
        label.set_text(message)
        box = dialog.get_content_area()
        box.add(label)       
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("playlist imported")

        dialog.destroy()
                    
    ####### import playlist #######
    def import_playlist(self):
        dlg = Gtk.FileChooserDialog(title="Please choose a file", parent=None, action = 0)
        dlg.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                     "Open", Gtk.ResponseType.OK)
                     
        filter = Gtk.FileFilter()
        filter.set_name("Playlists")
        filter.add_pattern("*.m3u")
        dlg.add_filter(filter)
        response = dlg.run()

        if response == Gtk.ResponseType.OK:
             infile = (dlg.get_filename())
             print("FileName:", infile)
             dlg.destroy()
             self.parse_playlist(infile)
             self.msgbox("Saved as mychannels10.txt\n\nShortcut 0")
        else:
            dlg.destroy()
        
        
    def parse_playlist(self, infile):
        t = open(infile, "r").read()
        text = linesep.join([s for s in t.splitlines() if s])
        chList = []
        urlList = []
        mlist = text.splitlines()

        for line in mlist:
            if line.startswith("#EXTINF"):
                ch = line.partition('tvg-name="')[2].partition('" ')[0]
                if ch == "":
                    ch = line.partition(',')[2]
                chList.append(ch)
            if line.startswith("http"):
                urlList.append(line)
        outfile = f"{home_folder}/mychannels10.txt"
        with open(outfile, "w") as f:
            for x in range(len(chList)):
                if not "***" in chList[x]:
                    f.write(f"{chList[x].replace('Pluto ', '').replace(' Made In Germany', '')},{urlList[x]}\n")
                    
        f.close()
        self.makeList(outfile)
            
    def showHelp(self):
        help_text = """Shortcuts
1 to 9 -> load list 1 to 9
f -> toggle Fullscreen
Escape -> leave Fullscreen
s -> toggle Sidebar
wheel -> Zoo in/out
q -> Quit
Key Up -> next Channel
Key Down -> previous Channel
Key Plus -> more Volume
Key Minus -> less Volume
i -> import m3u
d -> hide/show titlebar
"""
        self.msgbox(help_text)
            
    def on_key_press_event(self, widget, event):
        if not self.searchbar.has_focus():
            if event.keyval == Gdk.KEY_F1:
                self.showHelp()
            # toggle titlebar
            if event.keyval == Gdk.KEY_d:
                self.on_decoration()
            if event.keyval == Gdk.KEY_q:
                Gtk.main_quit()
            if event.keyval == Gdk.KEY_i:            
                self.import_playlist()
            if self.channelbox.is_visible():
                ### lists
                if event.keyval == Gdk.KEY_1:
                    if fpath.isfile(self.file_list[0]):
                        self.makeList(self.file_list[0])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_2:
                    if fpath.isfile(self.file_list[1]):
                        self.makeList(self.file_list[1])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_3:
                    if fpath.isfile(self.file_list[2]):
                        self.makeList(self.file_list[2])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_4:
                    if fpath.isfile(self.file_list[3]):
                        self.makeList(self.file_list[3])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_5:
                    if fpath.isfile(self.file_list[4]):
                        self.makeList(self.file_list[4])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_6:
                    if fpath.isfile(self.file_list[5]):
                        self.makeList(self.file_list[5])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_7:
                    if fpath.isfile(self.file_list[6]):
                        self.makeList(self.file_list[6])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_8:
                    if fpath.isfile(self.file_list[7]):
                        self.makeList(self.file_list[7])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_9:
                    if fpath.isfile(self.file_list[8]):
                        self.makeList(self.file_list[8])
                        self.vbox.show()
                if event.keyval == Gdk.KEY_0:
                    if fpath.isfile(self.file_list[9]):
                        self.makeList(self.file_list[9])
                        self.vbox.show()
                    # toggle sidebar
                if event.keyval == Gdk.KEY_s:
                    self.toggleSideBar()  
            else:
                    # volume up
                if event.keyval == Gdk.KEY_plus:
                    if self.mpv.volume < 205:
                        self.mpv.volume += 5.0
                        self.volume = self.mpv.volume
                    print(f"Volume: {self.mpv.volume}")
                    # volume down
                if event.keyval == Gdk.KEY_minus: 
                    if self.mpv.volume >= 5:
                        self.mpv.volume -= 5.0
                        self.volume = self.mpv.volume
                    print(f"Volume: {self.mpv.volume}")
                    # toggle sidebar
                if event.keyval == Gdk.KEY_s:
                    self.toggleSideBar()            
                if event.keyval == Gdk.KEY_f or \
                     (self.fullscreen and event.keyval == Gdk.KEY_Escape):
                    self.toggle_fullscreen()
                    # next
                if self.is_playing:
                    if event.keyval == Gdk.KEY_Up:
                        child = self.channelbox.get_child_at_index(self.id + 1)
                        self.channelbox.select_child(child)
                        self.id += 1
                        self.play_async(self.nameList[self.id], self.urlList[self.id])
                        # previous
                    if event.keyval == Gdk.KEY_Down:
                        child = self.channelbox.get_child_at_index(self.id - 1)
                        self.channelbox.select_child(child)
                        self.id -= 1
                        self.play_async(self.nameList[self.id], self.urlList[self.id]) 
                    
    def on_decoration(self, *args):
        self.toggleSideBar()
        self.toggle_decoration()
                    
    def toggle_decoration(self):
        if self.win.get_decorated():
            if self.vbox.is_visible():
                w, h = self.win.get_size()
                self.vbox.show()
                self.win.resize(h * 2.2, h)
            else:
                w, h = self.win.get_size()
                self.vbox.hide()
                self.win.resize(h * 1.77 , h)
            self.win.set_decorated(False)
        else:
            if self.vbox.is_visible():
                w, h = self.win.get_size()
                self.vbox.show()
                self.win.resize(h * 2.2, h)
            else:
                w, h = self.win.get_size()
                self.vbox.hide()
                self.win.resize(h * 1.77 , h)
            self.win.set_decorated(True)
            
    def toggle_fullscreen(self, *args):
        self.fullscreen = (not self.fullscreen)
        if self.fullscreen:
            # Fullscreen
            self.win.fullscreen()
            self.vbox.hide()
        else:
            # Normal
            self.win.unfullscreen()
            self.vbox.show()
            
    def toggleSideBar(self):
        if self.vbox.is_visible():
            w, h = self.win.get_size()
            self.vbox.hide()
            self.win.resize(h * 1.77, h)
        else:
            w, h = self.win.get_size()
            self.vbox.show()
            self.win.resize(h * 2.2 , h)
            
    def btn_clicked(self, wdg, i):
        self.play_async(self.nameList[i], self.urlList[i])
        child = self.channelbox.get_child_at_index(i)
        self.channelbox.select_child(child)
        #if self.sidebar.is_visible():
        #    self.toggleSideBar()
        self.id = i
        
    def on_mpv_player_realize(self, widget):
        self.reinit_mpv()

    def reinit_mpv(self):
        if self.mpv != None:
            self.mpv.stop()

        self.mpv = mpv.MPV(volume=str(self.volume), input_cursor=True, hwdec=False, 
                                input_default_bindings=False, border=False, osd_color='#d3d7cf', 
                                osd_blur=2, cursor_autohide=1000, 
                                input_vo_keyboard=False, osc=False, ontop=True, 
                                wid=str(self.mpv_player.get_window().get_xid()))

    def reinit_mpv_movies(self):
        if self.mpv != None:
            self.mpv.stop()

        self.mpv = mpv.MPV(volume=str(self.volume), input_cursor=True, hwdec=False, 
                                input_default_bindings=False, border=False, osd_color='#d3d7cf', 
                                osd_blur=2, cursor_autohide=1000, 
                                input_vo_keyboard=False, osc=True, ontop=True, 
                                wid=str(self.mpv_player.get_window().get_xid()))
                                
    def on_mpv_player_draw(self, widget, cr):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.paint()
        
    def async_function(func):
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.daemon = True
            thread.start()
            return thread
        return wrapper
        
    @async_function
    def play_async(self, channelname, channelurl):
        ext = [".mkv", ".mp4", ".mpg", ".mpeg", ".flv", ".wmv"]
        url_ext = f'.{channelurl.rpartition(".")[2]}'
        print (f"Sender: {channelname}\nurl: {channelurl}")
        if channelname != None and channelurl != None:
            if url_ext in ext:
                self.reinit_mpv_movies()
            else:
                self.reinit_mpv()
            self.mpv.play(channelurl)
            self.mpv.wait_until_playing()
            self.is_playing = True
            self.mpv.show_text(channelname, duration="3000", level=None)
            self.channelbox.grab_focus()
            
    def makeList(self, mlist):
        for child in self.channelbox.get_children():
            self.channelbox.remove(child)
        text = open(mlist, 'r').read()
        self.urlList = []
        self.nameList = []      
        for lines in text.splitlines():
            line = lines.split(",")
            name, url = line[0], line[1]
            self.nameList.append(name)
            self.urlList.append(url)
  
        i = 0
        for ch in self.nameList:
            btn = Gtk.Button(label = ch)
            btn.set_relief(2)
            child = Gtk.FlowBoxChild()
            child.set_name(ch)
            child.add(btn)
            btn.connect("clicked", self.btn_clicked, i)
            self.channelbox.add(child)
            i += 1
        self.channelbox.show_all()
        
    def find_channel(self, *args):
        text = self.searchbar.get_text()
        if len(text) > 0:
            self.flowbox_filter(text)
        else:
            self.flowbox_filter("")
            self.channelbox.grab_focus()            
        
    def flowbox_filter(self, search_entry):
        def filter_func(fb_child, text):
            if text in fb_child.get_name() or text.lower() in fb_child.get_name() \
            or text.upper() in fb_child.get_name() or text.title() in fb_child.get_name():
                return True
            else:
                return False
                
        text = self.searchbar.get_text()        
        self.channelbox.set_filter_func(filter_func, text)

            
        
    def main(self, argv):
        home_folder = fpath.expanduser('~/.mxtv')
        print(home_folder)       
        self.file_list = []
        for x in range(10):
            self.file_list.append(f"{home_folder}/mychannels{x + 1}.txt")
            print(f"{home_folder}/mychannels{x + 1}.txt")
        
        self.urlList = []
        self.nameList = []
        self.volume = 90
        self.is_playing = False
        self.mpv = None
        self.fullscreen = False
        self.id = 0
        builder = Gtk.Builder()
        builder.add_from_file("mxtvs_gui.glade")

        screen = Gdk.Screen.get_default()        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('mystyle_s.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider,
          Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.mpv_player = builder.get_object("mpv_player")
        self.win = builder.get_object("window")
        #self.win.set_events (Gdk.EventMask.ALL_EVENTS_MASK)
        self.win.connect('key_press_event', self.on_key_press_event)
        self.sidebar = builder.get_object("sidebar")
        self.channelbox = builder.get_object("channels_flowbox")
        self.channelbox.set_can_focus(True)
        self.searchbar = builder.get_object("searchbar")
        self.searchbar.set_placeholder_text("find ...")
        self.searchbar.connect('search_changed', self.find_channel)
        self.vbox = builder.get_object("vbox")
        self.btn_decoration = builder.get_object("btn_decoration")
        self.btn_decoration.connect("clicked", self.on_decoration)
        self.btn_fullscreen = builder.get_object("btn_fullscreen")
        self.btn_fullscreen.connect("clicked", self.toggle_fullscreen)
        self.win.connect("destroy", Gtk.main_quit)
        self.win.connect('scroll-event', self.my_zoom)
        
        self.mpv_player.connect("realize", self.on_mpv_player_realize)
        self.mpv_player.connect("draw", self.on_mpv_player_draw)
        
        self.win.set_title("MX TV")
        if len(self.file_list) > 0:
            if fpath.isfile(self.file_list[0]):
                self.makeList(self.file_list[0])
                
        self.win.set_keep_above(True)
        self.win.set_decorated(True)
        self.win.resize(640, 300)
        self.win.move(50, 50)
        self.win.show_all()
        self.channelbox.grab_focus()
        Gtk.main() 


if __name__ == "__main__":
    w = MyWindow()
    w.main(sys.argv)
                            
