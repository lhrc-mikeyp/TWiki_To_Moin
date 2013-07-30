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

import unittest

import twiki_to_moin.conversion as tm

class VariableTests(unittest.TestCase):

    def test_toc(self):
        twiki = "%TOC%"
        moin = "<<TableOfContents>>"
        self.assertEqual(tm.process_variables(twiki), moin)

        twiki = "!%TOC%"
        moin = "!%TOC%"
        self.assertEqual(tm.process_variables(twiki), moin)

    def test_info(self):
        twiki = "%I%"
        moin = "(!)"
        self.assertEqual(tm.process_variables(twiki), moin)
        twiki = "!%I%"
        moin = "!%I%"
        self.assertEqual(tm.process_variables(twiki), moin)

    def test_alert(self):
        twiki = "%X%"
        moin = "/!\\"
        self.assertEqual(tm.process_variables(twiki), moin)
        twiki = "!%X%"
        moin = "!%X%"
        self.assertEqual(tm.process_variables(twiki), moin)

    def test_vbar(self):
        twiki = "%VBAR%"
        moin = "|"
        self.assertEqual(tm.process_variables(twiki), moin)
        twiki = "!%VBAR%"
        moin = "!%VBAR%"
        self.assertEqual(tm.process_variables(twiki), moin)

    def test_vbar(self):
        twiki = "%CARET%"
        moin = "^"
        self.assertEqual(tm.process_variables(twiki), moin)
        twiki = "!%CARET%"
        moin = "!%CARET%"
        self.assertEqual(tm.process_variables(twiki), moin)

    def test_attachurl(self):
        twiki = "%ATTACHURL%/image.jpg"
        moin = "[[attachment:image.jpg]]"
        self.assertEqual(tm.process_variables(twiki), moin)

        twiki = "!%ATTACHURL%/image.jpg "
        moin = "!%ATTACHURL%/image.jpg "
        self.assertEqual(tm.process_variables(twiki), moin)


class MetaTests(unittest.TestCase):
    "Tests for %META% lines"

    def test_attachment(self):
        twiki = "%META:FILEATTACHMENT{}%"
        moin  = ""
        self.assertEqual(tm.process_meta(twiki), moin)

    def test_meta(self):
        twiki = """%META:TOPICINFO{version="1.6" date="976762663" author="LastEditorWikiName" format="1.0"}%
%META:TOPICMOVED{from="Codev.OldName" to="Codev.NewName" by="TopicMoverWikiName" date="976762680"}%
topic info
%META:TOPICPARENT{name="NavigationByTopicContext"}%
%META:FILEATTACHMENT{name="Sample.txt" version="1.3" ... }%
%META:FILEATTACHMENT{name="Smile.gif" version="1.1" ... }%
%META:FORM{name="WebFormTemplate"}%
%META:FIELD{name="OperatingSystem" value="OsWin"}%
%META:FIELD{name="TopicClassification" value="PublicFAQ"}%
"""
        moin  = """

topic info






"""
        self.assertEqual(tm.process_meta(twiki), moin)


class LinkTests(unittest.TestCase):
    "Tests for link conversion"

    # TODO need tests for prefix 
    def test_simple(self):
        twiki = "[[SimpleLink]]"
        moin  = "[[SimpleLink]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

    def test_lowercase(self):
        twiki = "[[simplelink]]"
        moin  = "[[Simplelink]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

    def test_simple_spaces(self):
        twiki = "[[Simple Link]]"
        moin  = "[[SimpleLink|Simple Link]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

    def test_wikiword(self):
        twiki = "SimpleLink"
        moin  = "SimpleLink"
        self.assertEqual(tm.process_links(twiki, ""), moin)

    def test_specific(self):
        twiki = "[[SimpleLink][A Friendly name]]"
        moin = "[[SimpleLink|A Friendly name]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

    def test_http(self):
        twiki = "[[http://www.example.com]]"
        moin = "[[http://www.example.com]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

        twiki = "[[http://www.example.com][Example.com]]"
        moin = "[[http://www.example.com|Example.com]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

        twiki = "[[https://www.example.com]]"
        moin = "[[https://www.example.com]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

        twiki = "[[https://www.example.com][Example.com]]"
        moin = "[[https://www.example.com|Example.com]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

    def test_attachment(self):
        "tests for attachment links"

        # by the time we process links, a bare %ATTACHURL% should have 
        # been converted to [[attachment: ]], so the test for that 
        # case is under VariableTests

        twiki = "[[attachment:something.jpg][Picture]]"
        moin = "[[attachment:something.jpg|Picture]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)

        twiki = "[[attachment:something.jpg]]"
        moin = "[[attachment:something.jpg]]"
        self.assertEqual(tm.process_links(twiki, ""), moin)


