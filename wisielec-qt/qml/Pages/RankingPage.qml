import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    ColumnLayout {
        id: columnLayout1
        anchors.fill: parent

        Button {
            id: refreshButton
            text: qsTr("Refresh")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: api.getRanking()
            width: 300
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
                height: 21
                RowLayout {
                    id: row1
                    spacing: 10
                    width: parent.width-10
                    Text {
                        text: modelData.position
                        font.pixelSize: 14
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        text: modelData.username
                        font.pixelSize: 14
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
