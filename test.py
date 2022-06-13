from tosclib import verify
from tosclib import etosc2
from xml.etree.ElementTree import fromstring

xml = """
<value>
<key>x</key>
<locked>0</locked>
<lockedDefaultCurrent>0</lockedDefaultCurrent>
<default>0</default>
<defaultPull>0</defaultPull>
</value>
"""

e = fromstring(xml)

root = etosc2.load("docs/demos/files/controls.tosc")
e = root[0]

ctrl = verify.to_ctrl(e)

print(ctrl.children)