import os
from pyshortcuts import make_shortcut

target = "C://Users//rmarinelli4//PycharmProjects//Real Estate Data//dist//main//"
icon = r"C://Users//rmarinelli4//PycharmProjects//Real Estate Data//House.ico"

make_shortcut(target, name='MyApp',
                        icon= icon)

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') # path to where you want to put the .lnk
path = os.path.join(desktop, 'NameOfShortcut.lnk')


