#!c:\users\administrador\dropbox\django\sis_telemedicina\envtelemedicina\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'tldextract==1.6','console_scripts','tldextract'
__requires__ = 'tldextract==1.6'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('tldextract==1.6', 'console_scripts', 'tldextract')()
    )
