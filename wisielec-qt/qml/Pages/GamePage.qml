import QtQuick 2.5
import QtQuick.Controls 2.0

Page {
    Connections {
        target: gameClient
        onMistakesChanged: wisielecImicz.source = "qrc:/img/wis0"+(gameClient.mistakes+1)+".png"
    }

    Image {
        anchors { top: mistakes_label.bottom; horizontalCenter: parent.horizontalCenter; bottom: keyboard.top }
        id: wisielecImicz
        source: "qrc:/img/wis01.png"
        fillMode: Image.PreserveAspectFit
    }

    Text {
        id: progress_label
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        text: gameClient.progress
        anchors {
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
        color: "#eee"
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        Text {
            anchors.centerIn: parent
            text: "Press here to enter text"
            color: "#999"
        }
        TextField {
            id: textfield
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.fill: parent
            opacity: 0
            focus: true
            //onFocusChanged: { textfield.focus = true; textfield.forceActiveFocus(); }
            onTextChanged: {
                // get letter
                var letter = textfield.text;
                // guess it
                if (letter)
                    gameClient.guess_letter(letter.toLowerCase());
                // reset
                textfield.text = "";
            }
        }
    }

    /*Rectangle {
        id: keyboard
        height: keyboardGrid.contentHeight
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        GridView {
            id: keyboardGrid
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
    }*/


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
