# COMMENT

This principle also works if you skip the main tkinter.Frame a.k.a. "class Window"[¹](https://github.com/Skrimpton/tk.Text-DisableDragSelect/blob/main/README.md#---or-window-among-friends)
<br>and e.g. add both text and EVENTSINK as children of root.

Using grab_set we can unfocus the text-widget and pass all events to the grabbed object
<br>Any widget or window can be used: https://dafarry.github.io/tkinterbook/widget.htm#tkinter.widget.grab_set-method
<br>I chose frame because it can be completely visually hidden, also I imagine it's "low cost".

## SAFE HANDLING OF CRASHES MIGHT BE AN IMPORTANT TODO, CURRENTLY BEYOND THE SCOPE OF MY COMPETENCY

A caveat of ```grab_set``` is that the object being grabbed has to be registered as visible, simply existing is not enough for tkinter
<br>so it needs to be placed, packed or begriddled[²](https://github.com/Skrimpton/tkinter.Text-DisableDragSelect/blob/main/README.md#---geometry-managed-using-the-grid-method)

```grab_set``` effects window manager behaviour in that mouse and keyboard events are handled and redirecred, potentially on a "global" scale.

It cannot be released after Tk() destruction[³](https://github.com/Skrimpton/tk.Text-DisableDragSelect/blob/main/README.md#---obviously-why-did-i-even-try)

So for some delusion of safety I bind both ```protocol("WM_DELETE_WINDOW")```
<br>and ```::SIGINT::``` to at least make sure ```grab_release``` is called/requested on user-interraction before exiting

I did experience once, on Linux - during testing, that left-clicks were not going through on anything in the KDE 5.27 panel or default application launcher (start-menu) [⁴](https://github.com/Skrimpton/tk.Text-DisableDragSelect/blob/main/README.md#---kickoff)

In Kate[⁵](https://github.com/Skrimpton/tk.Text-DisableDragSelect/main/README.md#---kde-text-editoride) clicks where partially going through[⁶](https://github.com/Skrimpton/tk.Text-DisableDragSelect/blob/main/README.md#---not-on-all-gui-elements-but-did-move-text-cursor-position-if-i-recall-correctly), but scrolling was not happening.

A frustrated and impulsive restart fixed the problem, and I imagine logging out and back in would have aswell.
<br>There might have been something wrong with code at that time, changes have been made and forgotten.

I was also using a mouse connected to a Windows 10 client, so it could have been something that happened in Barrier[⁷](https://github.com/Skrimpton/tk.Text-DisableDragSelect/main/README.md#---httpsgithubcomdebaucheebarrier).

Or it could have been one of many bugs that have happened after unfortunate circumstances
forced me to switch from the rock-solid Logitech G604 to an energy-drink themed abomination from Razer[⁸](https://github.com/Skrimpton/tk.Text-DisableDragSelect/blob/main/README.md#---in-all-fairness-its-mainly-the-horrible-software%E1%B5%83-the-mouse-is-decent-hardware)

Point being: *something* happend which affected xorg, and did so in a way that ```grab_set``` explicitly does.
<br>It did not occur before or after that one time.

## Annotations
##### ¹)   ...or Window(), among friends

##### ²)   geometry managed using the ```.grid``` method

##### ³)   Obviously... why did I even try?

##### ⁴)   Kickoff

##### ⁵)   KDE text-editor/IDE

##### ⁶)   Not on all gui-elements, but did move text-cursor position, if I recall correctly

##### ⁷)   https://github.com/debauchee/barrier

##### ⁸)   In all fairness: it's mainly the horrible software[ᵃ](https://github.com/Skrimpton/tk.Text-DisableDragSelect/blob/main/README.md#%E1%B5%83---macro-functionality-as-an-optional-downloadable-plugin-prone-to-crashing--the-mouse-has-12-side-buttons-all-prebound-to-numbers-and-2-extra-top-buttons-bound-to-nothing--and-do-not-get-me-started-on-the-fact-that-they-want-me-to-create-and-log-into-an-account--to-unlock-all-features-of-my-mouse-driver-software), the mouse is decent hardware

##### ᵃ)   Macro-functionality as an optional downloadable plugin (prone to crashing)?<br>  The mouse has 12 side-buttons all prebound to numbers and "+" "-" "=", in addition there are 2 extra top buttons bound to nothing...<br>  And do not get me started on the fact that they want me to create and log into an account to "unlock all features" of my mouse-driver-software! <br><br> Anyways, here is the code:


# CODE
```python
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

```
