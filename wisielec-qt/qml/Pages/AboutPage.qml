import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Item {
    id: item1

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
                anchors.fill: parent
                width: 100
                height: 100
                clip: true
                source: api.user.avatar
            }

            anchors {
                top: parent.top
                margins: 40
                horizontalCenter: parent.horizontalCenter
            }
        }

        Label {
            x: 219
            y: 160
            text: api.user.username
            z: 1
            font.pointSize: 16
            anchors {
                top: rectangle1.bottom
                margins: 20
                horizontalCenter: rectangle1.horizontalCenter
            }
        }
    }

    Label {
        id: wonGamesLabel
        y: 234
        text: qsTr("Wygrane gry")
        anchors.left: parent.left
        anchors.leftMargin: 8
        font.bold: true
    }

    Label {
        id: wonGames
        text: api.user.wonGames
        anchors.left: wonGamesLabel.left
        anchors.leftMargin: 0
        anchors.top: wonGamesLabel.bottom
        anchors.topMargin: 6
    }

    Label {
        id: lostGamesLabel
        x: -4
        text: qsTr("Przegrane gry")
        anchors.top: wonGames.bottom
        anchors.topMargin: 6
        anchors.left: parent.left
        anchors.leftMargin: 8
        font.bold: true
    }

    Label {
        id: lostGames
        text: api.user.lostGames
        anchors.top: lostGamesLabel.bottom
        anchors.topMargin: 6
        anchors.left: lostGamesLabel.left
        anchors.leftMargin: 0
    }

    Label {
        id: wonTournamentsLabel
        x: -5
        y: 234
        text: qsTr("Wygrane turnieje")
        anchors.left: wonGamesLabel.right
        anchors.leftMargin: 14
        font.bold: true
    }

    Label {
        id: wonTournaments
        text: api.user.wonTournaments
        anchors.top: wonTournamentsLabel.bottom
        anchors.topMargin: 6
        anchors.left: wonTournamentsLabel.left
        anchors.leftMargin: 0
    }

    Label {
        id: lostTournamentsLabel
        x: -9
        text: qsTr("Przegrane turnieje")
        anchors.top: wonTournaments.bottom
        anchors.topMargin: 6
        anchors.left: lostGamesLabel.right
        anchors.leftMargin: 6
        font.bold: true
    }

    Label {
        id: lostTournaments
        text: api.user.lostTournaments
        anchors.top: lostTournamentsLabel.bottom
        anchors.topMargin: 6
        anchors.left: lostTournamentsLabel.left
        anchors.leftMargin: 0
    }

    Label {
        id: label5
        x: 509
        y: 228
        text: api.user.position
        anchors.right: parent.right
        anchors.rightMargin: 8
        horizontalAlignment: Text.AlignRight
        font.pointSize: 40
    }

    Label {
        id: label6
        x: 579
        y: 298
        text: qsTr("w rankingu")
        anchors.right: parent.right
        anchors.rightMargin: 8
        horizontalAlignment: Text.AlignRight
    }
}
