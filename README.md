This script uses the `binwalk` API to generate a wxHexEditor TAGS file for any given binary/firmware dump.

Basic usage is `binnotate.py -f [filename]`

By default, the .tags file will have the name of the original file plus a .tags extension, and will be saved to the same folder as the original. wxHexEditor should automatically open the .tags file when you load the binary file up. If it doesn't, use the `File->Import TAGs` option.

You can also specify `-Y` to run the capstone module (if you've got capstone installed properly), or `-A` to run the "opcodes" module. The capstone module can be really hit and miss - sometimes it's useful and works, sometimes not. Mainly it just hangs a lot.

If you want, you can specify a new output file with `-o [output filename]`. By default, the output filename is the name of the original file + .tags.

You'll need `binwalk` installed, ideally the latest - not whatever comes with your linux distro. 

Absolutely zero support/help available from me at this moment I'm afraid - this is my own script for my own use mainly, but it might help you too.