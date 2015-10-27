# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************


class StringColor(object):
    
    
    F_COLOR = {"BLACK":30,
               "RED":31,
               "GREEN":32,
               "YELLOW":33,
               "BLUE":34,
               "AUBERGINE":35,
               "ULTRAMARINE":36,
               "WHITE":37}
    
    SHOWFMT = {"DEFAULT":0,
               "HIGLIG":1,
               "UNDERLINE":4,
               "GLINT":5,
               "NOSHOW":8}

    B_COLOR = {"BLACK":40,
               "RED":41,
               "GREEN":42,
               "YELLOW":43,
               "BLUE":44,
               "AUBERGINE":45,
               "ULTRAMARINE":46,
               "WHITE":47}
    
    F_BLK = 0
    F_RED = 2
    F_GRE = 4
    F_YEL = 6
    F_BLU = 8
    
    HIGLIG = 0
    UNDLIN = 1
    
    def __init__(self):
        self.start_fmt = "\033[%sm"
        self.end_fmt = "\033[0m"
    
    
    def selfprint(self, string):
        print string

    def printColorString(self, string, flags):
        if flags == 0:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["HIGLIG"],
                                     StringColor.F_COLOR["BLACK"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 2:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["HIGLIG"],
                                     StringColor.F_COLOR["RED"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 4:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["HIGLIG"],
                                     StringColor.F_COLOR["GREEN"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 6:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["HIGLIG"],
                                     StringColor.F_COLOR["YELLOW"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 8:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["HIGLIG"],
                                     StringColor.F_COLOR["BLUE"],
                                     StringColor.B_COLOR["WHITE"])

        if flags == 1:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["UNDERLINE"],
                                     StringColor.F_COLOR["BLACK"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 3:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["UNDERLINE"],
                                     StringColor.F_COLOR["RED"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 5:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["UNDERLINE"],
                                     StringColor.F_COLOR["GREEN"],
                                     StringColor.B_COLOR["WHITE"])
        elif flags == 7:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["UNDERLINE"],
                                     StringColor.F_COLOR["YELLOW"],
                                     StringColor.B_COLOR["BLACK"])
        elif flags == 9:
            color_fmt = "%d;%d;%d" %(StringColor.SHOWFMT["UNDERLINE"],
                                     StringColor.F_COLOR["BLUE"],
                                     StringColor.B_COLOR["WHITE"])
        return self.start_fmt %color_fmt + str(string) + self.end_fmt
        #self.selfprint(self.start_fmt %color_fmt + str(string) + self.end_fmt)

    

if __name__ == '__main__':
     StringColor().printColorString("testst", StringColor.F_BLU | StringColor.UNDLIN)