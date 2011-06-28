'''
rggStyles - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Various stylesheets for the application.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

standard = ''''''

test = '''background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf);'''

celtica = '''
*{ background-image: url(data/styles/bg_celt.png);}

QLineEdit,QTextEdit,QListWidget{ background: #f3f2e5; }

QLabel { background: #f3f2e5; }

QPushButton { background: #e5e2c9; }

QMenu {
     background: #c8c290;
 }
 
QMenu::item:selected {
     background: #625c2e;
 }
 
QMenu::item:pressed {
     background: #f3f2e5;
 }

QMenuBar::item {
     background: #c8c290;
 }

QMenuBar::item:selected {
     background: #f3f2e5;
 }

QMenuBar::item:pressed {
     background: #625c2e;
 }

'''

sheets = {"Default":standard, "Test":test, "Celtic":celtica}