import cv2
from django.http import HttpResponse
from django.views.decorators import gzip


def video_feed(request):
    try:
        cap = cv2.VideoCapture("rtsp://admin:Data@1357@192.168.1.193:554/cam/realmonitor?channel=1&subtype=0", cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        writer = None
        recording = False

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if recording:
                if writer is None:
                    writer = cv2.VideoWriter('recording.mp4', fourcc, 30.0, (720, 480))

                writer.write(frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break
            elif key == ord('r'):
                recording = not recording
                if recording:
                    print('Recording started...')
                else:
                    print('Recording stopped...')
                    if writer is not None:
                        writer.release()
                        writer = None

        cap.release()

        if writer is not None:
            writer.release()

        cv2.destroyAllWindows()

        return HttpResponse("Video stream ended.")

    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse(f"Error: {e}")
