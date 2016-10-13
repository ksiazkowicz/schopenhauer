import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    visible: true
    width: 400
    height: 480
    title: qsTr("wisielec schopenhauera")

    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

        Page1 {}
        LobbyPage {
            join_button.onClicked: {
                gamePage.client.join_game(session_field.text)
                swipeView.currentIndex = 2
            }
        }
        Page2 { id: gamePage }
        Page {}
    }

    header: TabBar {
        id: tabBar
        currentIndex: swipeView.currentIndex
        TabButton {
            //font.family: "Segoe MDL2 Assets"
            font.family: "Segoe UI Light"
            //text: qsTr("\uE716")
            text: qsTr("profile")
        }
        TabButton {
            font.family: "Segoe UI Light"
            text: qsTr("lobby")
        }

        TabButton {
            //font.family: "Segoe MDL2 Assets"
            //text: qsTr("\uE768")
            font.family: "Segoe UI Light"
            text: qsTr("game")
        }
        TabButton {
            font.family: "Segoe UI Light"
            text: qsTr("settings")
        }
    }
}
