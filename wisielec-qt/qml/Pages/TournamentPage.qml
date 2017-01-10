import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Page {
    id: tournamentPage

    Connections {
        target: gameClient
        onTournamentInfoFound: {
            label1.text = gameClient.currentTournament.name;
            label2.text = gameClient.currentTournament.modes;
            playersList.model = gameClient.currentTournament.playerList;
        }
        onGameFound: {
            busyOverlay.visible = false
            stack.push("qrc:/Pages/GamePage.qml")
            gameClient.join_game(sessionId)
        }
    }

    Label {
        id: label1
        text: gameClient.currentTournamentName()
        font.pointSize: 34
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.leftMargin: 20
    }

    Label {
        id: label2
        text: gameClient.currentTournamentModes()
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
            bottomMargin: 20
            right: parent.right
            left: parent.left
        }

        contentHeight: column1.height
        Column {
            id: column1
            anchors.fill: parent

            Rectangle {
                height: 1
                color: "#8f8f8f"
                anchors { right: parent.right; left: parent.left; }
            }

            RowLayout {
                id: tournamentManagementHeader
                height: 42
                anchors { right: parent.right; left: parent.left; margins: 10 }

                Label {
                    text: qsTr("Zarządzaj")
                    Layout.fillWidth: true
                    font.bold: true
                    font.pointSize: 11
                }

                Button {
                    text: qsTr("Utwórz rundę")
                    onClicked: {
                        busyOverlay.visible = true;
                        api.newRoundTournament(gameClient.tournamentId)
                    }
                }
                Button {
                    text: qsTr("Zakończ")
                    onClicked: console.log("Nie zaimplementowane")
                }

                Label {
                    text: qsTr("\uE912")
                    font.family: "Segoe MDL2 Assets"
                    font.pixelSize: 24
                }
            }

            Rectangle {
                height: 1
                color: "#8f8f8f"
                anchors { right: parent.right; left: parent.left; }
            }

            RowLayout {
                id: tournamentHeader
                height: 42
                anchors { right: parent.right; left: parent.left; margins: 10 }

                Label {
                    text: qsTr("Gracze")
                    Layout.fillWidth: true
                    font.bold: true
                    font.pointSize: 11
                }

                Button {
                    text: qsTr("Zaproś")
                    onClicked: stack.push("qrc:/Pages/TournamentInvitePage.qml")
                }

                Label {
                    text: qsTr("\uE716")
                    font.family: "Segoe MDL2 Assets"
                    font.pixelSize: 24
                }
            }
            ListView {
                id: playersList
                anchors { left: parent.left; right: parent.right }
                height: contentHeight
                interactive: false
                delegate: ItemDelegate {
                    width: parent.width
                    height:20 + playerDelegateHeader.height
                    clip: true
                    Rectangle {
                        height: 1
                        color: "#aaa"
                        anchors { left: parent.left; right: parent.right }
                    }
                    Column {
                        id: playerDelegateHeader
                        anchors { left: parent.left; right: parent.right; margins: 10; top: parent.top }
                        height: playerLabel.paintedHeight + player2Label.paintedHeight
                        Label {
                            id: playerLabel
                            text: modelData
                            font.pixelSize: 16
                        }
                        Label {
                            id: player2Label
                            text: "Wygrywa życie" //todo pobieraj statystyki
                            font.pixelSize: 16
                            color: "#555"
                        }
                    }
                }
                model: gameClient.currentTournament.playerList
            }
            Rectangle {
                height: 1
                color: "#8f8f8f"
                anchors { right: parent.right; left: parent.left; }
            }
        }
    }
}
