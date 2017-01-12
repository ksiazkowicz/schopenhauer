import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    id: page1

    Connections {
        target: api
        onAuthSuccess: {
            gameClient.switchChatChannel("lobby")
            gameClient.refresh_lobby()
            stack.replace("qrc:/Pages/MainPage.qml")
            busyOverlay.visible = false
        }
        onAuthFailed: {
            busyOverlay.visible = false
            errorLabel.text = reason;
        }
    }

    ColumnLayout {
        id: loginForm
        width: parent.width > 300 ? 300 : parent.width - 40
        height: implicitHeight
        anchors { horizontalCenter: parent.horizontalCenter; top: rabbit.bottom; topMargin: 70 }

        Label { text: qsTr("Login")}

        TextField {
            id: textField1
            text: "chlebzycia666"
            Layout.fillWidth: true
        }

        Label { text: qsTr("Hasło") }

        TextField {
            id: textField2
            text: ""
            Layout.fillWidth: true
            echoMode: TextInput.PasswordEchoOnEdit
        }

    }

    RowLayout {
        id: rowLayout1
        width: parent.width > 300 ? 300 : parent.width - 40
        height: implicitHeight
        anchors { horizontalCenter: parent.horizontalCenter; top: loginForm.bottom; topMargin: 20; }

        Button {
            id: loginButton
            text: qsTr("Zaloguj")
            Layout.fillWidth: true
            onClicked: {
                busyOverlay.visible = true
                api.attemptLogin(textField1.text, textField2.text)
            }
        }

        Button {
            id: registerButton
            text: qsTr("Zarejestruj")
            Layout.fillWidth: true
            onClicked: {
                stack.push("qrc:/Pages/RegisterPage.qml")
            }
        }
    }

    Image {
        id: rabbit
        anchors.topMargin: 40
        anchors { top: parent.top; left: parent.left; right: parent.right; }
        source: "qrc:/img/arthurlogo_small.png"
        fillMode: Image.PreserveAspectFit
    }

    Label {
        text: api.getApiServer()
        anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.bottom; bottomMargin: 10 }
    }

    Label {
        id: errorLabel;
        text: "";
        wrapMode: Text.WordWrap
        anchors {
            top: rabbit.bottom
            topMargin: 20
            right: loginForm.right
            left: loginForm.left
        }
        color: "red";
    }

}
