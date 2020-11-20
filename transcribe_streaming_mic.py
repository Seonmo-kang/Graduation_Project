# -*- coding: utf-8 -*-
#!/home/pi/Desktop/real_server/webserver_2202/


# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.
NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:
    pip install pyaudio
Example usage:
    python transcribe_streaming_mic.py
"""

# [START speech_transcribe_streaming_mic]
from __future__ import division
import re
import sys
import urllib
import json
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from modules.dbModule import Database


#외부 라이브러리의 기본 인코딩 방식 설정
#reload(sys)
#sys.setdefaultencoding('utf-8')

# Audio recording parameters
RATE = 48000
CHUNK = 1024 #int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
cmdLists = [
        #명령어    대답    종료 리턴값
    [u'끝',     '잘가요',       0],
    [u'끝내',     '잘가요',       0],
    [u'꺼 줘',     '잘가요',       0],
    [u'온습도', 'DHT',      1],
    [u'내 방 불 켜', 'LEDON',      1],
    [u'내 방 불 꺼', 'LEDOFF',      1],
    [u'거실 불 켜', 'LED2ON',      1],
    [u'거실 불 꺼', 'LED2OFF',      1],
    [u'주차장 불 켜', 'LED3ON',      1],
    [u'주차장 불 꺼', 'LED3OFF',      1],
    [u'불 다 켜', 'ALLLEDON',      1],
    [u'불 다 꺼', 'ALLLEDOFF',      1],
    [u'주차장 문 열', 'DOORON',      1],
    [u'주차장 문 닫', 'DOOROFF',      1]
]
def cmd_add():
    mode_db = Database()
    mode_lists = mode_db.showAll()
    print("mode_list :",mode_lists)
    print(len(mode_lists))
    for mode in range(len(mode_lists)):
        print(mode)
    for mode in range(len(mode_lists)):
        mode_name = mode_lists[mode]['module_name']
        print(mode_name)
        cmdLists.append([mode_name,'mode',1])
        print(cmdLists)

def order(name,stt):
    mode_db = Database()
    mode = mode_db.show(name)
    print('mode is ',mode)
    server_url = "http://192.168.43.104/" 
    url = server_url+stt
    try:
        if (stt == 'mode'):
            data = {"l_led" : mode['l_led'],
                    "m_led": mode['m_led'],
                    "g_led": mode['g_led'],
                    "window": mode['window'],
                    "g_window": mode['g_window'],
                    }
            print('data : ',data)
            print('MODE data sending...')
            #data_str = str(data)
            #print('String data : ',data_str)
            #en_data_str = data_str.encode('utf-8')
            #print('Encoding String data : ',en_data_str)
            params = json.dumps(data).encode('utf8')
            print(params)            
            request = urllib.request.urlopen(url,data=params)
            #en_data_str,{'Content-Type':'application/json'}
            print("MODE is starting")
        else:
            urllib.request.urlopen(url)
            print("send complete")
    except:
        print("send failed or exit complete")

"""
리턴이 0이면 종료
"""
def CommandProc(stt):
    # 문자 양쪽 공백 제거
    cmd = stt.strip()
    # 입력 받은 문자 화면에 표시
    print(u'나 : ' + str(cmd))

    for cmdList in cmdLists:
        if re.search(cmdList[0], str(cmd), re.I):
            #명령 리스트와 비교
            result = order(cmdList[0],cmdList[1])
            # 종료 명령 리턴 0이면 종료
            # 1이면 계속
            if cmdList[2] == 0:
                return cmdList[2]  
        # 명령이 없거
        # 계속            
    print (u'Excuse me?')
    return 1
"""

"""
    
def listen_print_loop(responses):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            #### 추가 ### 
            
            if CommandProc(transcript) == 0:
                break
            #else:
                #return CommandProc(transcript)
            """
                # 원래 있던 코드는 주석처리
                print(transcript + overwrite_chars)
                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break
            """
            num_chars_printed = 0
def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-KR'  # a BCP-47 language tag en-US
    cmd_add()
    credential = "/home/pi/Downloads/logical-carver-277605-91fe57214bc9.json"
    client = speech.SpeechClient()#"credentials="/home/pi/Downloads/logical-carver-277605-91fe57214bc9.json")
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        
        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()
# [END speech_transcribe_streaming_mic]
