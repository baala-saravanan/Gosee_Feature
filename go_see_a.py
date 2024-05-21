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

GPIO_TRIGECHO = 500
GPIO.setup(448, GPIO.IN)
GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
GPIO.output(GPIO_TRIGECHO, False)

def measure():
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)

    start = time.time()
    stop = start

    GPIO.setup(GPIO_TRIGECHO, GPIO.IN)

    while GPIO.input(GPIO_TRIGECHO) == 0:
        start = time.time()

    while GPIO.input(GPIO_TRIGECHO) == 1:
        stop = time.time()

    if 'stop' not in locals():
        machine_voice.play_machine_audio("now_press_confirm_button.mp3")

    GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
    GPIO.output(GPIO_TRIGECHO, False)

    time_elapsed = stop - start
    distance = time_elapsed * 34300 / 2  # Speed of sound is approximately 343 meters per second
    #distance = time_elapsed / 0.000058
    time.sleep(0.4)
    print("Start Time:", start)
    print("Stop Time:", stop)
    print("Time Elapsed:", time_elapsed)
    return distance
def restart_device():
    play_audio.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
    play_audio.play_machine_audio("Thank You.mp3")
    subprocess.run(["reboot"])
    return
    
def main():
    count = 0
    try:
        while True:
            distance = measure()
            print("Distance: %.1f cm" % distance)
            input_state = GPIO.input(448)
            
            if 137.16 <= distance <= 213.36:
                # Add your logic for correct distance range
                media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/340Hz-5sec.wav")
                media.play()
                time.sleep(1.25)
                media.stop()
                print("h1")
                count = 0
                what_obj.detect()
                
            elif 20 <= distance <= 121.91 :
                # Add your logic for another distance range
                media = vlc.MediaPlayer("/home/rock/Desktop/Hearsight/audios/beeb/3_long_high.mp3")
                media.play()
                time.sleep(1.25)
                media.stop()
                print("h3")
                count = 0
                what_obj.detect()
                
            elif 14 <= distance <= 15:
                count += 1
            elif distance >= 15:
                count = 0
            if count >= 40:
                restart_device()
                break
            # Add more conditions for different distance ranges
            elif input_state == True:
                play_audio.play_machine_audio("feature_exited.mp3")
                sys.exit()
                break
    except Exception as e:
        print(f"Error occurred:{e}")
    
if __name__ == "__main__":
    main()
