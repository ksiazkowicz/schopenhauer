import QtQuick 2.0
import QtQuick.Controls 2.0

Page {
    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

        AboutPage {
            renderlabel.text: renderer
            serverlabel.text: "127.0.0.1:8000" //gameClient.api_url
        }
        LobbyPage {
            new_button.onClicked: gameClient.refresh_lobby()
            newer_button.onClicked: gameClient.new_game()
        }
        GamePage { id: gamePage }
    }

    header: TabBar {
        id: tabBar
        currentIndex: swipeView.currentIndex
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("profile")
        }
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("lobby")
        }

        TabButton {
            font.family: "Segoe UI"
            text: qsTr("game")
        }
    }
}
