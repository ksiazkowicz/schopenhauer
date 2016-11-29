import QtQuick 2.0
import QtWebView 1.1
import QtQuick.Controls 2.0

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
        Component.onCompleted: url = "http://127.0.0.1:8000/profiles/register"
    }
}
