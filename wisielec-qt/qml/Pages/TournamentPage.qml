import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import "../Components"

Page {
    id: tournamentPage

    Connections {
        target: api
        onTournamentEnded: {
            finalHeader.visible = true
            if (winner) {
                finalHeader.title = "Turniej wygrał " + winner + " po " + roundCount + " rundach"
            } else {
                finalHeader.title = "Turniej zakończył się po " + roundCount + " rundach. Nikt nie wygrał."
            }
            tournamentManagementHeader.visible = false
            tournamentManagementSeparator.visible = false
        }
    }

    Component.onCompleted: {
        // refresh data
        if (gameClient.currentTournament)
            gameClient.joinTournament(gameClient.currentTournament.sessionId)
    }

    Connections {
        target: gameClient
        onTournamentInfoFound: {
            label1.text = gameClient.currentTournament.name;
            label2.text = gameClient.currentTournament.modes;
            playersList.model = gameClient.currentTournament.scoreboard;
            roundList.model = gameClient.currentTournament.rounds;
            finalHeader.visible = !gameClient.currentTournament.inProgress
            finalHeader.title = "Turniej wygrał " + gameClient.currentTournament.winner
            tournamentManagementHeader.visible = !finalHeader.visible
            tournamentManagementSeparator.visible = !finalHeader.visible
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
            right: parent.right
            left: parent.left
        }

        contentHeight: column1.implicitHeight
        Column {
            id: column1
            anchors.fill: parent

            Rectangle {
                id: tournamentManagementSeparator
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
                    onClicked: api.endTournament(gameClient.tournamentId)
                }

                Label {
                    text: qsTr("\uE912")
                    font.family: "Segoe MDL2 Assets"
                    font.pixelSize: 24
                }
            }

            BlockHeader {
                id: finalHeader
                visible: gameClient.currentTournament ? !gameClient.currentTournament.inProgress : false
                title: gameClient.currentTournament ? "Turniej wygrał " + gameClient.currentTournament.winner : ""
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
                    height: 20 + scoreColumn.implicitHeight
                    clip: true
                    Rectangle {
                        height: 1
                        color: "#aaa"
                        anchors { left: parent.left; right: parent.right }
                    }
                    Column {
                        anchors { left: parent.left; right: parent.right; margins: 10; top: parent.top }
                        Label {
                            id: playerLabel
                            text: modelData.username
                            font.pixelSize: 16
                        }
                        Label {
                            id: player2Label
                            text: modelData.winner ? "Wygrywa życie" : ""
                            font.pixelSize: 16
                            color: "#555"
                        }
                    }
                    Column {
                        id: scoreColumn
                        anchors { right: parent.right; margins: 5; top: parent.top }
                        Label {
                            font.pixelSize: 24
                            anchors.right: parent.right
                            horizontalAlignment: Text.AlignRight
                            text: modelData.score
                        }
                        Label {
                            text: "wygranych"
                            anchors.right: parent.right
                            horizontalAlignment: Text.AlignRight
                            font.pixelSize: 12
                        }
                    }
                }
                model: gameClient.currentTournament ? gameClient.currentTournament.scoreboard : null
            }

            BlockHeader {
                title: "Rundy"
            }
            ListView {
                id: roundList
                anchors { left: parent.left; right: parent.right }
                height: contentHeight
                interactive: false
                delegate: ItemDelegate {
                    width: parent.width
                    height: 20 + roundRow.implicitHeight
                    clip: true
                    Rectangle {
                        height: 1
                        color: "#aaa"
                        anchors { left: parent.left; right: parent.right }
                    }
                    Row {
                        id: roundRow
                        anchors { left: parent.left; right: parent.right; margins: 10; top: parent.top }
                        Label {
                            text: modelData.roundId
                            horizontalAlignment: Text.AlignLeft
                            anchors { verticalCenter: parent.verticalCenter }
                            font.pixelSize: 16
                            width: 60
                        }
                        Label {
                            text: modelData.inProgress() ? "W trakcie" : "Zakończona"
                            horizontalAlignment: Text.AlignHCenter
                            anchors { verticalCenter: parent.verticalCenter }
                            width: 100
                        }
                        Label {
                            text: modelData.winner ? modelData.winner : "nikt nie wygrał"
                            color: "#555"
                            horizontalAlignment: Text.AlignHCenter
                            anchors { verticalCenter: parent.verticalCenter }
                            width: parent.width - 160 - playButton.width
                            font.bold: modelData.winner == api.user.username
                        }
                        Button {
                            id: playButton
                            text: "Zagraj"
                            enabled: modelData.inProgress()
                            onClicked: {
                                var game_sessionId = modelData.getGameForPlayer(api.user.username);
                                if (game_sessionId) {
                                    stack.push("qrc:/Pages/GamePage.qml")
                                    gameClient.join_game(game_sessionId);
                                }
                            }
                        }
                    }
                }
                model: gameClient.currentTournament ? gameClient.currentTournament.rounds : null
            }
        }
    }
}
