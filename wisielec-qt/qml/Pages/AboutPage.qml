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
        api.getUserAchievements(usernameLabel.text)
    }

    Connections {
        target: api
        onUserChanged: if (viewingMe) updateProfileInfo();
        onViewedUserChanged: if (!viewingMe) updateProfileInfo();
    }

    Rectangle {
        id: headerContainer
        height: 222
        color: "#d9d9d9"
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0
        z: -1

        Rectangle {
            id: rectangle1
            x: 270
            y: 40
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
            x: 219
            y: 160
            text: "czlowiekPlaceholder"
            font.pointSize: 16
            anchors {
                top: rectangle1.bottom
                margins: 20
                horizontalCenter: rectangle1.horizontalCenter
            }
        }
    }

    Button {
        id: button1
        x: 270
        y: 174
        visible: !viewingMe
        text: qsTr("zaproś")
        anchors.top: separator.bottom
        anchors.topMargin: 10
        anchors.right: parent.right
        anchors.rightMargin: 270
        onClicked: {
            stack.push("qrc:/Pages/TournamentInvitePage.qml", {"username": usernameLabel.text})
        }
    }


    Column {
        id: column
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 228
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0

        Rectangle {
            id: statsContainer
            height: 101
            color: "transparent"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            Layout.fillWidth: true

            Label {
                id: statsIcon
                x: 0
                y: 15
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
                x: 571
                y: 76
                text: qsTr("w rankingu")
                anchors.bottom: lostTournaments.bottom
                anchors.bottomMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 8
                horizontalAlignment: Text.AlignRight
            }

            Label {
                id: rankingPosition
                x: 563
                y: 1
                text: "-1"
                anchors.top: headerContainer.bottom
                anchors.topMargin: 6
                anchors.right: parent.right
                anchors.rightMargin: 8
                horizontalAlignment: Text.AlignRight
                font.pointSize: 50
            }

            Label {
                id: lostTournaments
                x: 162
                y: 76
                text: "0"
                anchors { top: lostTournamentsLabel.bottom; topMargin: 6; left: lostTournamentsLabel.left; leftMargin: 0 }
            }

            Label {
                id: lostTournamentsLabel
                x: 162
                y: 57
                text: qsTr("Przegrane turnieje")
                anchors { top: wonTournaments.bottom; topMargin: 10; left: wonTournamentsLabel.left; leftMargin: 0 }
                font.bold: true
            }

            Label {
                id: wonTournaments
                x: 162
                y: 34
                text: "0"
                anchors { top: wonTournamentsLabel.bottom; topMargin: 6; left: wonTournamentsLabel.left; leftMargin: 0 }
            }

            Label {
                id: wonTournamentsLabel
                x: 162
                y: 15
                text: qsTr("Wygrane turnieje")
                anchors.top: headerContainer.bottom
                anchors.topMargin: 20
                anchors.left: wonGamesLabel.right
                anchors.leftMargin: 30
                font.bold: true
            }

            Label {
                id: lostGames
                x: 61
                y: 76
                text: "0"
                anchors { top: lostGamesLabel.bottom; topMargin: 6; left: lostGamesLabel.left; leftMargin: 0 }
            }

            Label {
                id: lostGamesLabel
                x: 61
                y: 57
                text: qsTr("Przegrane gry")
                anchors.top: wonGames.bottom
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 69
                font.bold: true
            }

            Label {
                id: wonGames
                x: 61
                y: 34
                text: "0"
                anchors { left: wonGamesLabel.left; leftMargin: 0; top: wonGamesLabel.bottom; topMargin: 6 }
            }

            Label {
                id: wonGamesLabel
                x: 61
                y: 15
                text: qsTr("Wygrane gry")
                anchors.top: headerContainer.bottom
                anchors.topMargin: 20
                anchors.left: parent.left
                anchors.leftMargin: 69
                font.bold: true
            }
        }

        Rectangle {
            id: separator
            height: 2
            color: "#797979"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillWidth: true
            border.color: "#a2a2a2"
            border.width: 2
        }

        Rectangle {
            id: rectangle2
            width: 200
            height: 200
            color: "#ffffff"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            GridView {
                id: achievementView
                anchors.fill: parent
                model: viewingMe ? api.me.achievements : api.viewedUser.achievements
                delegate: Rectangle {
                    Image {
                        id: achievementIcon
                        source: "http://schopenhauer.krojony.pl/"+modelData.icon
                    }
                }
            }
        }
    }
}
