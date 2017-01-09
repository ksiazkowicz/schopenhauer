import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Page {
    id: welcomePage
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
                id: tournamentHeader
                height: 42
                anchors { right: parent.right; left: parent.left; margins: 10 }

                Label {
                    id: tournamentHeaderLabel
                    text: qsTr("Trwające turnieje")
                    Layout.fillWidth: true
                    font.bold: true
                    font.pointSize: 11
                }

                Button {
                    text: qsTr("Utwórz!")
                    onClicked: stack.push("qrc:/Pages/NewTournamentPage.qml")
                }

                Label {
                    id: tournamentHeaderIcon
                    text: qsTr("\uE7FC")
                    font.family: "Segoe MDL2 Assets"
                    font.pixelSize: 24
                }
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
                }
                model: gameClient.tournaments
            }
            Rectangle {
                height: 1
                color: "#8f8f8f"
                anchors { right: parent.right; left: parent.left; }
            }
            RowLayout {
                id: antisocialHeader
                height: 42
                anchors { right: parent.right; left: parent.left; margins: 10 }

                Label {
                    id: antisocialHeaderLabel
                    text: qsTr("Nie masz znajomych?")
                    Layout.fillWidth: true
                    font.bold: true
                    font.pointSize: 11
                }

                Button {
                    id: antisocialButton
                    text: qsTr("Zagraj samemu!")
                    onClicked: stack.push("qrc:/Pages/NewGamePage.qml")
                }
            }
        }
    }
}
