import ffmpeg
import os
import shutil

def extract_frames(input_video_path: str, output_folder: str, frame_rate: int = 1) -> None:
    """
    Extract frames from a video file at a specified frame rate.

    :param input_video_path: Path to the input video file.
    :param output_folder: Folder where extracted frames will be saved.
    :param frame_rate: Number of frames to extract per second (default is 1).
    """

    tmp_directory_exists = os.path.exists("tmp")
    if tmp_directory_exists:
        remove = input("Temporary directory already exists. Remove? (y/n): ")
        
        if remove.lower() == "y":
            shutil.rmtree("tmp")
            print("Temporary directory removed.")
        else:
            print("Temporary directory not removed. Cancelling extraction.")
            return
    
    os.makedirs("tmp")

    # Run FFmpeg frame extraction
    try:
        print("Starting frame extraction for video:", input_video_path)
        (
            ffmpeg
            .input(input_video_path)
            .output(f"tmp/frame_%d.png", format="image2", vcodec="png")
            .run(overwrite_output=True, quiet=True)    
        )
        print(f"Frames successfully extracted to temporary directory, starting to move them to {output_folder}")
    except ffmpeg.Error as e:
        print(f"Error extracting frames: {e}")

    
    # Move extracted frames to the specified output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    # Extract the frame number from a string, assuming the format is "frame_1.png", "frame_2.png", etc.
    extract_frame_number = lambda x: int(x[6:-4])

    frames_by_number = sorted(os.listdir("tmp"), key=extract_frame_number)
    for i in range(0, len(frames_by_number), frame_rate):
        filename = frames_by_number[i]
        
        if filename.endswith(".png"):
            src_path = os.path.join("tmp", filename)
            dst_path = os.path.join(output_folder, filename)
            shutil.move(src_path, dst_path)
    print(f"Frames moved to {output_folder}")


    # Cleanup
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
        print("Temporary directory cleaned up.")
    else:
        print("No temporary directory to clean up.")