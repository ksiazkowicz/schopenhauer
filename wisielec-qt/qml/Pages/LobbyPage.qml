import QtQuick 2.5
import QtQuick.Controls 2.0

Page {
    property alias new_button: new_button
    property alias newer_button: newer_button
    property alias games_list: games_list
    id: page1

    Button {
        id: new_button
        text: qsTr("Refresh")
        anchors.horizontalCenterOffset: -60
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
    }

    ListView {
        id: games_list
        model: gameClient.games
        anchors { top: new_button.bottom; topMargin: 20; left: parent.left; right: parent.right; bottom: lobbyContainer.top; }
        delegate: Item {
            width: parent.width
            height: 64
            anchors { left: parent.left; leftMargin: 20; right: parent.right; rightMargin: 20 }
            Text {
                id: line1
                text: modelData.sessionId
                anchors { top: parent.top; topMargin: 15 }
                font.bold: true
                font.pointSize: 12
            }
            Row {
                id: line2
                spacing: 10;
                anchors { top: line1.bottom; topMargin: 5 }
                Repeater {
                    model: modelData.playerList;
                    Button {
                        text: modelData;
                        onClicked: {
                            api.getUserData(modelData)
                            switchToProfile()
                        }
                    }
                }
                Button {
                    text: "Dołącz";
                    onClicked: {
                        stack.push("qrc:/Pages/GamePage.qml")
                        gameClient.join_game(modelData.sessionId)
                    }
                }
            }
        }
    }

    Rectangle {
        id: lobbyContainer
        anchors { bottom: parent.bottom; left: parent.left; right: parent.right; }
        height: playersRow.implicitHeight + 70
        color: "#d9d9d9"
        Label {
            id: lobbyLabel
            text: "Gracze w lobby"
            anchors { top: parent.top; left: parent.left; margins: 20; }
        }
        Row {
            id: playersRow
            anchors.topMargin: 10
            spacing: 10;
            anchors { left: parent.left; right: parent.right; top: lobbyLabel.bottom; bottom: parent.bottom; margins: 20; }
            Repeater {
                model: gameClient.lobbyPlayers
                Button {
                    text: modelData;
                    onClicked: {
                        api.getUserData(modelData)
                        switchToProfile()
                    }
                }
            }
        }
    }

    Button {
        id: newer_button
        y: 20
        text: qsTr("New")
        anchors.left: new_button.right
        anchors.leftMargin: 17
        onClicked: stack.push("qrc:/Pages/NewGamePage.qml")
    }
}
