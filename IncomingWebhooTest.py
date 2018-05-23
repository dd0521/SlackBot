import requests
import json
import versioncheck as verchk

# incoming Webhookで取得したURL
post_url = "https://hooks.slack.com/services/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"

def post_slack(name, text):
    requests.post(
        post_url,
        data=json.dumps(
            {"text": '<!channel>\n'+text,
             "username": name,
             "icon_emoji": ":python:"}))

latestVer_FF = verchk.VersionCheckMain('FireFox')
latestVer_Chrome = verchk.VersionCheckMain('Chrome')
latestVer_All = '[Latest Version]\n' + latestVer_FF + '\n\n' + latestVer_Chrome
post_slack( "App Version Notice", latestVer_All )