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
