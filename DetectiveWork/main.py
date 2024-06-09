import cv2
import os

# Make sure to update paths as per your operating system and directories.

output_directory = "motion_frames"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Parameters for resizing and ROI
resize_width = 320
resize_height = 240
roi_x, roi_y, roi_width, roi_height = (
    0,
    0,
    300,
    300,
)  # Modify these values as needed

all_frames = 1200 * 60 * 24 * 3
frame_counter = 0


# Function to process a single video file
def process_video(video_path, date, hour):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {video_path}: Total frames: {total_frames}")

    ret, prev_frame = cap.read()
    if not ret:
        print(f"Error: Could not read first frame of {video_path}.")
        return

    prev_frame = cv2.resize(prev_frame, (resize_width, resize_height))
    roi_x_adj = int(roi_x * resize_width / cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    roi_y_adj = int(roi_y * resize_height / cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    roi_width_adj = int(roi_width * resize_width / cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    roi_height_adj = int(
        roi_height * resize_height / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray_roi = prev_gray[
        roi_y_adj : roi_y_adj + roi_height_adj, roi_x_adj : roi_x_adj + roi_width_adj
    ]

    motion_detected = False
    # frame_counter = 0
    skip_frames = 5  # Number of frames to skip

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        global frame_counter
        frame_counter += 1
        if frame_counter % skip_frames != 0:
            continue

        frame = cv2.resize(frame, (resize_width, resize_height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_roi = gray[
            roi_y_adj : roi_y_adj + roi_height_adj,
            roi_x_adj : roi_x_adj + roi_width_adj,
        ]

        diff = cv2.absdiff(prev_gray_roi, gray_roi)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        motion = (
            cv2.countNonZero(thresh) > 5
        )  # Adjust this threshold based on your requirements

        if motion and not motion_detected:
            motion_detected = True
            # Draw a rectangle around the ROI
            # Find contours of the motion
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            for contour in contours:
                if (
                    cv2.contourArea(contour) < 0
                ):  # Adjust the minimum area threshold based on your requirements
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(
                    frame,
                    (roi_x_adj + x, roi_y_adj + y),
                    (roi_x_adj + x + w, roi_y_adj + y + h),
                    (0, 255, 0),
                    2,
                )
            # Save the frame with detected motion
            output_filename = os.path.join(
                output_directory,
                f"{os.path.splitext(os.path.basename(video_path))[0]}_{date}_{hour}_frame_{frame_counter}.jpg",
            )
            cv2.imwrite(output_filename, frame)
            print(f"Motion detected. Saved frame {frame_counter} to {output_filename}")

            # cv2.imshow("Motion in ROI", frame)

            # while True:
            #     key = cv2.waitKey(1) & 0xFF
            #     if key == ord(" "):
            #         cv2.destroyWindow("Motion in ROI")
            #         motion_detected = False
            #         break

        prev_gray_roi = gray_roi.copy()
        global all_frames

        percentage_complete = (frame_counter / all_frames) * 100
        print(f"{os.path.basename(video_path)}: {percentage_complete:.2f}% complete")

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Directory containing the video files
target_dates = ["20240517", "20240518", "20240519"]
target_hours = [str(i).zfill(2) for i in range(0, 24)]

# Supported video file extensions
video_extensions = [".mp4", ".avi", ".mov", ".mkv"]

for date in target_dates:
    for target_hour in target_hours:
        video_directory = (
            f"/Users/$USER/Desktop/CameraFootage/{date}/{target_hour}"  # /42.mp4"
        )

        # Get a list of video files in the directory
        video_files = [
            os.path.join(video_directory, f)
            for f in os.listdir(video_directory)
            if os.path.isfile(os.path.join(video_directory, f))
            and os.path.splitext(f)[1] in video_extensions
        ]

        video_files.sort()

        # video_files = video_files[36:]

        total_videos = len(video_files)
        print(f"Total number of videos to process: {total_videos}")

        # Process each video file
        for idx, video_file in enumerate(video_files):
            print(
                f"Processing video {idx + 1} of {total_videos}: {os.path.basename(video_file)}"
            )
            process_video(video_file, date, target_hour)
            print(f"Completed {idx + 1} of {total_videos} videos.")
