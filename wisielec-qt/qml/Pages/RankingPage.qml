import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    Connections {
        target: api
        onRankingChanged: busyOverlay.visible = false
    }

    ColumnLayout {
        id: columnLayout1
        anchors.fill: parent

        Button {
            id: refreshButton
            text: qsTr("Refresh")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: { busyOverlay.visible = true; api.getRanking() }
            width: 300
        }

        ListView {
            id: listView1
            width: parent.width
            height: parent.height - refreshButton.height
            Layout.fillWidth: true
            Layout.fillHeight: true
            delegate: ItemDelegate {
                width: parent.width
                height: row1.height+20

                onClicked: {
                    if (modelData.username != api.user.username) {
                        api.getUserData(modelData.username)
                        switchToProfile()
                    } else { swipeView.currentIndex = 3; }
                }
                Rectangle {
                    height: 1
                    color: "#aaa"
                    anchors { left: parent.left; right: parent.right }
                }
                RowLayout {
                    id: row1
                    spacing: 10
                    anchors { margins: 10; top: parent.top; left: parent.left; right: parent.right; }
                    Text {
                        text: modelData.position
                        font.pixelSize: 14
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: modelData.username
                        font.pixelSize: 14
                        font.weight: modelData.username == api.user.username ? Font.Bold : Font.Normal
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: modelData.score
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignRight
                        Layout.fillWidth: true
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }
            model: api.rankingModel
        }
    }

}
