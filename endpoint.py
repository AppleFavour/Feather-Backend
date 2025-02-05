from flask import Flask as fl, request as req, Response as res

backend = fl(__name__)


@backend.route("/feather/genPlist/", methods=["GET"])
def generate_plist():
    try:
        bundleid = req.args["bundleid"]
        name = req.args["name"]
        version = req.args["version"]
        fetchurl = req.args["fetchurl"]
        """
        bundleid = req.args.get("bundleid", "")
        name = req.args.get("name", "")
        version = req.args.get("version", "")
        fetchurl = req.args.get("fetchurl", "")
        """

        install_plist_temp = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
            <dict>
                <key>items</key>
                <array>
                    <dict>
                        <key>assets</key>
                        <array>
                            <dict>
                                <key>kind</key>
                                <string>software-package</string>
                                <key>url</key>
                                <string>fetchurl</string>
                            </dict>
                        </array>
                        <key>metadata</key>
                        <dict>
                            <key>bundle-identifier</key>
                            <string>bundleid</string>
                            <key>bundle-version</key>
                            <string>version</string>
                            <key>kind</key>
                            <string>software</string>
                            <key>title</key>
                            <string>name</string>
                        </dict>
                    </dict>
                </array>
            </dict>
        </plist>
        """

        install_plist = (
            install_plist_temp.replace("fetchurl", fetchurl)
            .replace("bundleid", bundleid)
            .replace("version", version)
            .replace("name", name)
        )

        return res(install_plist, mimetype="application/xml", status=200)

    except Exception as error:
        return res(str(error), mimetype="text/plain", status=500)


if __name__ == "__main__":
    backend.run(host="0.0.0.0", port=1234)
