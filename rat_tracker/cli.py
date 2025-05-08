import argparse
import video_frame_extractor

def main():
    # Create a new argument parser (CLI instance)
    parser = argparse.ArgumentParser(prog="Rat Tracker", description="A CLI for analyzing rat movement when impaired by drugs.")

    # Allow the CLI to accept subcommands
    subparser = parser.add_subparsers(dest="command")

    # Create a subcommand for extracting frames, extract
    extract = subparser.add_parser("extract", help="extract frames from an mp4 video file")


    extract.add_argument('-i', help="path to the rat video to analyze", nargs=1)
    extract.add_argument('-step', help="amount of frames to skip at each analysis interval", nargs=1)
    extract.add_argument('-o', help="path to the output folder where you want to place frames", nargs=1)

    args = parser.parse_args()

    # Test command: RUN FROM ROOT!! 
    # python rat_tracker/cli.py extract -i "data/in/kyomoton cane.mp4" -step 25 -o data/out/kyomoton/
    if args.command == "extract":
        if args.i and args.step:
            video_path: str = args.i[0]
            step = int(args.step[0])
            output_path: str = args.o[0] if args.o else "output.txt"

            print(f"Analyzing video at {video_path} with a step of {step} frames and outputting at {output_path}.")
            video_frame_extractor.extract_frames(video_path, output_path, step)
    else:
        parser.print_help()



if __name__ == "__main__":
    main()