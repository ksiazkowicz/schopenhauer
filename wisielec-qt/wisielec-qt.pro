QT += quickcontrols2 websockets
QT -= widgets core gui

CONFIG += c++11
CONFIG += qtquickcompiler

SOURCES += main.cpp \
    src/SchopenhauerClient.cpp

RESOURCES += qml.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    src/SchopenhauerClient.h

DISTFILES +=
