# [START gae_python37_app]
from flask import Flask, request, Response 
import os
import slack

import gspread
from google.oauth2.service_account import Credentials

import json

from slack_block import ObjectPlainText as PText
from slack_block import ObjectMrkdwnText as MText
import slack_block as sb

slack_token = os.environ["SLACK_API_TOKEN_BOT"]
client = slack.WebClient(token=slack_token)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

class ProjectList:
    def __init__(self):
        scopes = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_file('ohinata-slack-bot-ccdaaa15b4f3.json', scopes=scopes)
        gc = gspread.authorize(credentials)
        wks = gc.open("プロジェクトリスト").sheet1
        self.values = wks.get_all_values()

        subjects = self.values[2]
        subjects[0] = 'id'
        data_list = self.values[3:] 
        projects = []

        for data in data_list:
            if not data[1] == '':
                temp = {
                    subjects[i]:data[i] for i in range(8)
                }
                projects.append(temp)
        self.project = projects

    def ListBlock(self, index):
        blocks = [
            sb.BlockDivider(),
            sb.BlockSection(
                text=MText("*#{}* *{}*".format(self.project[index]['id'], self.project[index]['プロジェクト名']))
            ),
            sb.BlockContext(
                elements=[
                    MText("*登録者* : {}\n*内容*　 : {}".format(self.project[index]['登録者'],self.project[index]['内容']))
                ]
            ),
            sb.BlockSection(
                text=MText("{}".format(self.project[index]['備考・コメント']))
            ),
            sb.BlockContext(
                elements=[
                    MText("*登録日* : {}\n*チャンネル* : {}".format(self.project[index]['登録日'],self.project[index]['プロジェクトルームのリンク']))
                ]
            )
        ]
        return blocks

    def AllListBlocks(self):
        blocks = []
        for index in range(len(self.project)):
            if not self.project[index]['プロジェクト名'] == '':
                blocks.extend(self.ListBlock(index))
        return blocks

@app.route('/interaction', methods=['POST'])
def interaction():
    form = json.loads(request.form['payload'])
    if form['type'] == 'block_actions':
        if form['actions'][0]['action_id'] == 'action_show_projectlist':
            pjlist = ProjectList()
            message = sb.Message()
            message.addBlocks(pjlist.AllListBlocks())

            print(pjlist.AllListBlocks())

            client.chat_postEphemeral(
                channel=form['channel']['id'],
                user=form['user']['id'],
                text="Project List",
                blocks = message.getPayload()['blocks']
            )

            return Response(response="OK", status=200)

    return Response(response="OK", status=200)


@app.route('/command', methods=['GET','POST'])
def command():
    blocks = [
        sb.BlockSection(text=MText("なにが知りたいですか？")),
        sb.BlockAction(
            elements=[
                sb.ElementButton(text=PText("プロジェクト一覧"), action_id="action_show_projectlist"),
                sb.ElementButton(text=PText("プロジェクトリストのシート"), action_id="action_link_to_projectlist",
                    url="https://docs.google.com/spreadsheets/d/11bz1FbA12aLSZLVE7w-X97aqfZ3YrFBXcl-nu5rGiHw/edit?usp=sharing")
            ]
        )
    ]
    message = sb.Message()
    message.addBlocks(blocks)

    print(message.getPayload())

    client.chat_postEphemeral(
        channel=request.form['channel_id'],
        user=request.form['user_id'],
        text="hoge",
        blocks = message.getPayload()['blocks']
    )
    return Response(status=200)


@app.route('/redirect', methods=['GET','POST'])
def redirect():
    return Response(response="OK", status=200)


@app.route('/event', methods=['POST'])
def event():
    json_data = request.get_json()
    print(json_data)

    if json_data['event']['type'] == 'app_mention':
        blocks = [
            sb.BlockSection(text=MText("なにが知りたいですか？")),
            sb.BlockAction(
                elements=[
                    sb.ElementButton(text=PText("プロジェクト一覧"), action_id="action_show_projectlist"),
                    sb.ElementButton(text=PText("プロジェクトリストのシート"), action_id="action_link_to_projectlist",
                        url="https://docs.google.com/spreadsheets/d/11bz1FbA12aLSZLVE7w-X97aqfZ3YrFBXcl-nu5rGiHw/edit?usp=sharing")
                ]
            )
        ]
        message = sb.Message()
        message.addBlocks(blocks)

        print(message.getPayload())

        client.chat_postEphemeral(
            channel=json_data['event']['channel'],
            user=json_data['event']['user'],
            text="hoge",
            blocks = message.getPayload()['blocks']
        )
        return Response(status=200)

    return Response(response="OK", status=200)
    """
    # Verify Challenge
    print(json_data)
    return Response(response=json_data['challenge'], status=200)
    """

@app.route('/sheet', methods=['GET','POST'])
def sheet():
    scopes = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = Credentials.from_service_account_file('ohinata-slack-bot-ccdaaa15b4f3.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    wks = gc.open("project").sheet1
    print(wks.get('A1'))
    
    return Response(response="OK", status=200)


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    command()


# [END gae_python37_app]
