import fnmatch
import os

import matplotlib.pyplot as plt
import pandas as pd

GPU_BASE_PATH = "runs/detect/GPU/"
CPU_BASE_PATH = "runs/detect/CPU/"

def combine_graphs():
    # OPTIONS YOU CAN CHANGE!! I put them up here for ease of access

    # The columns in the CSVs you want to visualize.
    columns_to_visualize = [
        "train/box_loss",
        "train/cls_loss",
        "train/dfl_loss",
        "metrics/precision(B)",
        "metrics/recall(B)",
        "metrics/mAP50(B)",
        "metrics/mAP50-95(B)",
        "val/box_loss",
        "val/cls_loss",
        "val/dfl_loss",
    ]

    # Paths to the CPU or GPU that we used for testing. EPOCHS_PATH_STRING will be used to get the full path later.
    model_results_paths = [
        GPU_BASE_PATH + "ant-4070s",
        GPU_BASE_PATH + "chris-1660ti",
        GPU_BASE_PATH + "thomas-3070"
    ]

    line_colors = ["red", "green", "blue"]
    line_styles = ["-", "--"]
    markers = ["o", "v", "^", "<", ">", "8", "s", "p", "*"]

    # Must be an amount we trained on, 10, 25, 50, or 100. they must also have been trained (e.g. Chris wasn't able to train 100 epochs on his GPU)
    epochs_amt = 25



    # End changeable options

    EPOCHS_PATH_STRING = f"train{epochs_amt}e"

    COMBINED_PATH_CSVS = [ path + "/" + EPOCHS_PATH_STRING + "/" + "results.csv" for path in model_results_paths ]

    columns_per_row = len(columns_to_visualize) // 2

    fig, ax = plt.subplots(figsize=(24, 12), nrows=2, ncols=columns_per_row)

    for i, y_axis_column_name in enumerate(columns_to_visualize):
        for j, csv_file in enumerate(COMBINED_PATH_CSVS):

            try:
                df = pd.read_csv(csv_file)

                x_axis_data = df['epoch']
                y_axis_data = df[y_axis_column_name]

                y_label = (csv_file
                           .removeprefix(GPU_BASE_PATH)
                           .removeprefix(CPU_BASE_PATH)
                           .removesuffix("/results.csv")
                           .removesuffix(f"/{EPOCHS_PATH_STRING}"))

                row, col = i // columns_per_row, i % columns_per_row

                ax_col = ax[ row, col ]

                ax_col.plot(
                    x_axis_data,
                    y_axis_data,
                    label=y_label,
                    color=line_colors[j % len(line_colors)],
                    linestyle=line_styles[j % len(line_styles)],
                    marker=markers[j % len(markers)],
                    linewidth=0.5
                )

                ax_col.set_xlabel("Epoch")
                ax_col.set_ylabel(y_axis_column_name)
                ax_col.set_title(y_axis_column_name)

                ax_col.legend()
                ax_col.grid(True, alpha=0.5)

            except FileNotFoundError:
                print(f"File {csv_file} not found")
                continue
            except KeyError as e:
                print(f"Error reading {csv_file}: Column {e} not found. Check column names in the file.")
                continue
            except Exception as e:
                print(f"An unexpected error occurred while processing {csv_file}: {e}")
                continue

    plt.tight_layout(pad=6.0)

    base_image_name = f"{EPOCHS_PATH_STRING}_combined_graphs"
    previous_run_count = count_images_with_pattern("visual/", f"{base_image_name}_*.png")

    plt.savefig(f"visual/{base_image_name}_{previous_run_count + 1}")




# Got this function from AI lol
def count_images_with_pattern(directory_path, filename_pattern, image_extensions=None):
    """
    Counts image files in a directory that match a specific filename pattern.

    Args:
        directory_path (str): The path to the directory to search.
        filename_pattern (str): The shell-style wildcard pattern to match
                                (e.g., '*.png', 'experiment_*.jpg', 'data_??.gif').
        image_extensions (list, optional): A list of image file extensions
                                         to look for (e.g., ['.jpg', '.png']).
                                         Defaults to common extensions if None.

    Returns:
        int: The count of matching image files, or -1 if the directory is not found.
    """
    count = 0

    # Default common image extensions if none are provided
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # Make extensions lowercase for case-insensitive matching
    image_extensions_lower = [ext.lower() for ext in image_extensions]

    try:
        # List all entries (files and subdirectories) in the directory
        entries = os.listdir(directory_path)

        # Iterate through each entry
        for entry_name in entries:
            full_path = os.path.join(directory_path, entry_name)

            # Check if the entry is a file (not a subdirectory)
            if os.path.isfile(full_path):
                # Check if the file extension is one of the image extensions
                # os.path.splitext splits the filename into (root, ext)
                file_extension = os.path.splitext(entry_name)[1].lower() # Get extension and make it lowercase

                if file_extension in image_extensions_lower:
                    # Check if the filename matches the pattern
                    # fnmatch.fnmatch checks if the filename matches the pattern
                    if fnmatch.fnmatch(entry_name, filename_pattern):
                        count += 1

    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory_path}'")
        return -1
    except Exception as e:
        # Catch other potential errors (e.g., permission errors)
        print(f"An error occurred while processing directory '{directory_path}': {e}")
        return -1

    return count

if __name__ == '__main__':
    combine_graphs()
