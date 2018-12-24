import os, time
from PIL import Image, ExifTags


original_directory = DIRECTORY_PATH

def time_convert_file(path):
    m_time = os.path.getmtime(path)
    label = time.strftime('%Y%m%d_%H%M%S', time.gmtime(m_time))
    return(label)

def time_convert_picture(path):
    img = Image.open(picture)
    exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
    pic_time = exif.get('DateTimeOriginal')
    label = pic_time.replace(":", "").replace(" ", "_")
    return(label)

def get_pictures(path):
    all_directories = [x[0] for x in os.walk(path)]

    total_file_list = []
    for directory in all_directories:

        file_list = os.listdir(directory)
        for file_name in file_list:
            if ('.jpg' in file_name.lower()) or ('.JPEG' in file_name.lower()):
                complete_path = directory + '/' + file_name
                total_file_list.append(complete_path)
    return(total_file_list)

def pad_number(original_int, places_int):
    int_str = str(original_int)
    string_length = len(int_str)
    add_str = str('0')
    while string_length < places_int:
        int_str = add_str + int_str
        string_length = len(int_str)
    return(int_str)

def find_last(substring, string):
    loc = string.find(substring)
    while string.find(substring,loc+1) > 0:
        loc = string.find(substring, loc+1 )
    return(loc)

picture_times = {}

total_pictures = get_pictures(original_directory)

for picture in total_pictures:
    try:
        pic_time = time_convert_picture(picture)
    except:
        pic_time = time_convert_file(picture)

    if pic_time in list(picture_times.keys()):
        pic_list = picture_times.get(pic_time)
        pic_list.append(picture)
        picture_times[pic_time]=pic_list
    else:
        picture_times[pic_time]=[picture]

picture_groups = list(picture_times.keys())
ordered_pictures = sorted(picture_groups)

destination_directory = original_directory + '/renamed'
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

for picture_group_name in ordered_pictures:
    picture_list = picture_times.get(picture_group_name)
    pic_count = 1
    for picture_name in sorted(picture_list):
        suffix = picture_name[find_last('.', picture_name):].lower()
        picture_rename = destination_directory + picture_group_name + '_' + pad_number(pic_count, 3) + suffix
        os.rename(picture_name, picture_rename)
        print(picture_name + ' moved to ' + destination_directory + picture_rename)
        pic_count +=1








