import QtQuick 2.0
import QtQuick.Controls 2.0

Page {
    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

        WelcomePage { id: welcomePage }
        LobbyPage {
            new_button.onClicked: gameClient.refresh_lobby()
            newer_button.onClicked: gameClient.new_game()
        }
        RankingPage { id: rankingPage }
        AboutPage { id: aboutPage }
    }

    header: TabBar {
        id: tabBar
        currentIndex: swipeView.currentIndex
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("witaj")
        }
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("gry")
        }

        TabButton {
            font.family: "Segoe UI"
            text: qsTr("ranking")
        }
        TabButton {
            font.family: "Segoe UI"
            text: qsTr("profil")
        }
        onCurrentIndexChanged: {
            switch (currentIndex) {
            case 2: { api.getRanking(); break; };
            case 3: { aboutPage.viewingMe = true; api.getUserData(); break; };
            }
        }
    }

    function switchToProfile() {
        swipeView.currentIndex = 3
        aboutPage.viewingMe = false
    }
}
