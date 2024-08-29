#!/bin/env python
import tkinter as tk
import signal

class Window(tk.Frame):
    def __init__(self
                 ,root=None
                 ,allowDragSelect=True
                 ,gain=1
                 ,*args,**kw
    ):
        signal.signal(signal.SIGINT, lambda x,y : print('terminal ^C') or self.close())
        super().__init__(root,*args,**kw)

        self.root                     = root
        self.grabbed                  = False
        self.pause_grab               = None

        self.allowDragSelect          = tk.BooleanVar()
        self.allowDragSelect          .set(allowDragSelect)
        self.allowDragSelect          .trace_add('write', self.handleAllowDragSelectChanged)

        self.build()
        self.bindem()



    def build(self):
        self.check                    = tk.Checkbutton(self,text="DISABLE CLICK-DRAG-SELECTING",variable=self.allowDragSelect)
        '''
            THIS IS THE EVENTSINK OBJECT.

        '''
        self.EVENTSINK                = tk.Frame( self
                                                   ,bd                  = 0
                                                   ,highlightthickness  = 0
                                                   ,relief              = 'flat'
                                                   ,cursor = 'xterm'
                                      )

        self.TEXT                     = tk.Text(self,)

        ntxt = ""
        for x in range(10):
            x+=1
            ntxt += f"{x}\n"

        self.TEXT.insert(1.0,ntxt.strip())

        self                          .pack(fill='both',expand=True)
        self.EVENTSINK                .place(x=0,y=0,width=0,height=0)
        self.check                    .pack(fill='x',expand=0)
        self.TEXT                     .pack(fill='both',expand=1)


    def bindem(self):

        self.root                     .protocol("WM_DELETE_WINDOW", self.close)
        self.root                     .bind('<Control-g>',self.toggleDragSelect)
        self.TEXT                     .bindtags((str(self.TEXT), "Text", "PostEvent", ".", "all")) # https://stackoverflow.com/a/50637979

        self.EVENTSINK                .bind('<ButtonRelease-1>',self.ungrab)

        if self.allowDragSelect.get():
            self.TEXT                 .bind_class("PostEvent", "<ButtonPress-1>", self.onClicked)
        else:
            self.TEXT                 .bind("<ButtonPress-1>", lambda e:self.onClicked(e,"selectguard"))

    def onEVENTSINK_DISABLE_DRAG_SELECT(self,e):
        return 'break'

    def handleAllowDragSelectChanged(self,*e):
        if self.allowDragSelect.get():
            self.TEXT                 .bind_class("PostEvent", "<ButtonPress-1>", self.onClicked)
        else:
            self.TEXT                 .bind_class("PostEvent", "<ButtonPress-1>",lambda e:self.onClicked(e,"selectguard"))

    def toggleDragSelect(self,*e):
        self.allowDragSelect          .set(not self.allowDragSelect.get())

    def onClicked(self,e,selectguard=None):
        if selectguard is not None:
            return 'break'
        else:
            if not self.grabbed:
                self                  .grab_sink()

    def grab_sink(self,*se):

        if not self.grabbed:
            self.grabbed              = True
            self.EVENTSINK            .grab_set()
            if self.allowDragSelect.get():
                self.EVENTSINK        .bind('<Motion>',self.onEVENTSINK_DISABLE_DRAG_SELECT)

        return 'break'

    def ungrab(self,*e):
        self.EVENTSINK                .grab_release()
        self.EVENTSINK                .unbind('<Motion>')
        self.grabbed                  = False

    def close(self):
        self.EVENTSINK                .grab_release()
        self.root                     .destroy()



if __name__ == "__main__":
    root     = tk.Tk()
    app      = Window(root)
    root     .mainloop()
