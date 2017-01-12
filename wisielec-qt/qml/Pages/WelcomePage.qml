import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import "../Components"

Page {
    id: welcomePage

    Connections {
        target: gameClient
        onTournamentInfoFound: {
            if (busyOverlay.visible)
                stack.push("qrc:/Pages/TournamentPage.qml")
            busyOverlay.visible = false;
        }
    }

    Label {
        id: label1
        text: qsTr("Witaj")
        font.pointSize: 34
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.leftMargin: 20
    }

    Label {
        id: label2
        text: api.user.username
        color: "#666"
        font.pointSize: 18
        anchors.top: label1.bottom
        anchors.topMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 20
    }

    Flickable {
        clip: true
        anchors {
            top: label2.bottom
            topMargin: 20;
            bottom: parent.bottom
            bottomMargin: 0
            right: parent.right
            left: parent.left
        }

        contentHeight: column1.implicitHeight
        Column {
            id: column1
            anchors.fill: parent
            BlockHeader {
                icon: qsTr("\uE7FC")
                title: qsTr("Turnieje w których uczestniczysz")
                button.text: qsTr("Utwórz!")
                button.onClicked: stack.push("qrc:/Pages/NewTournamentPage.qml")
                hasButton: true
            }
            ListView {
                id: tournamentList
                anchors { left: parent.left; right: parent.right }
                height: contentHeight
                interactive: false
                delegate: ItemDelegate {
                    width: parent.width
                    height: modelData.inProgress ? 20 + tournamentDelegateHeader.height : 0
                    clip: true
                    Rectangle {
                        height: 1
                        color: "#aaa"
                        anchors { left: parent.left; right: parent.right }
                    }
                    Column {
                        id: tournamentDelegateHeader
                        anchors { left: parent.left; right: parent.right; margins: 10; top: parent.top }
                        height: tournamentNameLabel.paintedHeight + tournamentModesLabel.paintedHeight
                        Label {
                            id: tournamentNameLabel
                            text: modelData.name
                            font.pixelSize: 16
                        }
                        Label {
                            id: tournamentModesLabel
                            text: "("+ modelData.modes+")"
                            font.pixelSize: 16
                            color: "#555"
                        }
                    }
                    onClicked: {
                        busyOverlay.visible = true;
                        gameClient.joinTournament(modelData.sessionId)
                    }
                }
                model: gameClient.tournaments
            }
            Label {
                anchors { horizontalCenter: parent.horizontalCenter }
                color: "#666"
                verticalAlignment: Text.AlignVCenter
                height: tournamentList.count == 0 ? paintedHeight + 40 : 0
                clip: true
                text: "Nie uczestniczysz w żadnych turniejach"
            }


            BlockHeader {
                icon: qsTr("\uE716")
                title: qsTr("Grają teraz")
                hasButton: false
            }
            Rectangle {
                id: lobbyContainer
                anchors { left: parent.left; right: parent.right; }
                height: playersRow.implicitHeight + 40
                Rectangle {
                    height: 1
                    color: "#aaa"
                    anchors { left: parent.left; right: parent.right }
                }
                Row {
                    id: playersRow
                    spacing: 10;
                    anchors { left: parent.left; right: parent.right; margins: 10; topMargin: 20; top: parent.top }
                    Repeater {
                        id: playersList
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
                Label {
                    anchors { horizontalCenter: parent.horizontalCenter }
                    color: "#666"
                    verticalAlignment: Text.AlignVCenter
                    height: playersList.count == 0 ? paintedHeight : 0
                    clip: true
                    text: "Nie ma żadnych graczy"
                }
            }
            BlockHeader {
                title: qsTr("Nie masz znajomych?")
                hasButton: true
                button.text: qsTr("Zagraj samemu!")
                button.onClicked: stack.push("qrc:/Pages/NewGamePage.qml")
            }
            BlockHeader {
                title: qsTr("Wróć do tych gier")
                hasButton: false
            }
            Label {
                anchors { horizontalCenter: parent.horizontalCenter }
                color: "#666"
                verticalAlignment: Text.AlignVCenter
                height: gamesList.count == 0 ? paintedHeight + 40 : 0
                clip: true
                text: "Nie masz żadnych gier"
            }

            ListView {
                id: gamesList
                interactive: false
                model: gameClient.games
                height: contentHeight
                anchors { left: parent.left; right: parent.right; }
                delegate: ItemDelegate {
                    width: parent.width
                    height: 64
                    anchors { left: parent.left; right: parent.right; }
                    Rectangle {
                        height: 1
                        color: "#aaa"
                        anchors { left: parent.left; right: parent.right }
                    }
                    onClicked: {
                        stack.push("qrc:/Pages/GamePage.qml")
                        gameClient.join_game(modelData.sessionId)
                    }
                    Label {
                        text: modelData.progress
                        anchors { fill: parent; margins: 15; }
                        wrapMode: Text.WordWrap
                        font.pointSize: 12
                    }
                }
            }
        }
    }
}