class MarkupTests(unittest.TestCase):
    "Tests for markup conversion"

    def test_italic(self):
        twiki = "_italic_"
        moin  = "''italic''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "_italic_word_"
        moin  = "''italic_word''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "_italic sentence words_"
        moin  = "''italic sentence words''"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_bold(self):
        twiki = "*bold*"
        moin  = "'''bold'''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "*bold_word*"
        moin  = "'''bold_word'''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "*bold sentence words*"
        moin  = "'''bold sentence words'''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "*bold* sentence *words*"
        moin  = "'''bold''' sentence '''words'''"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_bold_italic(self):
        twiki = "__bold_italic__"
        moin  = "''''bold_italic''''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "__bold_italic_word__"
        moin  = "''''bold_italic_word''''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "__bold_italic sentence words__"
        moin  = "''''bold_italic sentence words''''"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "__bold_italic__ sentence __words__"
        moin  = "''''bold_italic'''' sentence ''''words''''"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_fixed(self):
        twiki = "=fixed="
        moin  = "`fixed`" 
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "=fixed words="
        moin  = "`fixed words`"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_verbatim(self):
        twiki = "<verbatim>something</verbatim>"
        moin  = "`something`"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_verbatim_multiline(self):
        twiki = """
<verbatim>something
a second line
</verbatim>"""
        moin  = """
{{{
something
a second line
}}}
"""
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_literal(self):
        twiki = "<literal>something</literal>"
        moin  = "`something`"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_literal_multiline(self):
        twiki = """
<literal>something
a second line
</literal>"""
        moin  = """
{{{
something
a second line
}}}
"""
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_definition_list(self):
        twiki = "   $ MoinMoin: A great Wiki software"
        moin = "MoinMoin:: A great Wiki software"
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_numbered_list(self):
        twiki = "   1. Item 1"
        moin = "   1. Item 1" 
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_bulleted_list(self):
        twiki = "   * item"
        moin = "   * item"
        self.assertEqual(tm.process_markup(twiki), moin)
  
        twiki = """
   * item
      * subitem
   * item 2
      * subitem
      * subitem 2
"""
        moin = """
   * item
      * subitem
   * item 2
      * subitem
      * subitem 2
"""
        self.assertEqual(tm.process_markup(twiki), moin)
  
    def test_headings(self):
        twiki = "---++++++ Heading level 6"
        moin = "====== Heading level 6 ======"
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "---+++++ Heading level 5"
        moin = "===== Heading level 5 ====="
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "---++++ Heading level 4"
        moin = "==== Heading level 4 ===="
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "---+++ Heading level 3"
        moin = "=== Heading level 3 ==="
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "---++ Heading level 2"
        moin = "== Heading level 2 =="
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = "---+ Heading level 1"
        moin = "= Heading level 1 ="
        self.assertEqual(tm.process_markup(twiki), moin)

        # TODO check this - is this even legal in twiki ?
        twiki = "---# Heading level 1"
        moin = "= Heading level 1 ="
        self.assertEqual(tm.process_markup(twiki), moin)

    def test_horizontal_rule(self):
        twiki = '<hr />'        
        moin = '----'        
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = '--'        
        moin = '--'        
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = '---'        
        moin = '----'        
        self.assertEqual(tm.process_markup(twiki), moin)

        twiki = '----'        
        moin = '----'        
        self.assertEqual(tm.process_markup(twiki), moin)


class HTMLTests(unittest.TestCase):
    "Tests for html conversion"

    def test_break(self):
        twiki = '<br />'        
        moin = '\n'        
        self.assertEqual(tm.process_html(twiki), moin)

    def test_emphasis(self):
        twiki = "<em>emphasis</em>"
        moin = "''emphasis''"        
        self.assertEqual(tm.process_html(twiki), moin)

    def test_strong(self):
        twiki = "<strong>strong</strong>"
        moin = "'''strong'''"        
        self.assertEqual(tm.process_html(twiki), moin)

    def test_entities(self):
        twiki = "&lt;"
        moin = "<"
        self.assertEqual(tm.process_html(twiki), moin)

        twiki = "&gt;"
        moin = ">"
        self.assertEqual(tm.process_html(twiki), moin)

        twiki = "&amp;"
        moin = "&"
        self.assertEqual(tm.process_html(twiki), moin)

    def test_paragraph(self):
        twiki = "<p>paragraph of text</p>"
        moin = "paragraph of text<<BR>>"
        self.assertEqual(tm.process_html(twiki), moin)

        twiki = "<p>not paragraph of text"
        moin = "<p>not paragraph of text"
        self.assertEqual(tm.process_html(twiki), moin)

        twiki = """
<p>a multiline 
paragraph
</p>
"""
        moin = """
a multiline 
paragraph
<<BR>>
"""
        self.assertEqual(tm.process_html(twiki), moin)

    def test_pre(self):
        twiki = "<pre>This is preformatted content</pre>"
        moin = "`This is preformatted content`"
        self.assertEqual(tm.process_html(twiki), moin)
    
    def test_pre_multiline(self):
        twiki = """
<pre>This is preformatted
code
content
</pre>"""
        moin = """
{{{
This is preformatted
code
content
}}}
"""
        self.assertEqual(tm.process_html(twiki), moin)

class TableTests(unittest.TestCase):
    "tests for tables"

    def test_table(self):
        twiki = """
|header 1|header2|header3|
|data 1 1 | data 1 2 | data 1 3|
|data 2 1 | data 2 2 | data 2 3|
"""
        moin = """
||header 1||header2||header3||
||data 1 1 || data 1 2 || data 1 3||
||data 2 1 || data 2 2 || data 2 3||
"""
        self.assertEqual(tm.process_tables(twiki), moin)

    def test_not_table(self):
        twiki = """something |header 1|header2|header3|"""
        moin = """something |header 1|header2|header3|"""
        self.assertEqual(tm.process_tables(twiki), moin)

def suite():

    test_cases = [ 
        VariableTests,
        MetaTests,
        LinkTests,
        MarkupTests,
        TableTests,
        HTMLTests,
    ]
    test_suite = unittest.TestSuite(
        [ unittest.TestLoader().loadTestsFromTestCase(test_case)
        for test_case in test_cases ]
    )
    return test_suite

