# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog

from .ui_app_help import Ui_Dialog


HELP_QNA = '''
<html>
<p><strong>What is Unicorn App?</strong></p>
<p><em>Unicorn App</em> is a GUI application built upon PyQt5, features easy access and control to the <em>UNICORN</em> service, which is a web service to interpret the units between engineering and physics fields, typically for the accelerator system.</p>
<p><strong>How to start up Unicorn App?</strong></p>
<p>Search <em>Unicorn App </em>in the search box of Gnome's Activities, or locate it in the system menu, probably under the Other category.</p>
<p><strong>How to initialize the database?</strong></p>
<p>If for the first time <em>Unicorn App</em> is started, there might be the issue like the database cannot be located, thus 'Internal Server Error' happens, which could be resolved by resetting the database: <span style="color: #ff0000;">Edit</span> &rarr; <span style="color: #ff0000;">Preferences</span>&nbsp;&rarr; <span style="color: #ff0000;">Unicorn WebApp</span> &rarr; <span style="color: #ff0000;">Database</span>, push <span style="color: #ff0000;">Reset</span> button, and push <span style="color: #ff0000;">OK</span> button.</p>
<p><strong>How to update database?</strong></p>
<p>The database may need to update when unicorn-webapp is updated, simply push <span style="color: #ff0000;">Reset</span> database button, keep in mind that all user changes will be gone, e.g. invoked count.</p>
<p><strong>Internal Server Error?</strong></p>
<p>See <em>How to initialize the database</em>?</p>
<p><strong>Change the font size?</strong></p>
<p>This could be achieved by change the page zoom factor: <span style="color: #ff0000;">Edit</span> &rarr; <span style="color: #ff0000;">Preferences</span>&nbsp;&rarr; <span style="color: #ff0000;">Style</span> &rarr; <span style="color: #ff0000;">Page Zoom</span>, change the value that fit your screen, push <span style="color: #ff0000;">OK</span> to apply.</p>
<p><strong>Start UNICORN at another port?</strong></p>
<p>By default, the UNICORN service is started with random port number, if the user wanna start with some other port, the following procedure should work: <span style="color: #ff0000;">Edit</span> &rarr; <span style="color: #ff0000;">Preferences</span>&nbsp;&rarr; <span style="color: #ff0000;">Unicorn WebApp</span> &rarr; <span style="color: #ff0000;">Service Status</span>, push <span style="color: #ff0000;">STOP</span> button to stop the current one, and change the port number at <span style="color: #ff0000;">Base URL</span> line, then Push <span style="color: #ff0000;">START</span> and <span style="color: #ff0000;">OK</span>.</p>
<p><strong>Stop current UNICORN service?</strong></p>
<p><span style="color: #ff0000;">Edit</span> &rarr; <span style="color: #ff0000;">Preferences</span>&nbsp;&rarr; <span style="color: #ff0000;">Unicorn WebApp</span> &rarr; <span style="color: #ff0000;">Service Status</span>, push <span style="color: #ff0000;">STOP</span> button and <span style="color: #ff0000;">OK</span>.</p>
<p><strong>Clean up residual services?</strong></p>
<p>Sometimes, the started UNICORN service has not been stopped properly, clean up could be done by <span style="color: #ff0000;">Edit</span> &rarr; <span style="color: #ff0000;">Preferences</span>&nbsp;&rarr; <span style="color: #ff0000;">Advance</span>, push <span style="color: #ff0000;">Update</span> button to see all alive services, and push <span style="color: #ff0000;">Clean Up</span> to stop all but the current working one, if push <span style="color: #ff0000;">Update</span> button again, there should be only the current one alive.</p>
</html>
'''

HELP_LIC = '''
<html>
<p>The MIT License</p>
<p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
<p>Permission is hereby granted, free of charge, to any person obtaining a copy<br />of this software and associated documentation files (the "Software"), to deal<br />in the Software without restriction, including without limitation the rights<br />to use, copy, modify, merge, publish, distribute, sublicense, and/or sell<br />copies of the Software, and to permit persons to whom the Software is<br />furnished to do so, subject to the following conditions:</p>
<p>The above copyright notice and this permission notice shall be included in<br />all copies or substantial portions of the Software.</p>
<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR<br />IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,<br />FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE<br />AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER<br />LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,<br />OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN<br />THE SOFTWARE.</p>
</html>
'''

class HelpDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(HelpDialog, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle('Help')

        self.textBrowser_qna.setHtml(HELP_QNA)
        self.textBrowser_lic.setHtml(HELP_LIC)
