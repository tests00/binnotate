#!/usr/bin/python3

# binnotate v0.01

import binwalk
import string
import argparse, os
from xml.sax.saxutils import escape

parser = argparse.ArgumentParser(description="Generate a wxHexEditor tags file using binwalk. Does a basic signature scan for now.")
parser.add_argument("-f", "--file", dest="infile", help="file", required=True)
parser.add_argument("-o", "--output", dest="outfile", help="output file")

parser.add_argument("-Y", "--disasm", dest="do_disasm", help="scan with disasm", action="store_true")
parser.add_argument("-A", "--opcodes", dest="do_opcodes", help="scan for opcodes", action="store_true")

args = parser.parse_args()

if args.infile is not None:
	file = args.infile
	try:
		os.path.exists(file)
	except:
		print("File doesn't exist")
		os._exit(1)
else:
	print("Need a filename!")
	os._exit(1)
	
if args.outfile is not None:
	outfile = args.outfile
else:
	outfile = file + ".tags"
	
if os.path.exists(outfile):
	print("outfile already exists!")
	os._exit(1)


tags_outer_template = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
<wxHexEditor_XML_TAG>
\t<filename path="${file_absolute_path}">
${tag_elements}
\t</filename>
</wxHexEditor_XML_TAG>
""")

single_tag_template = string.Template("""\t\t<TAG id="${tag_id}">
\t\t\t<start_offset>${tag_start_offset}</start_offset>
\t\t\t<end_offset>${tag_end_offset}</end_offset>
\t\t\t<tag_text>${tag_text}</tag_text>
\t\t\t<font_colour>${tag_font_colour}</font_colour>
\t\t\t<note_colour>${tag_note_colour}</note_colour>
\t\t</TAG>
""")

'''
# Generic .tags file looks like this:
<?xml version="1.0" encoding="UTF-8"?>
<wxHexEditor_XML_TAG>
  <filename path="C:\Applications\testtag.tags">
    <TAG id="0">
      <start_offset>2142</start_offset>
      <end_offset>2144</end_offset>
      <tag_text></tag_text>
      <font_colour>#000000</font_colour>
      <note_colour>#A17D00</note_colour>
    </TAG>
  </filename>
</wxHexEditor_XML_TAG>
'''

# Empty string for the tags, zero for the id
all_tags = ""
this_id = 0

font_colour = "#000000"

note_colour = [	"#FCA0FF", # pastel pink
				"#76C4FF", # pastel darker blue
				"#76FF9F", # pastel turquoise
				"#daff76", # pastel green
				"#ffff76", # pastel yellow
				"#ffcc76", # pastel orange
				"#76FFFA", # pastel blue
				"#EBA0FF", # pastel purple
				"#ff7f76" ] # pastel red
				
colours_len = len(note_colour)


# requires capstone, will probably hang or fail if it's not installed properly
if args.do_disasm:
	print("Using --disasm against the file")
	for disasms in binwalk.scan('--disasm', file):
		for result in disasms.results:
			if result.valid:
				if result.size == 0:
					end_offset = result.offset + 4
					size_note = "(binwalk api didn't return a size, defaulted to 4)"
				else:
					end_offset = result.offset + result.size	
					size_note = "(binwalk api returned a size of " + str(result.size) + ")"
				all_tags += single_tag_template.substitute(	tag_id=this_id, 
															tag_start_offset=result.offset, 
															tag_end_offset=end_offset, 
															tag_text=escape(hex(result.offset) + ": " + result.description + " " + size_note), 
															tag_font_colour=font_colour, 
															tag_note_colour=note_colour[this_id%colours_len] )
				this_id += 1
			
			

if args.do_opcodes:
	print("Using --opcodes against the file...")

	for opcodes in binwalk.scan('--opcodes', file):
		for result in opcodes.results:
			if result.valid:
				if result.size == 0:
					end_offset = result.offset + 4
					size_note = "(binwalk api didn't return a size, defaulted to 4)"
				else:
					end_offset = result.offset + result.size
					size_note = "(binwalk api returned a size of " + str(result.size) + ")"
				all_tags += single_tag_template.substitute(	tag_id=this_id, 
															tag_start_offset=result.offset, 
															tag_end_offset=end_offset, 
															tag_text=escape(hex(result.offset) + ": " + result.description + " " + size_note), 
															tag_font_colour=font_colour, 
															tag_note_colour=note_colour[this_id%colours_len] )
				this_id += 1



for signature in binwalk.scan('--signature', file):
	for result in signature.results:
		if result.valid:
			if result.size == 0:
				end_offset = result.offset + 4
				size_note = "(binwalk api didn't return a size, defaulted to 4)"
			else:
				end_offset = result.offset + result.size
				size_note = "(binwalk api returned a size of " + str(result.size) + ")"
			all_tags += single_tag_template.substitute(	tag_id=this_id, 
														tag_start_offset=result.offset, 
														tag_end_offset=end_offset, 
														tag_text=escape(hex(result.offset) + ": " + result.description + " " + size_note), 
														tag_font_colour=font_colour, 
														tag_note_colour=note_colour[this_id%colours_len] )
			this_id += 1

final_tags_file = tags_outer_template.substitute(file_absolute_path=file, tag_elements=all_tags)

print("Writing .tags file...")
write_file = open(outfile, "w")
write_file.writelines(final_tags_file)
write_file.close()