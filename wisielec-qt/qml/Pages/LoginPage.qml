import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    id: page1

    ColumnLayout {
        id: loginForm
        width: parent.width > 300 ? 300 : parent.width - 40
        height: implicitHeight
        anchors { horizontalCenter: parent.horizontalCenter; top: rabbit.bottom; topMargin: 30; }

        Label { text: qsTr("Login")}

        TextField {
            id: textField1
            text: "chlebzycia666"
            Layout.fillWidth: true
        }

        Label { text: qsTr("Hasło") }

        TextField {
            id: textField2
            text: "chleb1234"
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
                api.attemptLogin(textField1.text, textField2.text)
                stack.replace("qrc:/Pages/MainPage.qml")
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
        anchors { top: parent.top; left: parent.left; right: parent.right; }
        source: "qrc:/img/suicide_rabbit.png"
        fillMode: Image.PreserveAspectFit
    }

    Label {
        text: api.getApiServer()
        anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.bottom; bottomMargin: 10 }
    }

}
