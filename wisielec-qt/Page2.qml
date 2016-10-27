import QtQuick 2.5
import QtQuick.Controls 2.0

Page {
    Connections {
        target: gameClient
        onMistakesChanged: wisielecImicz.source = "qrc:/img/wis0"+(gameClient.mistakes+1)+".png"
    }

    Image {
        anchors { top: mistakes_label.bottom; horizontalCenter: mistakes_label.verticalCenter }
        id: wisielecImicz
        source: "qrc:/img/wis01.png"
    }

    Text {
        id: progress_label
        font.family: "Segoe UI Light"
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        text: gameClient.progress
        anchors {
            horizontalCenter: parent.horizontalCenter;
            top: parent.top
            left: parent.left
            right: parent.right
            margins: 20
        }
    }

    Label {
        id: score_label
        text: gameClient.score
        anchors {
            horizontalCenter: parent.horizontalCenter;
            top: progress_label.bottom
            margins: 10
        }
    }

    Label {
        id: mistakes_label
        text: gameClient.mistakes
        anchors {
            horizontalCenter: parent.horizontalCenter;
            top: score_label.bottom
            margins: 10
        }
    }

    Rectangle {
        id: keyboard
        height: 200
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        GridView {
            anchors.fill: parent
            model: letters
            cellWidth: 40
            cellHeight: 50
            delegate: Item {
                width: 40
                height: 50
                Button {
                    text: letter
                    width: 30
                    height: 40
                    enabled: gameClient.mistakes < 5
                    onClicked: gameClient.guess_letter(letter.toLowerCase())
                    anchors { fill: parent; margins: 5 }
                }
            }
        }
    }


    ListModel {
        id: letters
        ListElement { letter: "Q" }
        ListElement { letter: "W" }
        ListElement { letter: "E" }
        ListElement { letter: "Ę" }
        ListElement { letter: "R" }
        ListElement { letter: "T" }
        ListElement { letter: "Y" }
        ListElement { letter: "U" }
        ListElement { letter: "I" }
        ListElement { letter: "O" }
        ListElement { letter: "Ó" }
        ListElement { letter: "P" }
        ListElement { letter: "A" }
        ListElement { letter: "Ą" }
        ListElement { letter: "S" }
        ListElement { letter: "Ś" }
        ListElement { letter: "D" }
        ListElement { letter: "F" }
        ListElement { letter: "G" }
        ListElement { letter: "H" }
        ListElement { letter: "J" }
        ListElement { letter: "K" }
        ListElement { letter: "L" }
        ListElement { letter: "Ł" }
        ListElement { letter: "Z" }
        ListElement { letter: "Ź" }
        ListElement { letter: "Ż" }
        ListElement { letter: "C" }
        ListElement { letter: "Ć" }
        ListElement { letter: "V" }
        ListElement { letter: "B" }
        ListElement { letter: "N" }
        ListElement { letter: "Ń" }
        ListElement { letter: "M" }
    }
}
