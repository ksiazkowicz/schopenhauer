import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import "Components"

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 540
    height: 720
    title: qsTr("Wisielec Schopenhauera")

    Item {
        id: busyOverlay
        anchors { fill: parent }
        visible: false
        z: 100
        Rectangle {
            anchors { fill: parent }
            color: "white"
            opacity: 0.9
            visible: busyOverlay.visible
        }
        BusyIndicator {
            width: 64
            height: 64
            anchors.centerIn: parent
            running: busyOverlay.visible
            visible: busyOverlay.visible
        }
    }

    StackView {
        id: stack
        anchors { top: parent.top; left: parent.left; right: parent.right; bottom: toolbar.top }
        onDepthChanged: {
            if (depth == 1) {
                // if we're logged in, assume we went back to lobby
                if (api.user.username != "AnonymousUser")
                    gameClient.leaveTournament();
            }
        }
    }

    ToolBar {
        id: toolbar
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right; }
        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: backButton
                text: qsTr("\uE72B")
                font.family: "Segoe MDL2 Assets"
                enabled: stack.depth > 1
                onClicked: stack.pop()
            }
            Item { Layout.fillWidth: true }
            ToolButton {
                id: logoutButton
                text: qsTr("\uE8BB")
                enabled: api.user.username != "AnonymousUser"
                visible: enabled
                font.family: "Segoe MDL2 Assets"
                onClicked: {
                    api.logout()
                    stack.replace("qrc:/Pages/LoginPage.qml")
                }
            }

            ToolButton {
                id: chatButton
                text: qsTr("\uE8F2")
                enabled: api.user.username != "AnonymousUser"
                visible: enabled
                font.family: "Segoe MDL2 Assets"
                onClicked: chatBox.visible = true
            }
        }
    }

    ChatBox {
        id: chatBox;
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right; }
    }

    Component.onCompleted: {
        stack.push("qrc:/Pages/LoginPage.qml")
        if (appSettings.authCredentialsPresent())
            busyOverlay.visible = true
    }
}
