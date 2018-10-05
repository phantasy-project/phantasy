# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog

from .ui.ui_app_help import Ui_Dialog


HELP_QNA = '''
<div>
<p><strong>What is Trajectory Viewer App?</strong></p>
</div>
<div>
<p><em>Trajectory Viewer </em>is a GUI application built upon PyQt5, features the display for the physics status of the FRIB accelerator, as well as virtual accelerator(s).</p>
</div>
<div>
<p><strong>How to start up Trajectory Viewer App?</strong></p>
</div>
<div>
<p>Search&nbsp;<em>Trajectory Viewer </em>in the search box of Gnome's Activities, or locate it in the system menu, probably under the Other category.</p>
</div>
<div>
<p><strong>Configure the line style?</strong></p>
</div>
<div>
<p>First press <span style="color: #ff0000;">Stop</span> button in the <em>Controls Panel</em> area, then reach the configuration menu by right-clicking the figure, to adjust the line style, after that, press <span style="color: #ff0000;">Start</span> button again.</p>
</div>
'''

HELP_LIC = '''
<p>Copyright (c) 2018, Facility for Rare Isotope Beams<br />All rights reserved.</p>
<p>Redistribution and use in source and binary forms, with or without modification,<br />are permitted provided that the following conditions are met:</p>
<p>1. Redistributions of source code must retain the above copyright notice, this<br /> list of conditions and the following disclaimer.</p>
<p>2. Redistributions in binary form must reproduce the above copyright notice,<br /> this list of conditions and the following disclaimer in the documentation<br /> and/or other materials provided with the distribution.</p>
<p>3. Neither the name of the copyright holder nor the names of its contributors<br /> may be used to endorse or promote products derived from this software without<br /> specific prior written permission.</p>
<p>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND<br />ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED<br />WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE<br />DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR<br />ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES<br />(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;<br />LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON<br />ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT<br />(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS<br />SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</p>
'''

class HelpDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(HelpDialog, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle('Help')

        self.textBrowser_qna.setHtml(HELP_QNA)
        self.textBrowser_lic.setHtml(HELP_LIC)
