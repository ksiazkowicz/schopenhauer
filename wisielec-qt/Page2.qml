import QtQuick 2.5
import QtQuick.Controls 2.0
import schopenhauer 1.0

Page {
    SchClient {
        id: game_client
    }

    Label {
        id: progress_label
        font.family: "Segoe UI Light"
        font.pixelSize: 20
        text: game_client.progress
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
        text: game_client.score
        anchors {
            horizontalCenter: parent.horizontalCenter;
            top: progress_label.bottom
            margins: 10
        }
    }

    Label {
        id: mistakes_label
        text: game_client.mistakes
        anchors {
            horizontalCenter: parent.horizontalCenter;
            top: score_label.bottom
            margins: 10
        }
    }

    Button {
        text: "Guess A"
        onClicked: game_client.guess_letter("a")
    }
}
