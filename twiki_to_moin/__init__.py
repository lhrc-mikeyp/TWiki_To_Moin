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
"""
TWiki to MoinMoin conversion

"""
import logging 
from optparse import OptionParser
import os
from os.path import isdir, join 
import re
import sys

__version__ = '1.0'

# set up console logging
log = logging.getLogger('twiki_to_moin')
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
log.addHandler(console_handler)

# constants used by Moin when mapping URL's to file names
moinslash = '(2f)'
moindash = '(2d)'
moinspace = '(2d)'

def run(args):
    """"entry point for command line driver

    args is the command line, in the form of sys.argv
    """

    usage_msg = """%prog [options] <twiki_page_dir> <twiki_data_dir> <moin_page_dir>

examples:

    %prog awiki/data/Main awiki/pub/Main moin-1.3.5/wiki/data/pages 

    %prog --help 

    """
    parser = OptionParser(usage=usage_msg, 
                          prog=os.path.basename(args[0]))

    parser.add_option("-p", "--prefix", 
                  action="store", type="string", dest="prefix", default="",
                  help="not sure; historical and weird ")

    parser.add_option("-l", "--logfile", 
                  action="store", type="string", dest="logfile", default=None,
                  help="optional log file ")

    parser.add_option("-v", "--verbose", 
                  action="count", dest="debug", default=0,
                  help="log additional detail during conversion")

    (options, arguments) = parser.parse_args(args[1:])
    if len(arguments) != 3:
        parser.error("Three arguments are required.")
        # parser.error() will exit 

    # adjust log level, set up file logging
    if options.debug == 1:
        log.setLevel(logging.DEBUG)
        msg = "Enabled verbose logging."
        log.debug(msg)   
    if options.logfile:    
        fh = logging.FileHandler(options.logfile)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        log.addHandler(fh)
        msg = "Enabled logging to file: " + options.logfile
        log.info(msg)

    log.info("Beginning conversion run")

    twiki_page_dir = arguments[0]
    twiki_data_dir = arguments[1]
    moin_page_dir = arguments[2]
    prefix = options.prefix

    log.info("Running with arguments:")
    msg = "TWiki page dir: {0} Twiki data dir: {1} Destination dir: {2}".format(
        twiki_page_dir, twiki_data_dir, moin_page_dir)
    log.info(msg)

    # validate arguments 
    if not os.path.isdir(twiki_page_dir):
        msg = "The TWiki page directory {0} does not exist.".format(
            twiki_page_dir)
        log.error(msg)
        log_exit(1)
    if not os.path.isdir(twiki_data_dir):
        msg = "The TWiki data directory {0} does not exist.".format(
            twiki_data_dir)
        log.error(msg)
        log_exit(1)
    if not os.path.isdir(moin_page_dir):
        msg = "The MoinMoin data directory {0} does not exist.".format(
            moin_page_dir)
        log.info(msg)
        msg = "The MoinMoin data directory will be created if possible." 
        log.info(msg)

    # validate source and targets are different !
    if os.path.abspath(twiki_page_dir) == os.path.abspath(moin_page_dir):
        msg = "The target directory is the same as the twiki page directory."
        log.error(msg)
        log_exit(1)
    if os.path.abspath(twiki_data_dir) == os.path.abspath(moin_page_dir):
        msg = "The target directory is the same as the twiki data directory."
        log.error(msg)
        log_exit(1)
        
    convert_directory(twiki_page_dir,twiki_data_dir, moin_page_dir, prefix)

    log_exit(0)

def log_exit(code):
    if code == 0:
        log.info("Successfully completed conversion run.")
        sys.exit(0)
    else:
        log.info("Conversion completed with errors.")
        sys.exit(code)
        
def convert_directory(old_dir, data_dir, new_dir, prefix=''):
    """Convert a directory of TWiki data to MoinMoin

    recursively calls itself to handle the TWiki directory structure

    """
    from twiki_to_moin.conversion import twiki2moin
    from twiki_to_moin.copying import make_page, copy_attachments

    msg = "Processing TWiki directory {0} using prefix {1}".format(
        old_dir, prefix)
    log.info(msg)
    # TODO - this really should use os.walk()
    names = os.listdir(old_dir)
    for name in names:
        if name[-4:] == ".txt":
             # convert filename from TWiki to moin format
            topic = name[:-4]
            if prefix:
                topic = join(prefix, topic)
            topic = re.compile(r"/").sub(moinslash, topic)
            topic = re.compile(r"-").sub(moindash, topic)
            topic = re.compile(r" ").sub(moinspace, topic)
            msg = "Converting TWiki page {0} to Moin topic {1}".format(
                name, topic)
            log.info(msg)

            txt = file(os.path.join(old_dir, name)).read()
            new_txt = twiki2moin(txt, prefix)
            make_page( new_dir, topic, new_txt) 
            if data_dir:
                copy_attachments( new_dir, data_dir, name[:-4], topic, txt)
        elif isdir(join(old_dir, name)):
                convert_directory(join(old_dir, name), 
                    new_dir, join(data_dir, name), join(prefix, name))
