#
#   Copyright 2013 La Honda Research Center, Inc.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re


def twiki2moin(txt, prefix):
    """Convert the text of a single TWiki page to MoinMoin markup

    txt is the TWiki input page content
    optional prefix is used to convert TWiki Web links to Moin subdirectories.
    returns the Moin equivalent

    """
    # Note: the approach used here involves multiple transformation passes
    # over the input.  Two things to be aware of: 
    #  1. The order of operations matters
    #  2. during conversion, txt contains _mixed_ TWiki and Moin markup 
    #
    # You have been warned - use the unit tests when making changes to
    # the conversion logic  :-)
    
    txt = process_variables(txt)	

    txt = process_meta(txt)

    txt = process_links(txt, prefix)

    txt = process_markup(txt)

    # remove signatures
    ## uncommento to enable 
    ## txt = re.compile("^-- Main.([a-z]+) - [0-9]+ [a-zA-Z]+ 200[0-9]\s*\n?", re.M).sub("", txt)

    txt = process_tables(txt)

    txt = process_html(txt)

    return txt

def process_html(txt):
    """convert various embedded html markup to Moin"""

    # HTML crud
    txt = re.compile(r"<br />").sub("\n", txt)
    txt = re.compile(r"</?em>").sub("''", txt)
    txt = re.compile(r"</?strong>").sub("'''", txt)
    txt = re.compile(r"&lt;").sub("<", txt)
    txt = re.compile(r"&gt;").sub(">", txt)
    txt = re.compile(r"&amp;").sub("&", txt)
    txt = re.compile(r"<p>(.*?)</p>", re.S).sub("\\1<<BR>>", txt)
    txt = re.compile(r"\B<pre>\b([^*\n]*?)</pre>\B").sub("`\\1`", txt)
    txt = re.compile(r"\B<pre>\b([^*]*?)</pre>\B").sub("{{{\n\\1}}}\n", txt)

    return txt

def process_markup(txt):

    # convert bold
    txt = re.compile(r"\*([^*].*?[^*])\*").sub("'''\\1'''", txt)
    # convert italic
    txt = re.compile(r"_([^_].*?[^_])_\b").sub("''\\1''", txt)
    # convert bold italic
    txt = re.compile(r"\b__([^_].*?[^_])__").sub("''''\\1''''", txt)

    # convert fixed and verbatim formats
    txt = re.compile(r"\B=\b([^*\n]*?)=\B").sub("`\\1`", txt)
    txt = re.compile(r"\B<verbatim>\b([^*\n]*?)</verbatim>\B").sub("`\\1`", txt)
    txt = re.compile(r"\B<verbatim>\b([^*]*?)</verbatim>\B").sub("{{{\n\\1}}}\n", txt)
    txt = re.compile(r"\B<literal>\b([^*\n]*?)</literal>\B").sub("`\\1`", txt)
    txt = re.compile(r"\B<literal>\b([^*]*?)</literal>\B").sub("{{{\n\\1}}}\n", txt)

    # convert definition list 
    # Three spaces, a dollar sign, the term, a colon, a space, followed by
    # the definition ( "   $ term: definition" -> "term:: definition" )
    txt = re.compile("   \$ (.*): (.*)").sub("\\1:: \\2", txt)

    # numbered lists
    txt = re.compile("(   )+[0-9] ").sub("\\1 1. ", txt)

    # convert headings
    txt = re.compile("^-?" + re.escape("---++++++") + "\s*(.*)$", re.M).sub("====== \\1 ======", txt)
    txt = re.compile("^-?" + re.escape("---+++++") + "\s*(.*)$", re.M).sub("===== \\1 =====", txt)
    txt = re.compile("^-?" + re.escape("---++++") + "\s*(.*)$", re.M).sub("==== \\1 ====", txt)
    txt = re.compile("^-?" + re.escape("---+++") + "\s*(.*)$", re.M).sub("=== \\1 ===", txt)
    txt = re.compile("^-?" + re.escape("---++") + "\s*(.*)$", re.M).sub("== \\1 ==", txt)
    txt = re.compile("^-?" + re.escape("---+") + "\s*(.*)$", re.M).sub("= \\1 =", txt)
    txt = re.compile("^-?" + re.escape("---#") + "\s*(.*)$", re.M).sub("= \\1 =", txt)

    # rules - html and twiki style 
    txt = re.compile(r"^\s*<hr ?/?>\s*$", re.M).sub("----", txt)
    txt = re.compile(r"^-?---.*$", re.M).sub("----", txt)

    return txt

def process_tables(txt):
    """Convert table syntax """

    # find table rows, then replace one by one 
    txt = re.compile(r"^\s*\|.*$", re.M).sub(convert_table_row, txt)

    return txt

def convert_table_row(matchobj):
    """convert a single table row"""

    row = matchobj.group(0)
    row = re.sub('\|', '||', row)
    return row

def process_variables(txt):
    """replace twiki variables with Moin counterparts"""

   # list of twiki variables, and their MoinMoin replacements
    twiki_moin_variables = [
        (r"%TOC%", "<<TableOfContents>>"),
        (r"%I%", "(!)"),
        (r"%X%", r"/!\\"),
        (r"%VBAR%", r"|"),
        (r"%CARET%", r"^"),
        (r"%ATTACHURL%/(\S*)", "[[attachment:\\2]]"),
    ]

    for mapping in twiki_moin_variables:	
        txt = re.compile("([^!]|^)" + mapping[0]).sub("\\1" + mapping[1], txt)
    return txt

def process_links(txt, prefix):
    """convert links to moin syntax"""

    # preprocess raw attachments into links
    txt = re.sub(r'[^\[][0,2](attachment:.*)[^\]][0,2]', 
                 '[[' + "\\1" + ']]', txt)
    # handle explicit links inside brackets [[link]]
    txt = re.sub(r'\[\[(.*?)\]\]', 
          lambda matchobj: '[[' + convert_link(matchobj, prefix) + ']]',
          txt)
    # handle prefix for WikiWords here 
    if prefix:
        wikiword_re = re.compile(r'(\s)([A-Z]\w+[A-Z]+\w+)')
        txt = wikiword_re.sub(r'\1' + prefix + '/' + r'\2', txt)

    return txt

def convert_link(matchobj, prefix):
    """convert the contents of a twiki link to MoinMoin Syntax """

    link = matchobj.group(1)
    # print 'before', link

    link = re.sub(r'\]\[', '|', link)
    if '|' not in link:
        # not a specific link; if it has spaces, make it a named link
        if ' ' in link.strip():
            link = link + '|' + link

    pieces = link.partition('|')
    first = pieces[0].replace(' ', '')
    # twiki forms it's topic by capitalizing 1st letter and 
    # removing space at render time.  We convert the link to 
    # do the same at conversion time
    if not (first.startswith('http:') or 
            first.startswith('https:') or
            first.startswith('file:') or
            first.startswith('attachment:')):
        first = first[0].capitalize() + first[1:]
        # convert SubWeb links to use / instead of .    
        first = first.replace('.', '/')
        # insert prefix if it's defined 
        if prefix:
            first = '/'.join([prefix, first])
    link = ''.join([first, pieces[1], pieces[2]])
    # print 'after', link
    return link

def process_meta(txt):
    """convert Twiki Meta lines"""

    txt = re.compile("^%META:.*%", re.M).sub("", txt)
    return txt
