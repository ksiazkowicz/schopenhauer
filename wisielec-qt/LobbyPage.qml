import QtQuick 2.5
import QtQuick.Controls 2.0

Page {
    property alias new_button: new_button
    property alias games_list: games_list
    id: page1

    Button {
        id: new_button
        text: qsTr("Refresh")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
    }

    ListView {
        id: games_list
        model: gameClient.games
        anchors { top: new_button.bottom; topMargin: 20; left: parent.left; right: parent.right; bottom: parent.bottom; }
        delegate: Item {
            width: parent.width
            height: 48
            anchors { left: parent.left; leftMargin: 20; right: parent.right; rightMargin: 20 }
            Text {
                id: line1
                text: modelData
                anchors { top: parent.top; topMargin: 15 }
                font.bold: true
                font.pointSize: 12
            }
            Text {
                id: line2
                anchors { top: line1.bottom; topMargin: 5 }
                text: "grają: <b>chlebzycia666</b>, <b>bezsensistnienia12</b>"
            }
            MouseArea {
                anchors.fill: parent
                onClicked:  {
                    gameClient.join_game(modelData)
                    swipeView.currentIndex = 2
                }
            }
        }
    }
}
