import cv2
import time
import win32gui,win32con 



def minimizeWindow():
    window=win32.GetForcegroundWindow()
    win32gui.ShowWindow(window,win32con.SW_MINIMIZE)


    
def cctv ():
    video = cv2.VideoCapture (0)
    video.set (3,640)
    video.set(4,480)
    width = video.get(3)
    height = video.get(4)
    print("Video resolution is set to ", width,' x ',height)
    print("Help-- \n1.Press esc key to exit.\n2.press m to minimize.")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    date_time = time.strftime("recording %H-%M-%d-%m-%y")
    output = cv2.VideoWriter('footages/'+date_time+'.mp4',fourcc,20.0,(640,480))
    while video.isOpened():
        check, frame = video.read()
        if check == True:
            frame = cv2.flip(frame, 1)
            t = time.ctime()
            cv2.rectangle(frame,(5,5,100,20),(255,255,255),cv2.FILLED)
            cv2.putText(frame,"Camera 1",(20,20),cv2.FONT_HERSHEY_DUPLEX,0.5,(255,255,255),1)
            cv2.imshow('CCTV Camera',frame)
            output.write(frame)
            if cv2.waitKey(1)==27:
                print("Video footage saved in current directory")
                break
            elif cv2.waitKey(1)==ord('m'):
                minimizeWindow()
        else:
            print("Can't open camera,check configuration")
            break
    video.release()
    output.release()
    cv2.destroyAllWindows()
print("*"*80+"\n"+" "*30+"Welcome to cctv sodtware\n"+"*"*80)
ask = int(input("Do you want to open the CCTV?\nl.yes\n2.no\n>>>"))
if ask==1:
    cctv()
elif ask==2:
    print("Byeee have a nice day!!")
    exit
