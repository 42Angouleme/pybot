#! /bin/python3
import module_microphone as microphone
import module_audio as audio
import module_camera as camera
import module_ia as ia
import module_ecran as ecran

def main():
    microphone.run()
    audio.run()
    camera.run()
    ia.run()
    ecran.run()

if __name__ == "__main__":
    print('=' * 42)
    print("HACKATHON : Robot Python - 16/17 Aout 2023")
    print('=' * 42)
    main()