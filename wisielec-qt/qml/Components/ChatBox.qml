import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Rectangle {
    id: chatBox
    color: "#d9d9d9"
    width: parent.width
    height: 300
    anchors { bottom: parent.bottom; }
    visible: false

    Rectangle {
        id: header
        color: "#E6E6E6"
        anchors { left: parent.left; right: parent.right; }
        height: headerLabel.paintedHeight + 20
        Rectangle {
            width: parent.width
            anchors.top: parent.bottom
            height: 1
            color: "#aaa"
        }

        Label {
            id: headerLabel
            anchors { margins: 10; fill: parent }
            verticalAlignment: Text.AlignVCenter
            font.weight: Font.Bold
            text: "Czat"
        }
        Label {
            anchors { right: parent.right; rightMargin: 10; verticalCenter: parent.verticalCenter }
            text: qsTr("\uE8F2")
            font.family: "Segoe MDL2 Assets"
        }
    }

    function sendChatMessage() {
        gameClient.sendChatMessage(messageInput.text)
        messageInput.text = ""
    }

    ListView {
        model: gameClient.chatMessages
        clip: true
        onModelChanged: positionViewAtEnd()
        anchors { top: header.bottom; left: parent.left; right: parent.right; bottom: chatToolbar.top; }
        delegate: ItemDelegate {
            width: parent.width
            contentItem: Column {
                anchors { margins: 5; fill: parent }
                spacing: 5
                Text {
                    anchors { left: parent.left; right: parent.right }
                    wrapMode: Text.WordWrap
                    text: modelData.username
                    font.pixelSize: 14
                    font.weight: Font.Bold
                }
                Text {
                    wrapMode: Text.WordWrap
                    anchors { left: parent.left; right: parent.right }
                    text: modelData.message
                }
            }
        }
        ScrollBar.vertical: ScrollBar { }
    }

    ToolBar {
        id: chatToolbar
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right }
        RowLayout {
            anchors.fill: parent
            TextField {
                id: messageInput
                placeholderText: "Wpisz wiadomość..."
                height: 48
                Layout.fillWidth: true
                Keys.onReturnPressed: chatBox.sendChatMessage()
            }
            ToolButton {
                text: qsTr("\uE724")
                font.family: "Segoe MDL2 Assets"
                onClicked: chatBox.sendChatMessage()
            }
            ToolButton {
                text: qsTr("\uE89B")
                font.family: "Segoe MDL2 Assets"
                onClicked: chatBox.visible = false
            }
        }
    }
}
