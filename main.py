# for read csv files
import csv

# for open and read all folders, files in OS system
import os
import re # regex

# -----------------------------------------

csv_file_path = 'input_folder/input.csv'
folder_need_to_change_path = 'C:/Users/Quang Nhu/PycharmProjects/pythonProject/folder-demo'


def read_csv_file(file_path):
    """
    open csv file and read with specific column
    :param file_path:
    :return: void

    example: read_csv_file('C:/Users/input.csv')
    """
    try:
        print('init tool')
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # let's change columns name to map with your csv files
                print(row['old'], row['new'], row['action'])
    except Exception as e:
        raise e
    finally:
        print('Tool finished!')


def replace_text_in_files_of_folder(folder_target_path=None, old_text=None, new_text=None):
    """
    find 'old_text' in all files on 'folder_target_path' and replace them by 'new_text'
    :param folder_target_path: will find all files in this folder
    :param old_text: text need to find
    :param new_text: destination text
    :return: void

    example: replace_text_in_files_of_folder('D:/pythonProject/', 'lqnhu', 'lequangnhu')
    """

    # init regex object to search text
    _replace_reg = re.compile(old_text)
    for dirpath, dirnames, filenames in os.walk(folder_target_path):

        # loop to all files in folder
        for file in filenames:
            file = os.path.join(dirpath, file)
            target_txt_file = file + ".txt"
            with open(target_txt_file, "w") as target:
                print('target: ' + file)
                with open(file, errors="ignore") as source:
                    print('source: ' + file)
                    for line in source:
                        line = _replace_reg.sub(new_text, line)
                        target.write(line)
            os.remove(file)  # apply for Windows OS, let's comment this in linux OS
            os.rename(target_txt_file, file)


def remove_html_tags(data=None, tag_type=None):
    """
    Remove tag in text data input
    :param data: find tag in this data to remove tag
    :param tag_type: tag name need to delete
    :return:

    example: remove_html_tags('<img src='....'>', 'img')
    """
    p = re.compile(r'<' + tag_type + '.*?>')
    return p.sub('', data)


def remove_img_tags(data):
    """
    Remove image tag in text data input
    :param data:
    :return:
    """

    p = re.compile(r'<img.*?>')  # case not contain '/' on of end tag
    p2 = re.compile(r'<img.*?/>')  # case contain '/' on of end tag
    print(p)
    print(p2)
    return p.sub('', data)


if __name__ == '__main__':
    old_text = '/images/entrysonypoint_300x30.gif'
    new_text = 'lequangnhu'
    replace_text_in_files_of_folder(folder_need_to_change_path, old_text, new_text)

    # read_csv_file(csv_file_path)


# Ph????ng th???c re.compile () c???a Python ???????c s??? d???ng ?????
# bi??n d???ch m???t m???u regex ???????c cung c???p d?????i d???ng chu???i
# th??nh m???t object m???u regex (re.Pattern).
# Sau ????, ch??ng ta c?? th??? s??? d???ng ?????i t?????ng m???u n??y
# ????? t??m ki???m k???t qu??? ph?? h???p b??n trong c??c chu???i m???c ti??u kh??c nhau
# b???ng c??ch s??? d???ng c??c ph????ng th???c regex nh?? re.match () ho???c re.search ().