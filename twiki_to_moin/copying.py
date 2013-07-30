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
import errno
import logging
import os
import re
import shutil

log = logging.getLogger('twiki_to_moin')

def make_page(new_dir, topic, txt):
    txt = unicode(txt, "latin1").encode("utf8")
    name = os.path.join(new_dir, topic)
    try:
        os.makedirs(os.path.join(name,"revisions"))
    except OSError as detail:
        if detail.errno == errno.EEXIST: 
            pass
        else:
            raise 

    # XXX these files need to be closed !
    file(os.path.join(name,"current"), "w").write("00000001")
    file(os.path.join(name,"revisions","00000001"), "w").write(txt)

def copy_attachments(new_dir, data_dir, twiki_name, moin_topic, txt):
    name = os.path.join(new_dir,moin_topic)
    try:
        os.makedirs(os.path.join(name,"attachments"))
    except OSError as detail:
        if detail.errno == errno.EEXIST: 
            pass
        else:
            raise 
    attachments = re.compile("%META:FILEATTACHMENT.*attachment=\"(.*?)\"\s",
        re.M).findall(txt)
    for attachment in attachments:
        msg = "processing attachment {0}".format(attachment)
        log.info(msg)
        try:
            #print "src: %s, dest: %s" % (
            #    os.path.join(data_dir,twiki_name,attachment), 
            #    os.path.join(name,"attachments",attachment))
            shutil.copyfile(
                os.path.join(data_dir, twiki_name, attachment),
                os.path.join(name, "attachments", attachment))
        except IOError:
            msg = "Could not copy attachment {0} for topic {1}".format(
                attachment, topic)
            log.warn(msg)
            pass

