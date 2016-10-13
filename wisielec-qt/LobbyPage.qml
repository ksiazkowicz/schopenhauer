import QtQuick 2.5
import QtQuick.Controls 2.0

Page {
    property alias join_button: join_button
    property alias session_field: session_field
    id: page1
    Button {
        id: join_button
        text: qsTr("Join")
        anchors.horizontalCenter: session_field.horizontalCenter
        anchors.top: session_field.bottom
        anchors.topMargin: 11
    }

    TextField {
        id: session_field
        width: 200
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: session_label.bottom
        anchors.topMargin: 6
        text: "13d77980919211e6af5d5cc5d4c8de39"
    }

    Label {
        id: session_label
        text: qsTr("Session ID")
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.leftMargin: 0
        anchors.left: session_field.left
    }
}
