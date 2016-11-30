import QtQuick 2.0
import QtWebView 1.1
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    WebView {
        id: webview
        url: "about:blank"
        anchors.fill: parent
        onUrlChanged: {
            console.log(url)
            var urlString = url.toString();

            if (!urlString.match("game\/new_game")) {
                // back on lobby page, quit
                stack.pop()
                gameClient.refresh_lobby()
            }
        }
        Component.onCompleted: url = "http://" + api.getApiServer() + "/game/new_game"
    }
    footer: ToolBar {
        RowLayout {
            anchors.fill: parent;
            ToolButton {
                text: "\uE72B"
                font.family: "Segoe MDL2 Assets"
                onClicked: stack.pop()
            }
        }
    }
}
