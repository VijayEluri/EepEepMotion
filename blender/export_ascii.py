#!BPY

""" Registration info for Blender menus: <- these words are ignored
Name: 'Ascii (.txt)...'
Blender: 241
Group: 'Export'
Tip: 'Export as ascii text'
"""

__author__ = "Daniel Salazar (ZanQdo)"
__url__ = ("blender", "blenderartists.org",
"e-mail: zanqdo@gmail.com")
__version__ = "16/04/08"

__bpydoc__ = """\
This script exports the selected object's motion channels to Lightwave
motion files (.mot).

Usage:
Run the script with one or more objects selected (any kind), frames exported
are between Start and End frames in Render buttons.

"""

# $Id: export_lightwave_motion.py 14530 2008-04-23 14:04:05Z campbellbarton $
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2003, 2004: A Vanpoucke
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------
import Blender as B
import math as M
#------------------------------------
#Declarados:
TotalCanales = 9
#------------------------------------

def FuncionPrincipal (Dir):
	B.Window.WaitCursor(1)
	ObjSelect = B.Object.GetSelected()
	
	if not ObjSelect:
		B.Draw.PupMenu('Select 1 or more objects, aborting.')
		return
	
	if not Dir.lower().endswith('.txt'):
		Dir += '.txt'
		
	
	SC = B.Scene.GetCurrent()
	SCR = SC.getRenderingContext()
	TL = SC.getTimeLine()
	
	for ob in ObjSelect:
		origName= NombreObjeto= ob.name
		print '----\nExporting Object "%s" motion file...' % origName

		FrameA = B.Get('curframe')
		FrameP = B.Get('staframe')
		FrameF = B.Get('endframe')

		FrameRate = float(SCR.framesPerSec())

		#---------------------------------------------

		# Replace danger characters by '_'
		for ch in ' /\\~!@#$%^&*()+=[];\':",./<>?\t\r\n':
			NombreObjeto = NombreObjeto.replace(ch, '_')

		# Check for file path extension
		if len(ObjSelect) > 1:
			DirN= '%s_%s.txt' % (Dir[:-4], NombreObjeto)
		else:
			DirN= Dir
		
		# Open the file
		File = open(DirN,'w')
#		File.write ('LWMO\n3\n\n') # 3 is the version number.

		# number of channels
#		File.write ('NumChannels %i\n' % TotalCanales)

		# ----------------------------
		# Main Cycle

		def CicloPrimario(NumCanal):
			B.Set('curframe', FrameP)

#			File.write ('Channel %i\n{ Envelope\n  %i\n' % (NumCanal, (FrameF - FrameP + 1)))

			FrameA = FrameP
			while FrameA < (FrameF + 1):

				B.Set('curframe', FrameA)
				
				mat= ob.mat # Worldspace matrix
				
				loc_x = mat.translationPart().x
				loc_y = -1 * mat.translationPart().y
				loc_z = mat.translationPart().z
				rx = M.radians (-mat.toEuler().x)
				ry = -1 * M.radians (-mat.toEuler().y)
				rz = M.radians (-mat.toEuler().z)
				x3 = mat.scalePart().x
				z3 = mat.scalePart().z
				y3 = mat.scalePart().y
#				File.write ('  Key %f %f 3 0 0 0 0 0 0\n' % (Val, (FrameA/FrameRate)))
#				File.write ('frame %d %s:%f\n' % (FrameA, txt, Val))
#				File.write ('frame:%d loc:(%f,%f,%f) rot:(%f, %f, %f) scale:(%f, :%f, %f)\n' 
				File.write ('%d %f %f %f %f %f %f %f %f %f\n' 
					% (FrameA, loc_x, loc_y, loc_z, rx, ry, rz, x3, y3, z3))
#					% (FrameA, TL.getMarked(FrameA), loc_x, loc_y, loc_z, rx, ry, rz, x3, y3, z3))

				FrameA += 1
			# Ending Stuff
#			File.write ('  Behaviors 1 1\n}\n')

		NumObjetoActual = len(ObjSelect)
		Iteraciones = 0
		ProgBarVal = 0.0
#		while Iteraciones < TotalCanales:
		CicloPrimario(Iteraciones)

			# Start Progress Bar
#			B.Window.DrawProgressBar(ProgBarVal, origName)
#			ProgBarVal = (float(Iteraciones) / TotalCanales) * 0.98
#			Iteraciones += 1
			
		B.Window.DrawProgressBar(1.0, '') # Done
		print '\nDone, %s motion file location is:\n%s\n' % (origName, DirN)
	B.Window.WaitCursor(0)

# Check if there are selected objects
def main():
#	B.Window.FileSelector(FuncionPrincipal, "Write .txt File", B.sys.makename(ext='.txt'))
	B.Window.FileSelector(FuncionPrincipal, "Write .txt File", B.Scene.GetCurrent().getName() + '.txt')

if __name__=='__main__':
	main()
