EVE Online Logo Generator.

This python module lets you generate corporation logos.


LICENSE:
This software is released under the MIT license. See evelogo.py for details.


REQUIREMENTS:
- Python 2.x
- Python Imaging Library 1.1.6 or better
- Tyrannis Pre-rendered Corporation Logo Symbols pack.


INSTALLATION:
Place the evelogo.py either in your site-packages folder or in your project
dir, whichever is appropriate for your project.

Download the corplogos pack:

   http://dl.eve-files.com/media/corp/Entity/corplogos.7z

Extract the corplogos archive and place the corplogos folder anywhere you want.
If you place it in your project's work folder, the module will work without
having to set the resourcePath in your code.


Example usage:
import eveapi
import evelogo

evelogo.resourcePath = "wherever/you/put/corplogos/"

YOUR_USERID = 123
YOUR_APIKEY = "bla bla bla"

# Generate logos directly from parameters:
logo = evelogo.CorporationLogo([[539, 520, 461], [672, 675, 672]])
logo.save("xfi1.png")

# Generate large opaque logo image with blue background:
logo = evelogo.CorporationLogo([[539, 520, 461], [672, 675, 672]], size=96, transparent=False, bgcolor=(33,133,233))
logo.save("xfi2.png")

# Or use the eveapi module!
api = eveapi.EVEAPIConnection()
corpsheet = api.corp.CorporationSheet(userID=YOUR_USERID, apiKey=YOUR_APIKEY, corporationID=219220371)
logo = evelogo.CorporationLogo(corpsheet.logo)
logo.save("xfi3.png")