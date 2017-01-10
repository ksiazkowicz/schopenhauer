import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Rectangle {
    property string title: ""
    property string icon: ""
    property bool hasButton: false
    property alias button: headerButton

    height: 52
    anchors { right: parent.right; left: parent.left;  }
    Rectangle {
        height: 1
        color: "#8f8f8f"
        anchors { right: parent.right; left: parent.left; }
    }
    RowLayout {
        anchors { fill: parent; margins: 10 }

        Label {
            text: title
            Layout.fillWidth: true
            font.bold: true
            font.pointSize: 11
        }
        Button {
            id: headerButton
            visible: hasButton
        }
        Label {
            text: icon
            font.family: "Segoe MDL2 Assets"
            font.pixelSize: 24
        }
    }
}
