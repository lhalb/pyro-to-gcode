pyuic5 -x ./gui/mainUI.ui -o ./gui/mainUI.py
pyuic5 -x ./gui/cncImportUI.ui -o ./gui/cncimportUI.py
pyuic5 -x ./gui/errorDialogueUI.ui -o ./gui/errordiaUI.py
pyrcc5 ./gui/icons/icns.qrc -o ./icns_rc.py