QT += quickcontrols2 websockets webview
QT -= widgets core gui

CONFIG += c++11
CONFIG += qtquickcompiler

SOURCES += src/main.cpp \
    src/libdecadence/client.cpp \
    src/libdecadence/auth.cpp \
    src/libdecadence/api.cpp \
    src/settings.cpp

RESOURCES += qml.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    src/libdecadence/client.h \
    src/libdecadence/auth.h \
    src/libdecadence/api.h \
    src/settings.h \
    src/models/RankingModel.h \
    src/models/UserModel.h \
    src/models/GameModel.h \
    src/models/TournamentModel.h \
    src/models/ChatMessageModel.h \
    src/models/AchievementModel.h

DISTFILES +=
