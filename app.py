#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, Response
from modules.dbModule import Database
import requests
import json
from camera import VideoCamera
import urllib
import transcribe_streaming_mic

url = "http://192.168.43.104/"
led_on = "LEDON"   # led on
led_off = "LEDOFF" # led off
led2_on = "LED2ON" # led2 on
led2_off = "LED2OFF" # led2 on
led3_on = "LED3ON" # led2 on
led3_off = "LED3OFF" # led2 on
window_on = "WINDOWON"
window_off = "WINDOWOFF"
door_on = "DOORON" # door open
door_off = "DOOROFF" # door lock
dht = "DHT" # dht 


app = Flask(__name__)
app.config['SAVE_ON_FILE_MAX_AGE'] = 0




@app.route('/')
def index():
    # request ( DHT22 )
    # need to recieve request message 
    return render_template('index.html')
@app.route('/mode_page')
def mode_page():
    return render_template("mode1.html")

#@app.route('/signin')
#def signin():
@app.route('/dht',methods=['POST'])
def dht():
    res = urllib.request.urlopen(url+dht)
    read_res = res.read().decode('utf-8')
    print("read_res : ",read_res)
    text_res = read_res.text
    print("text_res = ",text_res)

@app.route('/insert',methods=["POST"])
def insert():
    insert_class = Database()   # 먼저 ID 값부터 수정해야한다.
    print('DB 연동 성공')
    name = request.form['name']
    l_led = request.form['l_led']
    m_led = request.form['m_led']
    g_led = request.form['g_led']
    window = request.form['window']       # name,led,window 3개 값을 들고 와야한다.
    g_window = request.form['g_window']       # text로 보내기 때문에request.form[''] 쓰기
    print('값 들고오기 성공')
    result = insert_class.check(name)  # INSERT하기 전에 name으로 된 값이 있는 지 확인해야 한다. t/f로 반환
    if( insert_class.d_check == True):
        insert_class.insert((name,l_led,m_led,g_led,window,g_window))
        result=('해당 설정을 등록하였습니다!')
        print('등록하기 성공')
    return result

@app.route('/switch-change', methods=['POST'])
def switch():
    data = request.data.decode('utf8')
    jdata = json.loads(data)
    print(jdata)
    if jdata['num']=='1':
        if jdata['state']:
           print("on")
           #requests.get(url+led_on)
           #res = urllib.request.get(url+led_on)
           res = urllib.request.urlopen(url+led_on)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           #text_res = read_res.text
           #print("request : ",text_res)
           #print("data")
           #print(data)
           print('connect : true')
           
        else:
           print("off")
           res = urllib.request.urlopen(url+led_off)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : false')
         #return render_template('index.html',parameter=res)  
    elif jdata['num']=='2': # Living room1
        if jdata['state']:
           print("on")
           #requests.get(url+led_on)
           #res = urllib.request.get(url+led_on)
           res = urllib.request.urlopen(url+led2_on)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : true')      
        else:
           print("off")
           res = urllib.request.urlopen(url+led2_off)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print("request : ",text_res)
           print('connect : false')
         #return render_template(index.html,parameter=res)
    elif jdata['num']=='3': #LED3
        if jdata['state']:
           print("on")
           #requests.get(url+led_on)
           #res = urllib.request.get(url+led_on)
           res = urllib.request.urlopen(url+led3_on)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print("request : ",text_res)
           print('connect : true')
        else:
           print("off")
           res = urllib.request.urlopen(url+led3_off)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : false')
         #return render_template(index.html,parameter=res)
           #WINDOW
    elif jdata['num']=='4': 
        if jdata['state']: 
           print("on") 
           #requests.get(url+led_on)
           #res = urllib.request.get(url+led_on)
           res = urllib.request.urlopen(url+window_on)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : true')
           
        else:
           print("off")
           res = urllib.request.urlopen(url+window_off)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : false')
        return print("res : ",res)
    #on = requests.get(url+led_on)
    # num GARAGE DOOR
    elif jdata['num']=='5': 
        if jdata['state']: 
           print("on") 
           #requests.get(url+led_on)
           #res = urllib.request.get(url+led_on)
           res = urllib.request.urlopen(url+door_on)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : true')
           
        else:
           print("off")
           res = urllib.request.urlopen(url+door_off)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : false')
        return print("res : ",res)
    
    elif jdata['num']=='6': 
        if jdata['state']: 
           print("on") 
           #requests.get(url+led_on)
           #res = urllib.request.get(url+led_on)
           res = urllib.request.urlopen(url+door_on)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : true')
           
        else:
           print("off")
           res = urllib.request.urlopen(url+door_off)
           read_res = res.read().decode('utf-8')
           print("read_res : ",read_res)
           print('connect : false')
        return print("res : ",res)

@app.route('/mic')
def mic():
    MicrophoneStream.main()
    return print('complete')

@app.route('/camstreaming')
def camstreaming():
    return render_template('CamStreaming.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.43.100', port=8080)


