import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    visible: true
    width: 400
    height: 480
    title: qsTr("Hello World")

    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

        Page1 {}
        Page2 {}
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
