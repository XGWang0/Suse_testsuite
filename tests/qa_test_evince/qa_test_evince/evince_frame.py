#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        07/22/2010
# Description: Open a PDF function for reused in other tests
##############################################################################
from pyatspi import Registry
from strongwind import *

def openFile(accessible, app):
  # Step1: From <File> menu select <Open> menu item to invoke Open Document dialog
  menubar = accessible.findMenuBar(None)
  menubar.select(['File', 'Open...'])
  sleep(config.SHORT_DELAY)

  # Step2: Click ToggleButton "Type a file name" to show the textbox of input URL 
  open_dialog = accessible.findNewItem("Dialog", "Open Document")
  sleep(config.SHORT_DELAY)
  if not open_dialog.findToggleButton("Type a file name").checked:
      open_dialog.clickItem("ToggleButton", "Type a file name")
  else:
      pass
  sleep(config.SHORT_DELAY)

  # Step3: Input pdf path and press Open button
  textdata={"0":"/usr/share/doc/packages/iproute2/rtstat.pdf"}
  open_dialog.inputItem( "Texts", textdata)
  sleep(config.SHORT_DELAY)
  open_dialog.clickItem("PushButton", "Open")
  sleep(config.SHORT_DELAY)
  open_dialog.assertClosed()

  # Step4: Assert frame with new name
  app.assertobject("Frame", "rtstat.dvi (rtstat.pdf)")
  sleep(config.SHORT_DELAY)

  # Step5: Click that ToggleButton again to clean the test env.
  menubar.select(['File', 'Open...'])
  sleep(config.SHORT_DELAY)
  open_dialog = accessible.findNewItem("Dialog", "Open Document")
  sleep(config.SHORT_DELAY)
  open_dialog.clickItem("ToggleButton", "Type a file name")
  sleep(config.SHORT_DELAY)

  # Step6: Click Cancel button of the dialog and close the whole frame
  open_dialog.clickItem("PushButton", "Cancel")
  sleep(config.SHORT_DELAY)
  open_dialog.assertClosed()

def press (x, y, button=1, log=True):
    """
    Synthesize a mouse button press at (x,y)
    """
    if log:
        procedurelogger.action("Mouse button %s press at (%s,%s)"%(button,x,y))
    Registry.generateMouseEvent(x,y, 'b%sp' % button)
    sleep(config.SHORT_DELAY)

def release (x, y, button=1, log=True):
    """
    Synthesize a mouse button release at (x,y)
    """
    if log:
        procedurelogger.action("Mouse button %s release at (%s,%s)"%(button,x,y))
    Registry.generateMouseEvent(x,y, 'b%sr' % button)
    sleep(config.SHORT_DELAY)

def absoluteMotion (x, y, log=True):
    """
    Synthesize mouse absolute motion to (x,y)
    """
    if log:
        procedurelogger.action("Mouse absolute motion to (%s,%s)"%(x,y))
    Registry.generateMouseEvent(x,y, 'abs')
    sleep(config.SHORT_DELAY)

def drag(fromObject=None, toObject=None, fromXY=0, toXY=0, button = 1, log=True):
    """
    Synthesize a mouse press, drag, and release on the screen.
    """
    if fromObject:
        bbox_l = fromObject.extents
        x_l = bbox_l.x + (bbox_l.width / 2)
        y_l = bbox_l.y + (bbox_l.height / 2)
        fromXY = (x_l, y_l - 10)
    (x,y) = fromXY
    press (x, y, button, log)

    if toObject:
        bbox_t = toObject.extents
        x_t = bbox_t.x + (bbox_t.width / 2)
        y_t = bbox_t.y + (bbox_t.height / 2)
        toXY = (x_t + 120, y_t)
 	
    (x,y) = toXY

    if log and fromObject and toObject:
        procedurelogger.action("Mouse button %s drag %s from %s to %s%s"% \
                    (button, fromObject.name, fromXY, toObject.roleName, toXY))
    else:
        procedurelogger.action("Mouse button %s drag %s from %s to %s%s"% \
                    (button, fromObject, fromXY, toObject, toXY))
    absoluteMotion(x, y, log)
    #sleep(config.SHORT_DELAY)
 	
    release (x, y, button, log)
    sleep(config.SHORT_DELAY)
