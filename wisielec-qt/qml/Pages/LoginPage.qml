import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    id: page1

    ColumnLayout {
        x: 184
        y: 58
        width: 293
        height: 121
        anchors.horizontalCenter: parent.horizontalCenter

        Label {
            id: label1
            text: qsTr("Login")
        }

        TextField {
            id: textField1
            text: "chlebzycia666"
            Layout.fillWidth: true
        }

        Label {
            id: label2
            text: qsTr("Hasło")
        }

        TextField {
            id: textField2
            text: "chleb1234"
            Layout.fillWidth: true
        }

    }

    RowLayout {
        id: rowLayout1
        x: 184
        y: 195
        width: 293
        height: 40
        anchors.horizontalCenter: parent.horizontalCenter

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

}
