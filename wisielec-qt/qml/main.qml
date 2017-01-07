import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import "Components"

ApplicationWindow {
    visible: true
    width: 540
    height: 720
    title: qsTr("wisielec schopenhauera")

    StackView {
        id: stack
        anchors { top: parent.top; left: parent.left; right: parent.right; bottom: toolbar.top }
    }

    ToolBar {
        id: toolbar
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right; }
        RowLayout {
            anchors.fill: parent
            ToolButton {
                text: qsTr("\uE8F2")
                font.pixelSize: 24
                font.family: "Segoe MDL2 Assets"
                onClicked: chatBox.visible = true
            }
            Item { Layout.fillWidth: true }
            /*Switch {
                checked: true
                text: qsTr("Notifications")
            }*/
        }
    }

    ChatBox {
        id: chatBox;
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right; }
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
