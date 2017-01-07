import QtQuick 2.0
import QtQuick.Controls 2.0

Page {
    Component.onCompleted: gameClient.switchChatChannel("lobby")

    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

        AboutPage { id: aboutPage }
        LobbyPage {
            new_button.onClicked: gameClient.refresh_lobby()
            newer_button.onClicked: gameClient.new_game()
        }
        RankingPage { id: rankingPage }
    }

    header: TabBar {
        id: tabBar
        currentIndex: swipeView.currentIndex
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("profil")
        }
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("trwające gry")
        }

        TabButton {
            font.family: "Segoe UI"
            text: qsTr("ranking")
        }
        onCurrentIndexChanged: {
            switch (currentIndex) {
            case 0: { aboutPage.viewingMe = true; api.getUserData(); break; };
            case 2: { api.getRanking(); break; };
            }
        }
    }

    function switchToProfile() {
        swipeView.currentIndex = 0
        aboutPage.viewingMe = false
    }
}
