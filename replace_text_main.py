"""
cách sử dụng tool:
- chuẩn bị 1 file csv có 3 row với title như sau:
old, action, status
- và điền thông tin bên dưới theo dạng
old: tên đường dẫn cũ muốn thay đổi
action: tên đường dẫn mới or 'delete'

LƯU Ý: mỗi lần chỉ sài 1 loại HTML tag type trong file csv
VD: giờ ta muốn change all tag <img>
thì trong file csv chỉ nên bao gồm các đường dẫn img
và tag type truyền vào cũng phải là 'img'

- Khi ctrinh chạy xong ta cần quan tâm và đi search log sau:
ERROR
để xem các lỗi nghiêm trọng cần handle bằng tay
"""

import csv
import os
import re
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

csv_file_path = 'C:/Users/Quang Nhu/PycharmProjects/pythonProject/input_folder/input.csv'
folder_need_to_change_path = 'C:/Users/Quang Nhu/PycharmProjects/pythonProject/folder-demo'


def remove_html_tags(data=None, tag_type=None):
    """
    Remove tag in text data input
    :param data: find tag in this data to remove tag
    :param tag_type: tag name need to delete
    :return:

    example: remove_html_tags('<img src='....'>', 'img')
    """

    if tag_type == 'script' or tag_type == 'SCRIPT':
        # init regex object
        # p = re.compile(r'<script(.*)</script>', flags=re.IGNORECASE)
        p = re.compile(r'<script.*?/script>', flags=re.IGNORECASE)

        result = p.sub('', data)  # search regex in data and replace by empty string

        if result == data:  # not found
            # show log lên là: đang search text nào, trên file nào, nhắc xóa bằng tay
            logging.error('<script> not found, '
                          'because </script> xuống dòng,'
                          ' please manual handle by your hands!')
            return False
    else:
        p = re.compile(r'<' + tag_type + '.*?>', flags=re.IGNORECASE)

    return p.sub('', data)


def replace_text_in_files_of_folder(folder_target_path=None, old_text=None, new_text=None, html_tag_type=None):
    """
    find 'old_text' in all files on 'folder_target_path' and replace them by 'new_text'
    :param folder_target_path: will find all files in this folder
    :param old_text: text need to find
    :param new_text: destination text
    :return: void

    example: replace_text_in_files_of_folder('D:/pythonProject/', 'lqnhu', 'lequangnhu')
    """

    logging.debug('-----Tìm \' ' + old_text + ' \' | action: ' + new_text)
    # === for logging====
    count = 0
    files_found = []
    # ===/ for logging====

    # init regex object to search text
    _replace_reg = re.compile(old_text)
    for dirpath, dirnames, filenames in os.walk(folder_target_path):

        # loop to all files in folder
        for file in filenames:
            file = os.path.join(dirpath, file)
            target_txt_file = file + ".txt"
            try:
                with open(target_txt_file, "w") as target:  # open new file to write
                    with open(file, errors="ignore") as source:  # open file to find!
                        for line in source:
                            new_line = _replace_reg.sub(new_text, line)
                            if line != new_line:  # found at this line!
                                if new_text != 'delete':
                                    target.write(new_line)
                                else:
                                    if html_tag_type == 'img' or html_tag_type == 'link':  # action to delete
                                        target.write(remove_html_tags(line, html_tag_type))

                                    elif html_tag_type == 'script' or html_tag_type == 'SCRIPT':
                                        logging.debug('script tag: ' + line)
                                        result = remove_html_tags(line, html_tag_type)
                                        if result != False:
                                            target.write(result)
                                        else: # not found script
                                            logging.debug(old_text + ' not found at file: ' + file)
                                            logging.debug('---------END ROW: '+old_text+'------------')
                                            target.write(line)


                                # === for logging====
                                count += 1
                                files_found.append(file)  # only to show on logging

                            else:  # not found old_text
                                target.write(line)
            finally:
                os.remove(file)  # apply for Windows OS, let's comment this in linux OS
                os.rename(target_txt_file, file)

    if count == 0:
        logging.error('Không tìm thấy bất kỳ file nào. xin check lại!')
        return 'failed'

    # logging.info('Đã tìm thấy ' + str(count) + ' lần và change tại ' + str(len(files_found)) + ' files: ' + files_found)
    logging.info('Đã tìm thấy %s lần và change tại %s files: %s' % (count, len(files_found), files_found))
    return 'ok'


def replace_text_of_folder(csv_file_path, folder_path, html_tag_type):
    """

    :param folder_path:
    :param csv_file_path:
    :param html_tag_type:
    :return:
    """

    # read csv file
    try:
        logging.info('---Init tool------')
        logging.info('---Pre - load csv file---')
        with open(csv_file_path) as csv_file:
            logging.info('Load csv file Success!')
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                logging.debug('----------BEGIN ROW: '+row['old']+'---------------')
                action = row['action']
                old_text = row['old']

                # search text
                replace_text_in_files_of_folder(folder_path, old_text, action, html_tag_type)

    except Exception as e:
        logging.debug('something wrong')
        raise e
    finally:
        logging.info('Tool finished!')


if __name__ == '__main__':
    # p = remove_html_tags('<script src="../jquery/jquery-1.6.1.min.js"><link src="sdas">', 'script')
    replace_text_of_folder(csv_file_path, folder_need_to_change_path, 'script')
    # replace_text_of_folder(csv_file_path, folder_need_to_change_path, 'img')
    # replace_text_of_folder(csv_file_path, folder_need_to_change_path, 'css')
