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

    Column {
        id: column1
        anchors.top: label2.bottom
        anchors.topMargin: 5
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        anchors.right: parent.right
        anchors.rightMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 20

        Rectangle {
            id: separator1
            height: 1
            color: "#8f8f8f"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
        }

        RowLayout {
            id: tournamentHeader
            height: 42
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0

            Label {
                id: tournamentHeaderLabel
                text: qsTr("Trwające turnieje")
                Layout.fillWidth: true
                font.bold: true
                font.pointSize: 11
            }

            Label {
                id: tournamentHeaderIcon
                text: qsTr("\uE7FC")
                font.family: "Segoe MDL2 Assets"
                font.pixelSize: 24
            }
        }
        Label {
            text: "nie no"
        }
    }

}
