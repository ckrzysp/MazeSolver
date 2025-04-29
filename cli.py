import argparse

def main():
    parser = argparse.ArgumentParser(prog="Rat Tracker", description="A CLI for analyzing rat movement when impaired by drugs.")

    parser.add_argument('-i', help="path to the rat video to analyze", nargs=1)
    parser.add_argument('-step', help="amount of frames to skip at each analysis interval", nargs=1)
    parser.add_argument('-o', help="path to the output file", nargs=1)

    args = parser.parse_args()

    # Test command: python cli.py -i "in/kyomoton cane.mp4" -step 5 -o out/out.txt
    if args.i and args.step:
        video_path: str = args.i[0]
        step = int(args.step[0])
        output_path: str = args.o[0] if args.o else "output.txt"

        print(f"Analyzing video at {video_path} with a step of {step} frames and outputting at {output_path}.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()