This script uses the `binwalk` API to generate a wxHexEditor TAGS file for any given binary/firmware dump.

Basic usage is `binnotate.py -f [filename]`

You can also specify `-Y` to run the capstone module (if you've got capstone installed properly), or `-A` to run the "opcodes" module. The capstone module can be really hit and miss - sometimes it's useful and works, sometimes not. Mainly it just hangs a lot.

If you want, you can specify a new output file with `-o [output filename]`. By default, the output filename is the name of the original file + .tags (which is the wxHexEditor default, and will get opened by default if the two files are in the same directory).

You'll need `binwalk` installed, ideally the latest - not whatever comes with your linux distro. 

Absolutely zero support/help available from me at this moment I'm afraid - this is my own script for my own use mainly, but it might help you too.