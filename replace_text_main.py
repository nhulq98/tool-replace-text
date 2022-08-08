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
from cgitb import html

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

csv_file_path = '/home/nhulq/Desktop/shutto/tool-replace-text/input_folder/input.csv'
csv_file_path_test = '/home/nhulq/Desktop/shutto/tool-replace-text/input_folder/input_test.csv'
csv_file_output_path = '/home/nhulq/Desktop/shutto/tool-replace-text/output_folder/output.csv'
folder_need_to_change_path = '/home/nhulq/Desktop/airtrip/skygserv/web'


# html_tag_dict = {
#     'SCRIPT': 'script',
#     'IMG': 'img',
#     'link': 'link'
# }

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
        # regexObject = re.compile(r'<script(.*)</script>', flags=re.IGNORECASE)
        regex_object = re.compile(r'<script.*?/script>', flags=re.IGNORECASE)

        result = regex_object.sub('', data)  # search regex in data and replace by empty string

        if result == data:  # not found
            # show log lên là: đang search text nào, trên file nào, nhắc xóa bằng tay
            logging.error('Không thể xóa vì không tìm thấy thẻ </script>, '
                          'Vì có thể thẻ </script> được xuống dòng,'
                          ' Hãy xử lý bằng tay!')
            return False
    else:
        regex_object = re.compile(r'<' + tag_type + '.*?>', flags=re.IGNORECASE)

    return regex_object.sub('', data)  # remove tag type


def replace_text_in_files_of_folder(folder_target_path=None, old_text=None, new_text=None, html_tag_type=None):
    """
    find 'old_text' in all files on 'folder_target_path' and replace them by 'new_text'
    :param folder_target_path: will find all files in this folder
    :param old_text: text need to find
    :param new_text: destination text
    :return: void

    example: replace_text_in_files_of_folder('D:/pythonProject/', 'lqnhu', 'lequangnhu')
    """

    logging.debug('Tìm \'' + old_text + '\' | action: \'' + new_text + '\'')
    log_count_number_found_old_text = 0
    log_found_files_list = []
    log_count_number_changed = 0
    log_number_sucess = 0
    log_number_failed = 0

    # init regex object to search text
    _replace_reg = re.compile(old_text)
    for dir_path, dir_names, file_names in os.walk(folder_target_path):


        # loop to all files in folder
        for file in file_names:
            is_found = False
            if file.endswith(".jsp") or file.endswith(".vm"):
                file = os.path.join(dir_path, file)  # concat filename to path (/home/nhulq/index.html)
                target_txt_file = file + ".txt"
                try:
                    with open(target_txt_file, "w", encoding="shift-jis") as target_file:  # open new file to write
                        with open(file, errors="ignore", encoding="shift-jis") as source_file:  # open file in OS to find old_text!
                            # loop each line in current file
                            for line_text in source_file:
                                find_result = line_text.find(old_text)

                                # line_is_changed = _replace_reg.sub(new_text,
                                #                                    line_text)  # return text (find and replace old_text become new_text in line)
                                # if line_text != line_is_changed:  # found at current line!
                                if find_result != -1: # rewrite file
                                    is_found = True
                                    logging.debug('Đã tìm thấy: \'' + old_text + '\' tại file: ' + file)
                                    log_count_number_found_old_text += 1
                                    log_found_files_list.append(file)

                                    if new_text != 'delete':
                                        result_replace = line_text.replace(old_text, new_text)
                                        target_file.write(result_replace)

                                        logging.debug('Change thành công')
                                        log_count_number_changed += 1
                                    else:
                                        if html_tag_type == 'img' or html_tag_type == 'link':  # action to delete
                                            target_file.write(remove_html_tags(line_text, html_tag_type))

                                            logging.debug('Xóa thành công thẻ: ' + html_tag_type)
                                            log_count_number_changed += 1

                                        elif html_tag_type == 'script' or html_tag_type == 'SCRIPT':
                                            result = remove_html_tags(line_text, html_tag_type)
                                            if result != False:
                                                target_file.write(result)

                                                logging.debug('Xóa thành công thẻ: ' + html_tag_type)
                                                log_count_number_changed += 1
                                            else:  # can't delete whole script tag, because not found </script> tag
                                                logging.debug('Script tag failed: ' + line_text)
                                                logging.debug('Xóa thất bại thẻ ' + html_tag_type + ' tại file: ' + file)
                                                log_number_failed += 1

                                                target_file.write(line_text)

                                else:  # not found old_text
                                    target_file.write(line_text)

                finally:
                    if is_found == False:
                        os.remove(target_txt_file)# remove file not contain old_text
                    else:
                        os.remove(file)  # apply for Windows OS, let's comment this in linux OS
                        os.rename(target_txt_file, file)


    if log_count_number_found_old_text == 0:
        logging.error('Không tìm thấy bất kỳ file nào. xin check lại!')
        log_number_failed += 1

    # remove duplicate files because have exists change > 1 in 1 file

    logging.info('Result(failed: %s | success: %s): '
                 'Đã tìm thấy %s lần và change %s lần, tại %s files: %s' % (
                     log_number_failed, log_count_number_changed,
                     log_count_number_found_old_text, log_count_number_changed, len(set(log_found_files_list)),
                     set(log_found_files_list)))
    if log_number_failed > 0:
        return 'failed'

    return 'ok'


def replace_text_of_folder(csv_file_path, folder_path, html_tag_type):
    """

    :param folder_path:
    :param csv_file_path:
    :param html_tag_type:
    :return:
    """

    try:
        logging.info('---Init tool------')
        logging.info('---Pre - load csv file---')
        with open(csv_file_output_path, 'w', newline='') as csvfile:  # open file to write
            fieldnames = ['old', 'action', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            with open(csv_file_path) as csv_file:  # open file to read
                logging.info('Load csv file Success!')

                log_row_count = 1

                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    logging.debug('----------BEGIN ROW %s: %s---------------' % (log_row_count, row['old']))

                    action = row['action']  # [delete, new_text]
                    old_text = row['old']

                    status = replace_text_in_files_of_folder(folder_path, old_text, action, html_tag_type)

                    # write to csv_output
                    writer.writerow({'old': old_text, 'action': action, 'status': status})

                    logging.debug('---------END ROW: ' + old_text + '------------')
                    log_row_count += 1

    except Exception as e:
        logging.error('Something wrong')
        raise e
    finally:
        logging.info('Tool finished!')


if __name__ == '__main__':
    # p = remove_html_tags('<link rel="stylesheet" href="/css/common.css" media="screen"> '
    #                      '<link rel="stylesheet" href="/css/cc.css" media="screen">'
    #                      '<link rel="stylesheet" href="/css/cs.css" media="screen">', 'link')
    # replace_text_of_folder(csv_file_path, folder_need_to_change_path, 'script')
    # replace_text_of_folder(csv_file_path, folder_need_to_change_path, 'img')
    replace_text_of_folder(csv_file_path_test, folder_need_to_change_path, 'link')
