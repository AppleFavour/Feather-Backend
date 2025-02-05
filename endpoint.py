import os
from flask import Flask, request, Response

backend = Flask(__name__)


@backend.route("/feather/genPlist/", methods=["GET"])
def generate_plist():
    bundleid = request.args.get("bundleid", "")
    name = request.args.get("name", "")
    version = request.args.get("version", "")
    fetchurl = request.args.get("fetchurl", "")

    # print(f"ID: {bundleid}, Name: {name}, Version: {version}, Fetch: {fetchurl}")
    plist_template = """<?xml version="1.0" encoding="UTF-8"?>
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
    </plist>"""

    plist_content = (
        plist_template.replace("fetchurl", fetchurl)
        .replace("bundleid", bundleid)
        .replace("version", version)
        .replace("name", name)
    )

    return Response(plist_content, mimetype="application/xml")


if __name__ == "__main__":
    backend.run(host="0.0.0.0", port=1234)
