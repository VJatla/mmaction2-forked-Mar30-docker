"""
Description
-----------

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
Description
-----------
""")


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(description),
                                        formatter_class=RawTextHelpFormatter)

    # Adding arguments
    args_inst.add_argument("rdir", type=str, help=("Root directory having videos and annotations"))
    args_inst.add_argument("vext", type=str, help=("Video extension. Typically mp4 or avi"))
    args_inst.add_argument("otxt", type=str, help=("output text file path"))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'rdir': args.rdir,
                 'vext': args.vext,
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
    rdir = argd['rdir']
    vext = argd['vext']
    otxt = argd['otxt']

    # Check for annotations directory and videos directory at rdir
    videos_dir      = f"{rdir}/videos"
    annotations_file = f"{rdir}/annotations/classInd.txt"
    check_if_dir_exists(videos_dir)
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
        ann_idxs  += [int(ann_idx)]
        ann_labels += [ann_label]

    # If maximum classes > number of entries then we have a problem
    max_idx = max(ann_idxs)
    if max_idx > len(ann_labels):
        raise Exception(
            f"Maximum index is {max_idx},"
            f" while number of classes are {len(ann_class)}"
        )

    # Get full paths having videos
    vpaths = get_files_with_kws(videos_dir, [f".{vext}"])

    # Create a list from vlist having `Classname/videoname` entries
    vlist = []
    for vpath in vpaths:
        vclass = vpath.split('/')[-2]
        vname = vpath.split('/')[-1]

        # Class index
        class_idx = ann_labels.index(vclass)
        
        vlist += [f"{vclass}/{vname} {class_idx}"]


    # Shuffle
    random.shuffle(vlist)
    
    # Write to text file
    with open(otxt, 'w') as f:
        f.writelines("%s\n" %v for v in vlist)

    
    
    


# Execution starts here
if __name__ == "__main__":
    main()
