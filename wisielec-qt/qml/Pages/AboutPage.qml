import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Page {
    id: aboutPage
    property bool viewingMe: true

    function updateProfileInfo() {
        avatarImg.source = viewingMe ? api.user.avatar : api.viewedUser.avatar
        usernameLabel.text = viewingMe ? api.user.username : api.viewedUser.username
        wonGames.text = viewingMe ? api.user.wonGames : api.viewedUser.wonGames
        lostGames.text = viewingMe ? api.user.lostGames : api.viewedUser.lostGames
        wonTournaments.text = viewingMe ? api.user.wonTournaments : api.viewedUser.wonTournaments
        lostGames.text = viewingMe ? api.user.lostTournaments : api.viewedUser.lostTournaments
        rankingPosition.text = viewingMe ? api.user.position : api.viewedUser.position
        achievementView.model = viewingMe ? api.user.achievements : api.viewedUser.achievements
        achievementsProgress.text = viewingMe ? "(" + api.user.progress + "%)" : "(" + api.viewedUser.progress + "%)"
        api.getUserAchievements(usernameLabel.text)
    }

    Connections {
        target: api
        onUserChanged: if (viewingMe) updateProfileInfo();
        onViewedUserChanged: if (!viewingMe) updateProfileInfo();
    }

    Rectangle {
        id: headerContainer
        height: viewingMe ? 230 : 260
        color: "#d9d9d9"
        anchors {
            right: parent.right;
            left: parent.left;
            top: parent.top
        }
        z: -1

        Rectangle {
            id: rectangle1
            width: 100
            height: 100
            color: "#000"
            radius: 100
            clip: true
            Image {
                id: avatarImg
                anchors.fill: parent
                width: 100
                height: 100
                z: 0
                clip: true
                source: "qrc:/img/avatar.jpg"
            }

            anchors {
                top: parent.top
                margins: 40
                horizontalCenter: parent.horizontalCenter
            }
        }

        Label {
            id: usernameLabel
            text: "czlowiekPlaceholder"
            font.pointSize: 16
            anchors {
                top: rectangle1.bottom
                margins: 20
                horizontalCenter: rectangle1.horizontalCenter
            }
        }
        Button {
            id: inviteButton
            visible: !viewingMe
            text: qsTr("zaproś")
            anchors { top: usernameLabel.bottom; topMargin: 20; horizontalCenter: parent.horizontalCenter }
            onClicked: stack.push("qrc:/Pages/TournamentInvitePage.qml", {"username": usernameLabel.text})
        }
    }

    Flickable {
        anchors {
            bottom: parent.bottom;
            top: headerContainer.bottom;
            left: parent.left;
            right: parent.right;
        }
        ScrollBar.vertical: ScrollBar {}
        contentHeight: statsContainer.height + 2 + achievementBlock.height + 2
        z: -2

        Column {
            id: column
            anchors.fill: parent

            Rectangle {
                id: statsContainer
                height: 141
                color: "transparent"
                anchors {
                    right: parent.right;
                    left: parent.left;
                }
                Layout.fillWidth: true

                Label {
                    id: statsIcon
                    text: "\uE7C1"
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.top: wonGamesLabel.top
                    anchors.topMargin: 0
                    font.pointSize: 30
                    font.family: "Segoe MDL2 Assets"
                }

                Label {
                    id: rankingPositionLabel
                    text: qsTr("w rankingu")
                    anchors.bottom: lostTournaments.bottom
                    anchors.bottomMargin: 0
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    horizontalAlignment: Text.AlignRight
                }

                Label {
                    id: rankingPosition
                    text: "-1"
                    anchors.top: parent.top
                    anchors.topMargin: 6
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    horizontalAlignment: Text.AlignRight
                    font.pointSize: 50
                }

                Label {
                    id: lostTournaments
                    text: "0"
                    anchors { top: lostTournamentsLabel.bottom; topMargin: 6; left: lostTournamentsLabel.left; leftMargin: 0 }
                }

                Label {
                    id: lostTournamentsLabel
                    text: qsTr("Przegrane turnieje")
                    anchors { top: wonTournaments.bottom; topMargin: 10; left: wonTournamentsLabel.left; leftMargin: 0 }
                    font.bold: true
                }

                Label {
                    id: wonTournaments
                    text: "0"
                    anchors { top: wonTournamentsLabel.bottom; topMargin: 6; left: wonTournamentsLabel.left; leftMargin: 0 }
                }

                Label {
                    id: wonTournamentsLabel
                    text: qsTr("Wygrane turnieje")
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.left: wonGamesLabel.right
                    anchors.leftMargin: 30
                    font.bold: true
                }

                Label {
                    id: lostGames
                    text: "0"
                    anchors { top: lostGamesLabel.bottom; topMargin: 6; left: lostGamesLabel.left; leftMargin: 0 }
                }

                Label {
                    id: lostGamesLabel
                    text: qsTr("Przegrane gry")
                    anchors.top: wonGames.bottom
                    anchors.topMargin: 10
                    anchors.left: parent.left
                    anchors.leftMargin: 69
                    font.bold: true
                }

                Label {
                    id: wonGames
                    text: "0"
                    anchors { left: wonGamesLabel.left; leftMargin: 0; top: wonGamesLabel.bottom; topMargin: 6 }
                }

                Label {
                    id: wonGamesLabel
                    text: qsTr("Wygrane gry")
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.left: parent.left
                    anchors.leftMargin: 69
                    font.bold: true
                }
            }

            Rectangle {
                height: 2
                color: "#797979"
                anchors { left: parent.left; right: parent.right }
                border { color: "#a2a2a2"; width: 2 }
            }

            Rectangle {
                id: achievementBlock
                height: achievementView.contentHeight + 40
                color: "#ffffff"
                anchors { left: parent.left; right: parent.right }
                Label {
                    id: achievementsLabel
                    text: "Osiągnięcia"
                    anchors { left: parent.left; margins: 6; top: parent.top; }
                    height: 30
                    verticalAlignment: Text.AlignVCenter
                    font.bold: true
                }

                Label {
                    id: achievementsProgress
                    text: "(-2%)"
                    anchors { right: parent.right; margins: 6; top: parent.top; }
                    height: 30
                    verticalAlignment: Text.AlignVCenter
                    font.bold: true
                }

                GridView {
                    id: achievementView
                    anchors { top: achievementsLabel.bottom; margins: 6; left: parent.left; right: parent.right; bottom: parent.bottom }
                    model: viewingMe ? api.user.achievements : api.viewedUser.achievements
                    interactive: false

                    cellWidth: parent.width / 3
                    cellHeight: 160

                    delegate: ItemDelegate {
                        width: parent.width / 3
                        height: 160
                        clip: true
                        Column {
                            id: achievementColumn
                            spacing: 5
                            anchors { fill: parent; }
                            Image {
                                id: achievementIcon
                                source: "http://schopenhauer.krojony.pl/"+modelData.icon
                                anchors { horizontalCenter: parent.horizontalCenter; }
                            }
                            Label {
                                id: achievementName
                                font.bold: true;
                                text: modelData.name;
                                wrapMode: Text.WordWrap;
                                font.pixelSize: 13
                                horizontalAlignment: Text.AlignHCenter
                                anchors { left: parent.left; right: parent.right; }
                            }
                            Label {
                                id: achievementDescription
                                text: modelData.description;
                                wrapMode: Text.WordWrap;
                                font.pixelSize: 11
                                horizontalAlignment: Text.AlignHCenter
                                anchors { left: parent.left; right: parent.right; }
                            }
                        }
                    }
                }
            }

            Rectangle {
                height: 2
                color: "#797979"
                anchors { left: parent.left; right: parent.right }
                border { color: "#a2a2a2"; width: 2 }
            }
        }
    }
}
