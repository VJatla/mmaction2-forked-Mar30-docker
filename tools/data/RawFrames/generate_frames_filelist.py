"""
Description
-----------
Generates a text file containing RawFrameDataset information as required by
mmaction2 library.

Example
-------
```
```
"""
import os
import sys
import pdb
import argparse
import random
from argparse import RawTextHelpFormatter


description = ("""
Description:
  Generates a text file containing RawFrameDataset information as required by
  mmaction2 library.
""")


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(description),
                                        formatter_class=RawTextHelpFormatter)

    # Adding arguments
    args_inst.add_argument("rfrm_dir", type=str, help=("Directory containing raw frames"))
    args_inst.add_argument("ctxt", type=str, help=("Text file containing class indexes"))
    args_inst.add_argument("otxt", type=str, help=("output text file path"))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'rfrm_dir': args.rfrm_dir,
                 'ctxt': args.ctxt,
                 'otxt': args.otxt}

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict

def check_if_dir_exists(directory_path):
    """
    If file does not exists it raises an exception

    Parameters
    ----------
    directory_path : str
        Full path of directory
    """
    if not os.path.isdir(directory_path):
        raise Exception(f"The directory does not exist,\n\t{directory_path}")

def check_if_file_exists(file_path):
    """
    If file does not exists it raises an exception

    Parameters
    ----------
    file_path : str
        Full path to file
    """
    if not os.path.isfile(file_path):
        raise Exception(f"The file does not exist,\n\t{file_path}")


def get_files_with_kws(loc, kws):
    """
    Lists full paths of files having certian keywords in their names

    Parameters
    ----------

    loc : str
    Path to the root directory containing files.
    kws : list of str
    List of key words the files have
    """
    # Check if directory is valid
    if not (os.path.exists(loc)):
        raise Exception(f"The path {loc} is not valid.")

    # create a list using comma separated values
    kw_lst_csv = []
    for idx, litem in enumerate(kws):
        litem_split = litem.split(",")
        if len(litem_split) > 1:
            kw_lst_csv = kw_lst_csv + litem_split
        else:
            kw_lst_csv.append(litem_split[0])

    # Loop through each file
    files = []
    for r, d, f in os.walk(loc):
        for file in f:
            # Break comma separated values
            # Check if current file contains all of the key words
            is_valid_file = all(kw in file for kw in kw_lst_csv)
            if is_valid_file:
                files.append(os.path.join(r, file))

    # return
    return files



def main():
    """Main function."""
    argd = _arguments()
    rawframes_dir = argd['rfrm_dir']
    annotations_file = argd['ctxt']
    otxt = argd['otxt']

    # Check for annotations and rawframes directories
    check_if_dir_exists(rawframes_dir)
    check_if_file_exists(annotations_file)

    # Load annotations as dictionary
    with open(annotations_file, "r") as f:
        ann_list = f.readlines()
    
    ann_idxs = []
    ann_labels = []
    for ann in ann_list:
        ann = ann.rstrip().split(" ")
        if len(ann) > 2:
            raise Exception(f"Annotation is not valid {ann}")
        ann_idx, ann_label = ann
        ann_idxs  += [int(ann_idx) - 1] #  index starts from 0
        ann_labels += [ann_label]

    # If maximum classes > number of entries then we have a problem
    max_idx = max(ann_idxs)
    if max_idx > len(ann_labels):
        raise Exception(
            f"Maximum index is {max_idx},"
            f" while number of classes are {len(ann_class)}"
        )

    # Loop through each class label and get rawframe instance
    # names
    rlist = []
    for i, ann_label in enumerate(ann_labels):
        ann_label_fpth = f"{rawframes_dir}/{ann_label}"
        check_if_dir_exists(ann_label_fpth)

        rawframe_dirs = os.listdir(ann_label_fpth)

        for crawframe_dir in rawframe_dirs:
            cdir = f"{ann_label_fpth}/{crawframe_dir}"

            imgs = get_files_with_kws(cdir, ["img_"])
            nfrms = len(imgs)

            rlist += [
                f"{ann_label}/{crawframe_dir} {nfrms} {ann_idxs[i]}"
            ]
            
    # Shuffle
    random.shuffle(rlist)
    
    # Write to text file
    with open(otxt, 'w') as f:
        f.writelines("%s\n" %r for r in rlist)

# Execution starts here
if __name__ == "__main__":
    main()
