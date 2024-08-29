#!/bin/env python
import tkinter as tk
# from tkinter import ttk
import signal

'''
    # tkinter.text with optional click-blocking, click-drag selecting and/or click-drag-scrolling - using <grab_set>

    # --------------------------------------------------------------------------------------------------------------
    # COMMENT:
    # --------------------------------------------------------------------------------------------------------------

    The principle also works if you skip the parented tkinter.frame a.k.a. "class Window"¹.
    and e.g. add both text and EVENTSINK as children of root.

    ( I tested this on accident, when I forgot to reparent TEXT to Window(), and also forgot <.pack> Window() )

    Using <grab_set> we can unfocus the text-widget and pass all events to the grabbed object

    Any widget or window can be used: https://dafarry.github.io/tkinterbook/widget.htm#tkinter.widget.grab_set-method
    I chose frame because it can be completely visually hidden, also I imagine it is "low cost".

    A caveat of <grab_set> is that the object being grabbed has to be registered as visible, simply existing is not enough
    so it needs to be placed, packed or begriddled²

    <grab_set> effects window manager behaviour in that mouse and keyboard events are handled and modified, potentially on a "global"-scale.
    It cannot be unset after tk() destruction³

    So for some delusion of safety I bind both window <protocol("WM_DELETE_WINDOW")>
    and  ::SIGINT:: to at least make sure <grab_release> is called/requested (on user-interraction) before exiting


    ### SAFE HANDLING OF CRASHES MIGHT BE AN #IMPORTANT TODO, CURRENTLY BEYOND THE SCOPE OF MY COMPETENCY:


    I did experience once, on Linux - during testing
    that left-clicks were not going through on anything in the KDE 5.27 panel or default-startmenu⁴

    In Kate⁵ clicks where partially going through⁶, but scrolling was not happening.

    A frustrated and impulsive restart fixed the problem, and I imagine logging out and back in would have aswell.

    There might have been something wrong with code at that time, changes have been made and forgotten.

    I was also using a mouse connected to a Windows 10 client, so it could have been something that happened in Barrier⁷.
    Or it could have been one of many bugs that have happened after unfortunate circumstances
    forced me to switch from the rock-solid Logitech G604 to an energy-drink themed abomination from Razer⁸

    But *something* happend which affected xorg, and did so in a way that <grab_set> explicitly does.
    It did not occur before or after that one time.

    # --------------------------------------------------------------------------------------------------------------
    # COMMENT-ANNOTATIONS
    # --------------------------------------------------------------------------------------------------------------

    ¹)   ...or Window(), among friends
    ²)   widget.grid
    ³)   Obviously... why did I even try?
    ⁴)   Kickoff
    ⁵)   KDE text-editor/IDE
    ⁶)   Not on all gui-elements, but did move text-cursor position, if I recall correctly
    ⁷)   https://github.com/debauchee/barrier

    ⁸)   In all fairness: it's mainly the horrible softwareᵃ, the mouse is decent hardware

    ᵃ)   Macro-functionality as an optional downloadable plugin (prone to crashing)?
         The mouse has 12 side-buttons all prebound to numbers and 2 extra top buttons bound to nothing...

         And do not get me started on the fact that they want me to create and log into an account
         to "unlock all features" of my mouse-driver-software...!

    # --------------------------------------------------------------------------------------------------------------

    Anyways, here is the code:

'''

