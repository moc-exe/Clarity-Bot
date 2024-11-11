import os

icon_music = '\U0001F3B5'
icon_img = '\U0001F5BC'
icon_folder = '\U0001F4C1'
icon_file = '\U0001F4C4'
icon_archive = '\U0001F5C4'
curr_root_dir = 'C:/Users/levus/Music'

def build_filetree(root:str)->dict[dict]:
    
    '''walks the filesystem from <root> supplied and creates a dictionary of nested entries as follows: 

        {
        
            'root': {
                'folder1': {
                    'meow_files': ['file1.txt', 'file2.txt'],
                    'folder2': {
                        'meow_files': ['file3.txt']
                    }
                },
                'meow_files': []
            }
        }   
    
    '''
    
    tree = {}

    for path, dirs, files in os.walk(root):
        
        path_chunks = path.split(os.sep)
        curr_level = tree

        for chunk in path_chunks: 
            curr_level = curr_level.setdefault(chunk, {})
        
        curr_level['meow_files'] = files
    
    return tree

def get_icon(filename:str) -> str:     
    
    '''provided with a filename ending with an extension, returns the appropriate unicode icon for the filetype'''

    if filename.lower().endswith(('.mp3', '.flac')):
        return icon_music
    elif filename.lower().endswith(('.zip', '.tar', '.rar')):
        return icon_archive
    elif filename.lower().endswith(('.jpg', '.png', '.webp')):
        return icon_img
    else:
        return icon_file

def print_tree(tree : dict[dict], indent=0) -> str:

    '''builds a filetree string when supplied with a dictionary from the build_filetree(root:str)->dict[dict]'''

    out = ""
    for k, v in tree.items():
        if k == "meow_files":
            for filename in v:
                icon = get_icon(filename)
                out += " " * indent + f"{icon} {filename}\n"
        
        else:
            out += " " * indent + f"{icon_folder} {k}\n"
            out += print_tree(v, indent + 4)
    
    return out

def split_text_by_newlines(text, limit=1800) -> list[str]:

    '''provided with a string, will return a list of strings compliant with discord's max post request payload length'''

    mess_list = []
    curr_message = ""
    
    for line in text.splitlines(keepends=True):  
        # keep newlines at end of each line, check if adding this line would exceed the character limit
        if len(curr_message) + len(line) <= limit:
            curr_message += line
        
        else:
            # if the line exceeds the limit, start a new message
            mess_list.append(curr_message)
            curr_message = line
    
    # append the last message if it still got any content
    if curr_message:
        mess_list.append(curr_message)
    
    return mess_list

def check_is_file_and_size(path: str) -> tuple[bool, str]:
    

    if (path.startswith("'") and path.endswith("'")) or (path.startswith('"') and path.endswith('"')):
        path = path[1:-1]

    if os.path.isfile(path):
        
        file_size = os.path.getsize(path)
        file_size_mb = file_size / (1024 ** 2)
        if file_size_mb < 25:
            return (True, path)
        else:

            return (False, f"The file is too large for upload = {file_size_mb}mb, Discord allows up to 25mb uploads")
    else: 
        return (False, "The path specified is not a file")