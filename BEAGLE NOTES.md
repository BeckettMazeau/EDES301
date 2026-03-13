BEAGLE NOTES

Cloud9IDE: http://192.168.7.2:3000/

Connecting to Internet
Connect: sudo /sbin/route add default gw 192.168.7.1
Test: ping www.google.com | ping 8.8.8.8
DNS:
sudo nano /etc/resolv.conf
▪ Add line: nameserver 8.8.8.8
▪ Exit nano: Ctrl-x (to eXit) → “Y” (for Yes) → <Enter> (to confirm file to write)
Sphinx "Independent Project" Checklist

Navigate:
cd "Project Name" (Use quotes if the name has spaces).

Initialize:
py -m sphinx.cmd.quickstart docs
Answer y to "Separate source and build".

Configure (docs/source/conf.py):
Path (Top of file):
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

Extensions (List): Add 'sphinx.ext.autodoc', 'sphinx.ext.napoleon'.

Mock Imports (Bottom of file):
autodoc_mock_imports = ['Adafruit_BBIO']
(Add other hardware libraries here like 'smbus' or 'time' separated by commas if needed)

Connect (docs/source/index.rst):
Add this block below the title (ensure a blank line above and below, and exactly 3 spaces for indent):

.. automodule:: file_name
   :members:
(Example: .. automodule:: blink_USR3 -- no .py extension!)

Generate / Re-run:
cd docs
py -m sphinx -a -b html source build/html
(Note: The -a flag forces Sphinx to rebuild everything from scratch so changes apply correctly)

Quick Troubleshooting for your structure:

The "Double Dot": Because you chose "Separate source and build," your conf.py is two levels deep (docs -> source), which is why the ../../ in step 3 is essential to "climb out" and see your .py files.