class Window(tk.Frame):
    def __init__(self
                 ,root=None
                 ,allowClicks=True
                 ,clickDragScroll=True
                 ,gain=1
                 ,*args,**kw
    ):
        signal.signal(signal.SIGINT, lambda x,y : print('terminal ^C') or self.close())
        super().__init__(root,*args,**kw)

        self.root               = root

        self.grabbed            = False
        self.pause_grab         = None

        self.allowClicks        = tk.BooleanVar()
        self.allowClicks        .set(allowClicks)
        self.allowClicks        .trace_add('write', self.handleAllowClicksChanged)

        self.clickDragScroll    = tk.BooleanVar()
        self.clickDragScroll    .set(clickDragScroll)


        self.varScale           = tk.IntVar()
        self.varScale           .set(gain)
        self.varScale           .trace_add("write",self.onSliderChanged)
        self.gain               = gain
        self.build()
        self.bindem()



    def build(self):
        # root = self.root
        self.pack(fill='both',expand=True)

        '''
            THIS IS THE EVENTSINK OBJECT.

        '''
        self.EVENTSINK = tk.Frame( self
                                   ,bd                  = 0
                                   ,highlightthickness  = 0
                                   ,relief              = 'flat'
                                  )
        self.EVENTSINK.place(x=0,y=0,width=0,height=0)

        # BEGIN ------------------------------------------------------  Useless information occupies every open space inside your skull

        self.frameSlider = tk.Frame(self,height=18)
        self.frameSlider.pack_propagate(False)

        self.buttonallowClicks = tk.Checkbutton(self.frameSlider
                                              ,font=("",8)
                                              ,variable=self.allowClicks
                                              ,text="Allow text clicks")
        self.buttonclickDragScroll = tk.Checkbutton(self.frameSlider
                                               ,font=("",8)
                                               ,variable=self.clickDragScroll
                                               ,text="Drag-scrolling"
                                              )

        self.labelSlider = tk.Label(self.frameSlider
                                    ,font=("",8)
                                    ,text="Drag-scroll distance/speed (gain):"
                                    )

        self.buttonSliderPlus = tk.Button( self.frameSlider
                                          ,font=("",8)
                                          ,text="+"
                                          ,command=self.onSliderPlus
                                          )
        self.buttonSliderMinus = tk.Button( self.frameSlider
                                           ,font=("",8)
                                           ,text="-"
                                           ,command=self.onSliderMinus
                                           )

        self.labelSliderCurrent = tk.Label( self.frameSlider
                                           ,font=("",8)
                                           ,textvariable=self.varScale
                                           ,width=4
                                           )
        self.clickDragScrollSpeed = tk.Scale(self.frameSlider
                                        ,from_          =0
                                        ,tickinterval   =1
                                        ,to             =1000
                                        ,showvalue      =False
                                        ,sliderrelief   ='flat'
                                        ,orient         ="horizontal"
                                        ,variable       =self.varScale
                                        )


        self.TEXT = tk.Text(self,)

        for x in range(60000):
            x+=1
            self.TEXT.insert(float(f"{x}.0"),f"{x}\n")

        # self.TEXT.bind("button", "<Button>", self.grab)

        self.buttonallowClicks      .pack(side='left'
                                          ,fill='both',expand=0)
        self.buttonclickDragScroll  .pack(side='left'
                                          ,fill='both',expand=0)
        self.labelSlider            .pack(side='left'
                                          ,fill='both',expand=0)
        self.clickDragScrollSpeed        .pack(side='left'
                                          ,fill='both',expand=1)
        self.labelSliderCurrent     .pack(side='left'
                                          ,fill='both',expand=0)
        self.buttonSliderMinus      .pack(side='left'
                                          ,fill='both',expand=0)
        self.buttonSliderPlus       .pack(side='left'
                                          ,fill='both',expand=0)

        self.frameSlider            .pack(fill='x',expand=0)
        self.TEXT                   .pack(fill='both',expand=1)

        # END ------------------------------------------------------    You [now] know what's going on every day, every night, everywhere.
        #                                                               Swear you're so international.

    def bindem(self):

        self.root       .protocol("WM_DELETE_WINDOW", self.close)
        self.root       .bind('<Control-g>',self.toggleEdit)

        self.TEXT       .bindtags((str(self.TEXT), "Text", "PostEvent", ".", "all")) # https://stackoverflow.com/a/50637979
        self.TEXT       .bind("<ButtonPress-2>",self.grab)

        # self.TEXT       .bind('<ButtonRelease-1>',self.ungrab)
        # self.TEXT       .bind('<ButtonRelease-2>',self.ungrab)

        self.EVENTSINK  .bind('<ButtonRelease-1>',self.ungrab)
        self.EVENTSINK  .bind("<ButtonRelease-2>",self.ungrab)

        if self.allowClicks.get():
            self.TEXT   .bind_class("PostEvent", "<ButtonPress-1>", self.onClicked)
        else:
            self.TEXT   .bind("<ButtonPress-1>", lambda e:self.onClicked(e,"clickguard"))

    def onEVENTSINK_DISABLE_DRAG_SELECT(self,e):
        return 'break'

    def onEVENTSINK_CLICK_DRAG_SCROLL(self,e):
        if self.grabbed == True:
            # self.TEXT.scan_dragto(e.x,e.y)
            self.TEXT.tk.call( self.TEXT._w ,'scan' ,'dragto'
                    ,e.x, e.y, self.gain
            );

    def handleAllowClicksChanged(self,*e):
        if self.allowClicks.get():
            # print("TOGGLING EDIT")
            self.TEXT.unbind('<ButtonPress-1>')
            self.TEXT.bind_class("PostEvent", "<ButtonPress-1>", self.onClicked)
        else:
            self.TEXT.bind_class("PostEvent", "<ButtonPress-1>",lambda e:self.onClicked(e,"clickguard"))
            self.TEXT.bind("<ButtonPress-1>", lambda e:self.onClicked(e,"clickguard"))

    def toggleEdit(self,*e):
        self.allowClicks.set(not self.allowClicks.get())

    def onSliderChanged(self,*e):
        self.gain = self.varScale.get()

    def onSliderMinus(self,*e):
        if self.gain > 0:
            self.varScale.set(self.gain-1)

    def onSliderPlus(self,*e):
        if self.gain < 1000:
            self.varScale.set(self.gain+1)


    def onClicked(self,e,clickguard=None):
        if clickguard == "clickguard" or clickguard is True:

            if not self.grabbed:
                self.grabbed = True
                self.EVENTSINK.grab_set()
                # if self.clickDragScroll.get():
                self.EVENTSINK.bind('<Motion>',self.onEVENTSINK_DISABLE_DRAG_SELECT)
            return 'break'

    def grab(self,e):

        if not self.grabbed:
            self.grabbed = True
            self.EVENTSINK.grab_set()
            if self.clickDragScroll.get():
                self.TEXT.scan_mark(e.x,e.y)
                self.EVENTSINK.bind('<Motion>',self.onEVENTSINK_CLICK_DRAG_SCROLL)

        return 'break'

    def ungrab(self,*e):
        self.EVENTSINK.grab_release()
        if self.clickDragScroll.get():
            self.EVENTSINK.unbind('<Motion>')
        self.grabbed = False

    def close(self):
        self.EVENTSINK.grab_release()
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
