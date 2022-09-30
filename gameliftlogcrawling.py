import tkinter
import boto3
import os
from parse import *

client = boto3.client('gamelift')

def main():
    #OpenPort
    text.insert("current" ,"GameliftLogDownloder Start!\n")
    
    fleetid = inputbox01.get("1.0",tkinter.END).strip('\n\t')
    region = inputbox.get("1.0",tkinter.END).strip('\n\t')
    myid = inputbox02.get("1.0",tkinter.END).strip('\n\t')

    text.insert("current" , "OpenPort \n\n")
    try:
        openport = client.update_fleet_port_settings(
        FleetId=fleetid,
        InboundPermissionAuthorizations=[
            {
                'FromPort': 22,
                'ToPort': 22,
                'IpRange': '61.37.80.131/32',
                'Protocol': 'TCP'
            }
        ]
        )
        text.insert("current" ,openport)
        text.insert("current" ,"\n\n")
    except Exception as errortext: #todo. 여기선 듀플리케이트 에러또한 발생할수 있는데 이는 이미 포트목록에 있어서 작업 실패했다는뜻이라 이 작업을 건너뛰는 식으로 처리를 해야한다.
        text.insert("current" , "\n\nError : OpenPort \n\n")
        text.insert("current" ,errortext)
        text.insert("current" ,"\n\n")
        #return # 함수 정지
    

    #DescrIbeinstance
    text.insert("current" , "DescrIbeinstance \n\n")
    try:
        describeinstance = client.describe_instances(
        FleetId=fleetid,
        Location=region
        )
        text.insert("current" ,describeinstance)
        text.insert("current" ,"\n\n")
    except Exception as errortext:
        text.insert("current" , "Error : DescrIbeinstance \n\n")
        text.insert("current" ,errortext)
        text.insert("current" ,"\n\n")
        return # 함수 정지
    

    #InstancesParse
    text.insert("current" , "InstancesParse \n\n")
    try:
        instanceid = str(describeinstance.get('Instances')[0].get('InstanceId'))
        ipaddress = str(describeinstance.get('Instances')[0].get('IpAddress'))
    except Exception as errortext:
        text.insert("current" , "Error : InstancesParse \n\n")
        text.insert("current" ,errortext)
        text.insert("current" ,"\n\n")
        return # 함수 정지


    #GetInstanceAccess
    text.insert("current" , "GetInstanceAccess \n\n")
    try:
        getinstanceaccess = client.get_instance_access(
        FleetId=fleetid,
        InstanceId=instanceid
        )
    except Exception as errortext:
        text.insert("current" , "Error : GetInstanceAccess \n\n")
        text.insert("current" ,errortext)
        text.insert("current" ,"\n\n")
        return # 함수 정지

  #GetPublicKey
    text.insert("current" , "GetPublicKey \n\n")
    try:
        publickey = str(getinstanceaccess.get('InstanceAccess').get('Credentials').get('Secret'))
        username = str(getinstanceaccess.get('InstanceAccess').get('Credentials').get('UserName'))
    except Exception as errortext:
        text.insert("current" , "Error : GetPublicKey \n\n")
        text.insert("current" ,errortext)
        text.insert("current" ,"\n\n")
        return # 함수 정지

    file = open("./SecretKey.pem", "w")
    file.write(publickey)
    file.close()

    operation = "scp -r -i ./SecretKey.pem "+ username +"@"+ipaddress+":/local/game/K2/Saved .\\ \nyes"
    os.system(operation)


# GUI
window = tkinter.Tk()
window.title("GameliftSaveFileDownloder")
window.geometry("640x400")
window.resizable(False, False)

text=tkinter.Text(window, width=100, height=10, fg="black", relief="solid", yscrollcommand='Any')
text.insert(tkinter.CURRENT, "게임리프트 서버의 Log를 몽땅 가져온다!\n*주의 : AWS CLI 설치와 해당 Gamelift 조작권한을 가진 계정으로 로그인이 선행되어야 합니다.")
text.pack(side="top", fill="both", expand=True)

frame=tkinter.Frame(width=100, height=1, relief="solid", bd=1)
frame.pack(fill="both")

frame01=tkinter.Frame(width=100, height=1, relief="solid", bd=1)
frame01.pack(fill="both")

frame02=tkinter.Frame(width=100, height=1, relief="solid", bd=1)
frame02.pack(fill="both")

#Region
message=tkinter.Message(frame, text="Region :", width=100)
message.pack(side="left")
inputbox=tkinter.Text(frame, width=100, height=1, fg="black", relief="solid", yscrollcommand='Any')
inputbox.pack(side="right")
inputbox.insert("current" ,"ap-northeast-2")   

#FleetID
message01=tkinter.Message(frame01, text="FleetID :", width=100)
message01.pack(side="left")
inputbox01=tkinter.Text(frame01, width=100, height=1, fg="black", relief="solid", yscrollcommand='Any')
inputbox01.pack(side="right")

message02=tkinter.Message(frame02, text="MyIP :", width=100)
message02.pack(side="left")
inputbox02=tkinter.Text(frame02, width=100, height=1, fg="black", relief="solid", yscrollcommand='Any')
inputbox02.pack(side="right")
inputbox02.insert("current" ,"0.0.0.0/0")

button = tkinter.Button(window, overrelief="solid", width=15, padx=5, pady=5, command=main, highlightthickness=1, text="Generate!", relief="solid", bd=1)
button.pack(side="bottom")

window.mainloop()