import os
import shutil


def touch(file_path):
    """
    Create file if not existed.

    Args:
        file_path : str
            File path.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("")
    else :
        raise FileExistsError(f"touch() : File is already existed.\t{file_path}")


def remove(file_path):
    """
    Remove file if existed.

    Args:
        file_path : str
            File path.
    """
    if os.path.exists(file_path):
        try :
            os.remove(file_path)
        except Exception as e :
            raise e
    else :
        raise FileNotFoundError(f"remove() : File is not existed.\t{file_path}")
    

def copy(source, destination, overwrite=False):
    """
    Copy file.

    Args:
        source : str
            Source file path.
        destination : str
            Destination file path.
        overwrite : bool
            Overwrite flag.
    """
    if os.path.exists(source):
        if os.path.exists(destination) and not overwrite:
            raise FileExistsError(f"copy() : Destination file is already existed.\t{destination}")
        try :
            shutil.copyfile(source, destination)
        except Exception as e :
            raise e
    else :
        raise FileNotFoundError(f"copy() : Source file is not existed.\t{source}")


def move(source, destination, overwrite=False):
    """
    Move file.

    Args:
        source : str
            Source file path.
        destination : str
            Destination file path.
        overwrite : bool
            Overwrite flag.
    """
    if os.path.exists(source):
        if os.path.exists(destination) and not overwrite:
            raise FileExistsError(f"move() : Destination file is already existed.\t{destination}")
        try :
            shutil.move(source, destination)
        except Exception as e :
            raise e
    else :
        raise FileNotFoundError(f"move() : Source file is not existed.\t{source}")


def rename(source, destination, overwrite=False):
    """
    Rename file.

    Args:
        source : str
            Source file path.
        destination : str
            Destination file path.
        overwrite : bool
            Overwrite flag.
    """
    if os.path.exists(source):
        if os.path.exists(destination) and not overwrite:
            raise FileExistsError(f"rename() : Destination file is already existed.\t{destination}")
        try :
            os.rename(source, destination)
        except Exception as e :
            raise e
    else :
        raise FileNotFoundError(f"rename() : Source file is not existed.\t{source}")

    
def makedir(dir_path, exist_ok=False):
    """
    Make directory.

    Args:
        dir_path : str
            Directory path.
        exist_ok : bool
            Existence check flag.
    """
    if not os.path.exists(dir_path):
        try :
            os.makedirs(dir_path)
        except Exception as e :
            raise e
    elif not exist_ok :
        raise FileExistsError(f"mkdir() : Directory is already existed.\t{dir_path}")
    

def makedirs(list_dir_path, exist_ok=False):
    """
    Make directories.

    Args:
        list_dir_path : list
            List of directory path.
        exist_ok : bool
            Existence check flag.
    """
    for dir_path in list_dir_path:
        makedir(dir_path, exist_ok)



