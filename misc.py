#
# Copyright (C) 2015 Michael B. Kulik
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import umake.frameworks.baseinstaller
from bs4 import BeautifulSoup
import os, urllib, logging, shutil
from os.path import join, isfile
from decompressor import Decompressor
from umake.interactions import DisplayMessage, UnknownProgress
from umake.network.download_center import DownloadCenter, DownloadItem
from umake.tools import create_launcher, get_application_desktop_file,\
    ChecksumType, Checksum, MainLoop
from umake.ui import UI

logger = logging.getLogger(__name__)

class MiscCategory(umake.frameworks.BaseCategory):
    def __init__(self):
        super().__init__(name="Misc",
                         description="Miscellaneous Frameworks for ubuntu-make",
                         logo_path=None)

class Popcorntime(umake.frameworks.baseinstaller.BaseInstaller):
    """Popcorntime Movie Watcher"""

    def __init__(self, category):
        super().__init__(name="Popcorntime",
                         description="Popcorntime torrent video player",
                         category=category,
                         download_page=None,
                         only_on_archs=['amd64'],
                         desktop_filename='popcorntime.desktop')

    def download_provider_page(self):
        response = urllib.request.urlopen('http://popcorntime.io')
        htmlDocument = response.read()
        soupDocument = BeautifulSoup(htmlDocument, 'html.parser')
        link = soupDocument.find_all('li', "download dl-lin-64")[0]
        fileURL = link.a.get('href')
        fileName = os.path.basename(fileURL)
    
        self.download_requests.append(DownloadItem('http://104.236.185.158/build/' + fileName))
        self.start_download_and_install()

    def post_install(self):
        """Create the launcher"""
        icon_filename = "popcorntime.png"
        icon_path = join(self.install_path, icon_filename)
        exec_path = '"{}" %f'.format(join(self.install_path, "Popcorn-Time"))
        comment = "The Popcorn-Time video player"
        categories = "Video;"
        create_launcher(self.desktop_filename,
                        get_application_desktop_file(name="Popcorn-Time",
                                                     icon_path=icon_path,
                                                     exec=exec_path,
                                                     comment=comment,
                                                     categories=categories))
        
    @property
    def is_installed(self):
        # check path and requirements
        if not super().is_installed:
            return False
        if not isfile(join(self.install_path, "Popcorntime")):
            logger.debug("{} binary isn't installed".format(self.name))
            return False
        return True

        

class Drjava(umake.frameworks.baseinstaller.BaseInstaller):
    """The DrJava IDE"""
    
    def __init__(self, category):        
        super().__init__(name="DrJava",
                         description="DrJava IDE",
                         category=category,
                         download_page=None,
                         only_on_archs=['i386','amd64'],
                         desktop_filename='drjava.desktop',
                         packages_requirements=['openjdk-7-jdk'])


    def download_provider_page(self):
                download_url= "http://downloads.sourceforge.net/project/drjava/1.%20DrJava%20Stable%20Releases/drjava-stable-20140826-r5761/drjava-stable-20140826-r5761.jar?r=&ts=1439498832&use_mirror=iweb"
        self.download_requests.append(DownloadItem(download_url))
        self.start_download_and_install()

    def decompress_and_install(self, fd):
        UI.display(DisplayMessage("Installing {}".format(self.name)))
        
        if not os.path.exists(self.install_path):
            os.mkdir(self.install_path)
        
        shutil.copyfile(fd.name, self.install_path + '/drjava.jar')

        self.post_install()

        # Mark as installation done in configuration
        self.mark_in_config()

        UI.delayed_display(DisplayMessage("Installation done"))
        UI.return_main_screen()

    def post_install(self):
        """Create the launcher"""
        icon_filename = ""
        icon_path = join(self.install_path, icon_filename)
        exec_path = 'java -jar {} %f'.format(join(self.install_path, "drjava.jar"))
        comment = "DrJava IDE"
        categories = "Developement;IDE;"
        create_launcher(self.desktop_filename,
                        get_application_desktop_file(name="DrJava",
                                                     icon_path=icon_path,
                                                     exec=exec_path,
                                                     comment=comment,
                                                     categories=categories))

        
    @property
    def is_installed(self):
        if not super().is_installed:
            return False
        if not os.path.isfile(os.path.join(self.install_path, "DrJava")):
            logger.debug("{} binary isn;t installed".format(self.name))
            return False
        return True
