import os

import Db.database as db

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(cwd_dir, 'downloads/')


def get_newest_link(software, platform):
    """database request for download-link of newest version"""
    link = db.get_software_link(software.lower(), platform.lower())
    return link
