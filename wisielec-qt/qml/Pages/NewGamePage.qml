import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Page {
    id: newGamePage
    property string modifiers: ""

    ListModel {
        id: modifierModel
        ListElement {
            icon: "qrc:/img/modes/eutanazol.png"
            name: "Eutanazol"
            description: "Klasyczna gra w wisielca."
            code: "no_modifiers"
        }
        ListElement {
            icon: "qrc:/img/modes/born_to_die.png"
            name: "Born To Die"
            description: "Spróbuj poznać słodki smak porażki."
            code: "inverse_death"
        }
        ListElement {
            icon: "qrc:/img/modes/yolo.jpg"
            name: "Masz tylko jedno życie"
            description: "I dobrze."
            code: "only_one_mistake"
        }
    }


    Column {
        anchors { fill: parent; margins: 6 }
        spacing: 5
        Label {
            font.pixelSize: 28
            text: "tworzenie gry"
            horizontalAlignment: Text.AlignHCenter
            anchors { left: parent.left; right: parent.right }
            height: 80
            verticalAlignment: Text.AlignVCenter
        }
        Rectangle {
            width: parent.width
            height: 20
        }

        Label {
            font.pixelSize: 20
            text: "modyfikatory"
            horizontalAlignment: Text.AlignHCenter
            anchors { left: parent.left; right: parent.right }
        }

        GridView {
            id: achievementView
            anchors { left: parent.left; right: parent.right; }
            model: modifierModel
            interactive: false
            height: contentHeight

            cellWidth: parent.width / 3
            cellHeight: 160

            delegate: ItemDelegate {
                width: parent.width / 3
                height: 160
                clip: true

                Connections {
                    target: newGamePage
                    onModifiersChanged: {
                        if (modifiers.match(code) || (code == "no_modifiers" && modifiers == ""))
                            backgroundRectangle.color = "#d9d9d9";
                        else backgroundRectangle.color = "white";
                    }
                }

                background: Rectangle {
                    id: backgroundRectangle
                    color: code == "no_modifiers" ? "#d9d9d9" : "white";
                    anchors { fill: parent; margins: 2; }
                    radius: 5
                }

                onClicked: {
                    if (code == "no_modifiers") {
                        modifiers = "";
                        modifiersChanged();
                    } else {
                        if (!modifiers.match(code)) {
                            if (!modifiers == "")
                                modifiers += ";"
                            modifiers += code;
                            modifiersChanged();
                        }
                    }
                }

                Column {
                    spacing: 5
                    anchors { fill: parent; topMargin: 10; }

                    Image {
                        source: icon
                        sourceSize { width: 100; height: 100 }
                        width: 100
                        height: 100
                        anchors { horizontalCenter: parent.horizontalCenter; }
                    }
                    Label {
                        font.bold: true;
                        text: name;
                        wrapMode: Text.WordWrap;
                        font.pixelSize: 13
                        horizontalAlignment: Text.AlignHCenter
                        anchors { left: parent.left; right: parent.right; }
                    }
                    Label {
                        text: description;
                        wrapMode: Text.WordWrap;
                        font.pixelSize: 11
                        horizontalAlignment: Text.AlignHCenter
                        anchors { left: parent.left; right: parent.right; }
                    }
                }
            }
        }

        Rectangle {
            width: parent.width
            height: 60
        }
        Button {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Zaczynamy"
            font.pixelSize: 28
            onClicked: {
                busyOverlay.visible = true
                api.createGame(modifiers)
            }
        }

        Connections {
            target: api
            onGameCreated: {
                busyOverlay.visible = false;
                stack.replace("qrc:/Pages/GamePage.qml")
                gameClient.join_game(sessionId)
            }
        }
    }
}
