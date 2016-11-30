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

            if (!urlString.match("profiles\/register")) {
                // back on lobby page, quit
                stack.pop()
            }
        }
        Component.onCompleted: url = "http://" + api.getApiServer() + "/profiles/register"
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
