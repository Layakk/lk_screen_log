#!/usr/bin/python
########################
## lk_screen_log.py - Some functions to write message to a console
##
## Copyright (C) 2015 LAYAKK - www.layakk.com
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################
import textwrap
import os
import sys

# Source: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])

# GLOBALS
_INDENT_SIZE = 4
(_termwidth, _termheight) = getTerminalSize()
_widthremains = _termwidth
_currentIndentLevel = 0
_indent_str=''

def lkSMsgSetIndentSize(size=1):
	global _INDENT_SIZE
	_INDENT_SIZE = size

def lkSMsgSetIndentLevel(level):
	global _currentIndentLevel, _indent_str
	_currentIndentLevel = max(0,min(_termwidth-_INDENT_SIZE,level))
	_indent_str = ' '*(_INDENT_SIZE*_currentIndentLevel)
	
def lkSMsgMoreIndent(more=1):
	global _currentIndentLevel
	lkSMsgSetIndentLevel(_currentIndentLevel+more)

def lkSMsgLessIndent(less=1):
	global _currentIndentLevel
	lkSMsgSetIndentLevel(_currentIndentLevel-less)

def lkSMsgDontContinue():
	global _widthremains, _termwidth
	_widthremains = _termwidth

def lkScreenMsg(message="", ToBeContinued=False, ToBeRewritten=False, IndentLevel=-1):
	global _widthremains, _terminwidth
	global _indent_str

	if IndentLevel != -1:
		lkSMsgSetIndentLevel(IndentLevel)

	if len(message) == 0:
		sys.stdout.write("\n")
		sys.stdout.flush()
		return

	if ToBeRewritten:
		if _widthremains <> _termwidth:
			sys.stdout.write('\n')
			_widthremains = _termwidth
		_lines = _indent_str + message + ' '*(_termwidth-len(message)-len(_indent_str)-1) + '\r'
		sys.stdout.write(_lines[:_termwidth])
		sys.stdout.flush()
		return
	else:
		if _widthremains <> _termwidth:
			_initial_indent_str = ' '*(_termwidth-_widthremains)
		else:
			_initial_indent_str = _indent_str
		_lines=textwrap.wrap(message, _termwidth, initial_indent=_initial_indent_str, subsequent_indent=_indent_str, drop_whitespace=True, break_long_words=False, replace_whitespace=False)
		if _widthremains <> _termwidth:
			sys.stdout.write(_lines[0][-(len(_lines[0])-len(_initial_indent_str)):])
		else:
			sys.stdout.write(_lines[0])
		for i in range(1,len(_lines)):
			sys.stdout.write("\n"+_lines[i])

	if ToBeContinued:
		_widthremains = _termwidth-len(_lines[-1])
	else:
		sys.stdout.write('\n')
		_widthremains = _termwidth
		
	sys.stdout.flush()
