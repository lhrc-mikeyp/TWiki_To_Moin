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
import os
from os.path import isdir
import sys

import twiki_to_moin
#import twiki_to_moin.conversion as conversion
#import twiki_to_moin.copying as copying 


#TODO(mikeyp) fix version for release
__version__ = '0.3'

# constants used by Moin when mapping URL's to file names
moinslash = '(2f)'
moindash = '(2d)'
moinspace = '(2d)'

def run():

    #TODO(mikeyp) add command line parser/driver 
    print "run not implemented"
    return 

    # main("../awiki/data/Main", "moin-1.3.5/wiki/data/pages", "../awiki/pub/Main")
    twiki_page_dir = sys.argv[1]
    moin_page_dir = sys.argv[2]
    twiki_data_dir = sys.argv[3]
    prefix = sys.argv[4:]

    main(twiki_page_dir, moin_page_dir, twiki_data_dir, prefix)

def main(old_dir, new_dir, data_dir=None, prefix=[]):
    # print "+++ processing", old_dir, "using prefix", prefix
    names = os.listdir(old_dir)
    for name in names:
        if name[-4:] == ".txt":
             # fixup moin page names
            topic = moinslash.join(prefix + [name[:-4]])
            topic = re.compile(r"-").sub(moindash, topic)
            topic = re.compile(r" ").sub(moinspace, topic)
            print topic

            txt = file(os.path.join(old_dir, name)).read()
            twiki_to_moin.copying.make_page(new_dir, topic, twiki_to_moin.conversion.twiki2moin(txt, prefix))
            if data_dir:
                twiki_to_moin.copying.copy_attachments(new_dir, data_dir, name[:-4], topic, txt)
	else:
            path = old_dir + '/' + name
            if isdir(path):
                main(path, new_dir, data_dir + "/" + name, prefix + [name])


