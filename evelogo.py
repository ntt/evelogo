#-----------------------------------------------------------------------------
# evelogo - EVE Online Logo Generator
#
# Copyright (c)2008 Jamie "Entity" van den Berge <entity@vapor.com>
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE
#
#-----------------------------------------------------------------------------
# Version: 1.1.0 (23 May 2010)
# - Now uses (and requires) the large size logos added in Tyrannis.
#
# Version: 1.0.1 (08 December 2008)
# - Fixed logos breaking that have only 1 or 2 shapes defined (Arkady)
#
# Version: 1.0 (08 December 2008)
# - Initial release
#
# Requirements:
#   Python 2.4+
#   Python Image Library
#   Prerendered Tyrannis Corp Logos
#

import os
from PIL import Image

resourcePath = "corplogos"

_folder = {
	64: "small",
	128: "medium",
	256: "large",
}

def CorporationLogo(data, size=64, transparent=True, bgcolor=None):
	"""Generates corp logo defined by the parameters in data object. The data
object may be an eveapi logo element from the CorporationSheet, a dict
containing the shapes and colors, or a sequence containing a shapes- and colors
sequence. Optionally, size other than the default 64px may be specified, and
transparency can be turned off, in which case it will render the logo on
a background with the color of your choice if specified, otherwise black."""

	if (getattr(data, "_name", None) == "logo") and hasattr(data, "_isrow"):
		# eveapi corpsheet logo data
		shape1, shape2, shape3 = data.shape1, data.shape2, data.shape3
		color1, color2, color3 = data.color1, data.color2, data.color3
	elif type(data) is dict:
		# dict with shape/color definitions
		shape1, shape2, shape3 = data["shape1"], data["shape2"], data["shape3"]
		color1, color2, color3 = data["color1"], data["color2"], data["color3"]
	elif type(data) in (list, tuple):
		# sequence with shape/color sequences
		shape1, shape2, shape3 = data[0]
		color1, color2, color3 = data[1]
	else:
		raise ValueError("Invalid logo data.")

	if size <= 64:
		baseSize = 64
	elif size <= 128:
		baseSize = 128
	else:
		baseSize = 256

	if transparent:
		logo = Image.new("RGBA", (baseSize,baseSize))
	else:
		logo = Image.new("RGB", (baseSize,baseSize))
		if bgcolor is not None:
			logo.paste(bgcolor, (0,0,baseSize,baseSize))

	path = os.path.join(resourcePath, _folder[baseSize])

	if shape3:
		layer3 = Image.open(os.path.join(path, str(color3), str(shape3) + ".png"))
		logo.paste(layer3, (0,0), layer3)
		p3 = layer3.load()
	if shape2:
		layer2 = Image.open(os.path.join(path, str(color2), str(shape2) + ".png"))
		logo.paste(layer2, (0,0), layer2)
		p2 = layer2.load()
	if shape1:
		layer1 = Image.open(os.path.join(path, str(color1), str(shape1) + ".png"))
		logo.paste(layer1, (0,0), layer1)
		p1 = layer1.load()

	if transparent:
		pix = logo.load()
		for x in xrange(baseSize):
			for y in xrange(baseSize):
				r,g,b,a = pix[x,y]
				a1 = ((255 - p1[x,y][3]) / 255.0) if shape1 else 1.0
				a2 = ((255 - p2[x,y][3]) / 255.0) if shape2 else 1.0
				a3 = ((255 - p3[x,y][3]) / 255.0) if shape3 else 1.0
				a = (1.0-(a1*a2*a3))
				if a:
					pix[x,y] = (int(r/a),int(g/a),int(b/a),int(255*a))

	if size != baseSize:
		return logo.resize((size,size), Image.ANTIALIAS)

	return logo

