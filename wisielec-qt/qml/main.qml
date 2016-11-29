import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    visible: true
    width: 540
    height: 720
    title: qsTr("wisielec schopenhauera")

    StackView {
        id: stack
        anchors.fill: parent;
    }

    Component.onCompleted: {
        /*if (appSettings.isLoggedIn) {
            stack.push("qrc:/Pages/MainPage.qml")
        } else {
            stack.push("qrc:/Pages/LoginPage.qml")
        }*/
        stack.push("qrc:/Pages/LoginPage.qml")
    }
}
