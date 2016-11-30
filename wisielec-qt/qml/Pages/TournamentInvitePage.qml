import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    property string username: "czlowiekPlaceholder"

    ColumnLayout {
        id: columnLayout1
        anchors.fill: parent


        Rectangle {
            id: rectangle1
            width: 200
            height: 100
            color: "#d9d9d9"
            Layout.maximumHeight: 80
            Layout.fillWidth: true

            Label {
                id: label1
                x: 312
                y: 14
                text: qsTr("Zaproś gracza do turnieju")
                anchors.horizontalCenterOffset: 0
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 10
                horizontalAlignment: Text.AlignHCenter
            }

            Label {
                id: usernameLabel
                x: 311
                y: 36
                text: username
                anchors.horizontalCenterOffset: 0
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                font.pointSize: 20
            }
        }
        ListView {
            id: listView1
            width: 300
            height: 400
            Layout.fillWidth: true
            Layout.fillHeight: true
            delegate: Item {
                x: 5
                width: parent.width
                height: 70
                RowLayout {
                    id: row1
                    spacing: 10
                    width: parent.width-10
                    Text {
                        text: modelData.name
                        font.pixelSize: 14
                        font.bold: true
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: "("+ modelData.sessionId+")"
                        font.pixelSize: 14
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                Row {
                    id: playersRow
                    anchors { topMargin: 10; top: row1.bottom; }
                    spacing: 10;
                    Repeater {
                        model: modelData.playerList
                        Button {
                            text: modelData;
                            onClicked: {
                                api.getUserData(modelData)
                                switchToProfile()
                            }
                        }
                    }
                    Button {
                        text: "Zaproś"
                        onClicked: api.invitePlayerToTournament(modelData.sessionId, username)
                    }
                }
            }
            model: gameClient.tournaments
        }
    }

    footer: ToolBar {
        RowLayout {
            anchors.fill: parent;
            ToolButton {
                text: "\uE72B"
                font.family: "Segoe MDL2 Assets"
                onClicked: stack.pop()
            }
        }
    }
}
