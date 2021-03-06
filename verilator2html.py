#!/bin/env python3
import sys
import os
import argparse
import html

parser = argparse.ArgumentParser(description="Parse a logfile and creates a sortable/filterable/searchable HTML table.")
parser.add_argument('infile', metavar='<input file>', type=str, help="file to read, if '-', stdin is used")
parser.add_argument('outfile', metavar='<output file>', nargs='?', default='-', help="file to write, if '-' or no filename is given, stdout is used")
#parser.add_argument("-V", "--verbose", help="Be more verbose", action="store_true")
#parser.add_argument("-d", "--debug", help="debug flag", action='append', nargs="*")
parser.add_argument("-l", "--logtype", help="logfile type", choices=['spyglass', 'verilator'])
args = parser.parse_args()
 
html_h = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Excel Bootstrap Table Filter</title>
  <link href="https://www.jqueryscript.net/css/jquerysctipttop.css" rel="stylesheet" type="text/css">
    <!-- Load jQuery -->
  <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
  <!-- Load the plugin bundle. -->
  <script src="https://udif.github.io/verilator2html/dist/excel-bootstrap-table-filter-bundle.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" />
  <link rel="stylesheet" href="https://udif.github.io/verilator2html/dist/excel-bootstrap-table-filter-style.css" />
  <style>
  body {{ background-color:#fafafa;}}
  .container {{ margin:150px auto;}}
  </style>
</head>

<body>
<div class="jquery-script-clear"></div>
</div>
</div>
<div class="container">
  <div class="row">
    <div class="col-md-12">
      <table id="table" class="table table-bordered table-intel">
        <thead>
          <tr class="table-info">
            {}
          </tr>
        </thead>
        <tbody>
"""
html_t = """
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
  // Use the plugin once the DOM has been loaded.
  $(function () {
    // Apply the plugin 
    $('#table').excelTableFilter();
  });
</script>
</body>
</html>
"""

verilator_header =("Type", "File", "Line", "Col", "Message")
def convert_verilator_log(flog, fhtml):
  print(html_h.format("".join(["<th>"+i+"</th>" for i in verilator_header])), file=fhtml)
  for l in flog.readlines():
    if not l.startswith('%'):
      continue
    lw = ''
    for w in l.split(':', 4):
      lw += '<td>{}</td>'.format(html.escape(w))
    print('<tr>{}</tr>'.format(lw), file=fhtml)
  print(html_t, file=fhtml)

#ID       Rule                Alias               Severity    File                                                                                                                                         Line     Wt    Message
spyglass_header = ('ID', 'Rule', 'Alias', 'Severity', 'File', 'Line', 'Wt', 'Message')
spyg_hdr_pos = [0, 9, 29, 49, 61, 202, 211, 217, 0]
def convert_spyglass_log(flog, fhtml):
  s = spyg_hdr_pos 
  print(html_h.format("".join(["<th>"+i+"</th>" for i in spyglass_header])), file=fhtml)
  for l in flog.readlines():
    if not l.startswith('['):
      continue
    lw = ''
    s[-1] = len(l)
    for i in range(len(s)-1):
      lw += '<td>{}</td>'.format(html.escape(l[s[i]:s[i+1]].strip()))
    print('<tr>{}</tr>'.format(lw), file=fhtml)
  print(html_t, file=fhtml)

def convert_any_log(flog, fhtml):
  if args.logtype == 'verilator':
    convert_verilator_log(flog, fhtml)
  elif args.logtype == 'spyglass':
    convert_spyglass_log(flog, fhtml)

def convert_log(fhtml):
  if args.infile == "-":
    convert_any_log(sys.stdin, fhtml)
  else:
    with open(args.infile, "r") as flog:
      convert_any_log(flog, fhtml)

if args.outfile == "-":
  convert_log(sys.stdout)
else:
  with open(args.outfile, "w") as fhtml:
    convert_log(fhtml)



