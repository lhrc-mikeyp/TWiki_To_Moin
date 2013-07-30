######################################
Twiki to MoinMoin conversion utility
######################################

twiki_to_moin is a command line utility to convert from TWiki to
MoinMoin.

It supports a comprehensive set of markup conversions, handles
attachments, and should convert most TWikis without any code
modification.

twiki_to_moin is intended to be relatively easy to expand for
additional markup, and includes unit tests for the various markup
conversions to speed development.

The code was developed under Python 2.7, and primarily tested against
TWiki 4.3.2 and MoinMoin 1.9.  It should work against most Twiki 4
sources, and target MoinMoin 1.8 or 1.9. It might work against Twiki 5.

The utility should be run under Linux or OS X.  No testing has been
done under Windows, and the file manipulations will probably not work.

homepage: https://github.com/lhrc-mikeyp/TWiki_To_Moin

*************
Installation
*************

There are no dependencies other than the Python standard library.

1. Download the source distribution TWiki_To_Moin-1.0.tar.gz 
2. ``tar xvf TWiki_To_Moin-1.0.tar.gz`` 
3. ``python setup.py install``

The source distribution will also install with pip and easy_install.

From source
===========

The source repository is at https://github.com/lhrc-mikeyp/TWiki_To_Moin

1. ``git clone https://github.com/lhrc-mikeyp/TWiki_To_Moin.git``
2. ``cd TWiki_To_Moin``
3. ``python setup.py install``

*******
Usage
*******

twiki_to_moin will convert a single TWiki to it's corresponding
MoinMoin equivalent. ``twiki_to_moin --help`` provides a basic
command line summary.

You will need to know the location if the twiki page directory (e.g.
/var/www/twiki/data/Main), the twiki data directory ( e.g.
/var/www/twiki/pub/Main), and read access to those files.

You will also need the destination for the MoinMoin files (e.g.
/var/www/moin-1.9.4/new_wiki/data/pages,) and enough space to store
the converted wiki.

The results are written to the console, and also appended to a
log file if the --logfile option is used.

The target is updated on each run without any warnings for existing files.

Remember to restart MoinMoin to recognize updated pages.

Converting a single Wiki
========================

If you have a main TWiki wiki in /var/www/twiki, and would like to
convert it to a MoinMoin wiki in /var/www/new_wiki::

    twiki_to_moin --logfile conversion.log /var/www/twiki/data/Main /var/www/twiki/pub/Main /var/www/moin-1.9.4/new_wiki/data/pages

Converting a TWiki sub-wiki
===========================

TWiki supports multiple sub-wiki's called webs.  A single web can
be converted to a MoinMoin wiki using the example above, and
specifying the correct TWiki directories.

twiki_to_moin also supports a --prefix option, which can be used
to add a 'parent' path to the pages while they are converted. This
allows a sub-wiki to be merged into an existing MoinMoin Wiki, while
avoiding page name conflicts by using MoinMoin's '/' feature.

Here is an example of converting two TWikis, Main, and Sandbox,
into a single destination MoinMoin wiki, with the second wiki
prefixed with 'SandboxPages' ::

    twiki_to_moin --logfile main.log /var/www/twiki/data/Main /var/www/twiki/pub/Main /var/www/moin-1.9.4/new_wiki/data/pages
    twiki_to_moin --logfile sandbox.log --prefix SandboxPages /var/www/twiki/data/Sandbox /var/www/twiki/pub/Sandbox /var/www/moin-1.9.4/new_wiki/data/pages

**********************
Capabilities
**********************

TWiki markup supported
======================

- bold, italic, bold italic
- fixed and verbatim converted to {{{ }}}  
- definition lists 
- numbered lists
- seven levels of headers
- horizontal rules
- tables
- TWiki variables - %TOC%, %I%, %X%, %VBAR%, %CARET
- Page attachments
- many types of links, including the capitalization and space 
  removal TWiki does at runtime.

HTML markup supported
=====================

- <br>
- <em>
- <strong>
- &lt; &gt; &amp;
- <p>   
- <pre>

Unrecognized html markup is passed through untouched.

SubWiki Support
===============

When processing wikis using the --prefix option, links in the source
wiki are fixed to refer to the correct MoinMoin path in the destination
wiki.  Explicit SubWiki links of the form wiki.topic are also
converted.


**********************
Limitations and Issues
**********************

Many markup conversion issues arise because TWiki is extremely
flexible in the markup it accepts, and generally renders it without
reporting errors, while MoinMoin is more structured. This often
results is unusual source markup, probably cut and pasted from other
sources. The conversion attemts to handle many of these issues,
especially embedded html, but it doesn't handle everything. The
best way to catch these issues is to look at the converted wiki,
since unusual markup is left untouched. If you see a common pattern,
log an issue or submit a patch.

Beyond these general markup conversion issues, here are some other
limitations:

1. Doesn't convert history and versions; only the current TWiki data is 
   converted.
#. twiki_to_moin only runs under Linux and OS X.
#. There is minimal awareness of code pages; the results are UTF-8 encoded, 
   reads assume latin1 code page.
#. TWiki metadata lines are just stripped from the output.
#. TWiki allows links embedded in headers, MoinMoin doesn't support this.  
   In these cases, the converted wiki will just have the MoinMoin link 
   syntax in the header.
#. empty headers (e.g. ---+<nl> ) cause problems.
#. embedded html <a> links are not converted.
#. No attempt is made to check for locking or active edits.  It is 
   assumed the source and target wikis are not active.
#. Embedded images using html <img> markup are not handled.
#. The list of supported TWiki variables should be expanded.
#. \* as a bullet with * as bold inside a paragraph is not handled. 
#. TWiki signatures are left in place.
#. Needs to be upgraded to MoinMoin 2.
#. Needs to be converted to Python 3.
#. There are never enough tests.

*************
Hacking
*************

Some guidelines if you would like to hack on the code.

Workflow
========

1. The git trunk is current and should always be working.
#. Development work happens in branches, and is merged to trunk when complete.
#. Pull requests are welcome, against trunk or a branch.
#. New code, expecially conversions, should include unit tests.

Code and Logic
==============

The drectory organization is a standard Python package, intended to support
the Python installers.

**twiki_to_moin/__init__.py** contains the command line driver.

**twiki_to_moin/conversion.py** contains the markup conversion code.

**twiki_to_moin/copying.py** contains the file processing code.

**twiki_to_moin/tests** contains the unit tests.

Conversion Logic
----------------

The conversion is done by reading the TWiki source page, and applying
multiple transformation passes to the input.  Most transformation
passes use regular expressions to perform the substitution. 

The conversion has been broken into several pieces:

- variables
- metadata
- links
- markup
- tables
- html conversions
    
There are a few things to be aware of when modifying the conversion logic:

1. The order of operations matters.
2. During conversion, txt contains _mixed_ TWiki and Moin markup. 
3. Use very specific regular expressions to avoid side-effects.

To modify the conversion logic, the easiest approach is to write a
unit test with the original and expected results, and use that to
develop the conversion logic.

``python setup.py test`` will run the unit tests.

If you're stuck, submit a pull request with just the unit test.

More TWiki syntax examples from the real world are also needed.

********************
History and Credits
********************

This code is more or less a complete rewrite of the conversion
scripts found on http://moinmo.in/TwikiConverter

I believe the original scripts were originally developed by Bill
Trost, Erich ?, Reimar Bauer, Thomas Waldmann, and perhaps others.
They all deserve credit for working out the general process.

