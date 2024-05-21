import time
import gpio as GPIO
import sys
import subprocess
import vlc
from pydub import AudioSegment
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from play_audio import GTTSA
from English.go_see.what import SSD

what_obj = SSD()
play_audio = GTTSA()

GPIO_TRIGECHO = 501
GPIO.setup(448, GPIO.IN)
GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
GPIO.output(GPIO_TRIGECHO, False)

def measure():
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)
    start = time.time()
    GPIO.setup(GPIO_TRIGECHO, GPIO.IN)
    while GPIO.input(GPIO_TRIGECHO)==0:
        start = time.time()
    while GPIO.input(GPIO_TRIGECHO)==1:
        stop = time.time() 
    if 'stop' not in locals():# Add a check to see if 'stop' variable is still undefined
#        machine_voice.play_machine_audio("sensor_is_not_working_so_switch_off_the_HearSight_device_for_some_time_and_then_start_it_again.mp3")
         play_audio.play_machine_audio("now_press_confirm_button.mp3")
    GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
    GPIO.output(GPIO_TRIGECHO, False)
    TimeElapsed = stop-start
    distance = TimeElapsed / 0.000058
#    distance = (TimeElapsed * 34300)/1.5
    time.sleep(0.1)
    return distance

while True:
    distance = measure()
    print("Distance: %.1f cm" % distance)
    
#    if distance<=457.2 and distance >=426.72:#15 to 14
#        play_audio.play_machine_audio("340Hz-5sec.wav")
#        time.sleep(0.3)
#        what_obj.detect()
        
#    elif distance<=304.8 and distance >=274.32:#10 to 09
    if distance<=243.84 and distance >=182.88:#08 to 06
#        play_audio.play_machine_audio("440Hz-6sec.wav")
        play_audio.play_machine_audio("1_Short_Main.mp3")
        time.sleep(0.3)
        what_obj.detect()
        
    elif distance<=121.92 and distance >=60.96:#04 to 02
#        play_audio.play_machine_audio("640-3.5min.wav")
        play_audio.play_machine_audio("1_long_high.wav")
        time.sleep(0.3)
        what_obj.detect()

    input_state = GPIO.input(448)
    if input_state == True:
        play_audio.play_machine_audio("exit_button_pressed.mp3")
        break
