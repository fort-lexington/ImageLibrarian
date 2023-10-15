import os
import json
import re
import datetime
import exifread
import shutil
import logging
import hashlib

def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

class ImageLibrarian:

    date_pattern = re.compile(r'^(\d\d\d\d)(\d\d)(\d\d)_')

    def __init__(self, init_file):
        self.PREFLIGHT = True
        self.output_root = ''
        self.seed_list = list()
        self.unique_hash = set()
        self.total_size_mb = 0

        with open(init_file, 'r', encoding='utf8') as fh:
            seeds = json.load(fh)
            self.seed_list = seeds['dirs']
            self.output_root = seeds['destination']
            self.image_formats = tuple(seeds.get('format', ['.png','.jpg','.bmp','.mov','.jpeg','.gif','mp4']))
        print(self.seed_list)

    @staticmethod
    def get_created_date(file_path):
        create_time = os.path.getctime(file_path)
        return datetime.datetime.fromtimestamp(create_time)

    @staticmethod
    def get_date_from_name(file_name):
        m = ImageLibrarian.date_pattern.match(file_name)
        if m is None:
            return None

        file_name_date = None
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if m and 1970 < year <= 2030 and 0 < month <= 12 and 0 < day <= 31:
            file_name_date =  datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            logging.info('Found date {0}'.format(file_name_date))
        return file_name_date

    @staticmethod
    def get_exif_date(path_name):
        original_date_time = None
        if path_name.endswith(('.jpeg', '.jpg',)):
            try:
                with open(path_name, 'rb') as f:
                    tags = exifread.process_file(f)
                    dto = tags.get('EXIF DateTimeOriginal')
                    str_dto = str(dto)
                    if re.match(r'\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}', str_dto):
                        original_date_time = datetime.datetime.strptime(str_dto, '%Y:%m:%d %H:%M:%S')
                        logging.info('Found EXIF datetime {0}'.format(original_date_time))
                    elif  re.match(r'\d{2}\.\d{2}.\d{4} \d{2}:\d{2}:\d{2}', str_dto):
                        original_date_time = datetime.datetime.strptime(str_dto, '%m.%d.%Y %H:%M:%S')
                        logging.info('Found EXIF datetime {0}'.format(original_date_time))
            except Exception as err:
                logging.error('EXIF error ', err)
        return original_date_time

    def is_image(self, file_name: str):
        return True if file_name.endswith(self.image_formats) else False

    def walk(self):
        for image_root in self.seed_list:
            print('ROOT: ', image_root)
            self.process_dir(image_root)

    def process_dir(self, path):
        for root, dirs, files in os.walk(path):
            for img in [f for f in files if self.is_image(f)]:
                abs_path = os.path.join(root, img)
                self.process_file(abs_path)

    def is_duplicate(self, abs_path):
        hash = get_sha256(abs_path)
        if hash in self.unique_hash:
            return True
        else:
            self.unique_hash.add(hash)
            return False

    def log_size(self, abs_path):
        file_stats = os.stat(abs_path)
        self.total_size_mb = file_stats.st_size / (1024 * 1024)

    def process_file(self, abs_path):
        logging.debug(abs_path)
        if self.is_duplicate(abs_path):
            logging.info('Duplicate: {0}'.format(abs_path))
            return

        self.log_size(abs_path)

        orig_date = ImageLibrarian.get_exif_date(abs_path)
        file_name_date = ImageLibrarian.get_date_from_name(os.path.basename(abs_path))
        final_created_date = ImageLibrarian.get_created_date(abs_path)

        if orig_date is None:
            final_created_date = ImageLibrarian.get_created_date(abs_path)
        elif file_name_date is not None:
            final_created_date = ImageLibrarian.get_exif_date(abs_path)

        if self.PREFLIGHT:
            return

        destination = self.make_target_dirs(self.output_root, abs_path, final_created_date)
        self.copy_file(abs_path, destination)

    def make_target_dirs(self, target_dir, file_path, date_time: datetime.datetime):
        new_folder = os.path.join(target_dir, '{:0>4}'.format(date_time.year), '{:0>2}'.format(date_time.month), os.path.basename(file_path))
        os.makedirs(os.path.dirname(new_folder), exist_ok=True)
        return new_folder

    def copy_file(self, from_file_path, to_path):
        try:
            shutil.copy2(from_file_path, to_path)
            logging.info('Copied {0} to {1}'.format(from_file_path, to_path))
        except IOError as err:
            logging.error('Unable to copy file {0}'.format(from_file_path))


if __name__ == '__main__':
    log_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.log')
    logging.basicConfig(filename=log_name, level=logging.INFO)

    manager = ImageLibrarian('images.json')
    manager.walk()
    print('Total MB: {0}'.format(manager.total_size_mb))
    print('File Count: {0}'.format(len(manager.unique_hash)))


