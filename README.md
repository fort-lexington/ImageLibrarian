fortlexington@gmail.com
Last Updated: October 13, 2024

# Image Librarian

Take a list of directories containing images, and sorts them into YEAR/MONTH folders using 
a file copy (original images are undisturbed). 

Over time, I found that my many backups of old laptops, SD cards, old phone's internal storage, 
camera SD cards, and so on... had been backed up in a confusing array of folders across multiple drives. 

While _gallery_ apps will allow you to view images as a timeline without actually moving them, 
having images stored in structured folders makes some things easier:

1. Creating a unified backup.
2. Being able to view folders that don't load thousands of thumbnails.
3. Easily upload images from a specified time.

For example, see the following example output folders: 
    
    C:.
    ├───2019
    │   └───12
    ├───2020
    │   ├───01
    │   ├───04
    │   ├───06
    │   ├───07
    │   ├───11
    │   └───12
    ├───2021
    │   ├───03
    │   ├───08
    │   └───09
    ...

There must be a single `images.json` in the same folder as `main.py`.

The strategy to get the date is to:

1. Common date formats in the file name `YYYYMMDD_ or YYYY-MM-DD `.
2. Extract EXIF data embedded in JPG format (DateTimeOriginal)
3. Use the system created date
4. Use the system last modified date
5. If all else fails, use Jan 1, 1970

The script computes a hash of each binary, and will not copy duplicates by comparing with existing
hashes.

A log file is created with the current timestamp as a name. e.g. 20231015_182813.log.

Run by configuring `images.json` and typing the following from the script directory:

```python main.py```

## images.json

**dirs** List of folders that are *recursively* searched. While it is entirely possible to type `/` here, this
will likely result in long run times, and unwanted images. (For a little perspective, my list is about 25 "root" folders
-- which may explain why I needed a script like this).

**destination** The root directory where _YYYY\MM_ folders will be created and files copied.

**format** (Optional) List of file extensions to find. Default is `['.png','.jpg','.bmp','.mov','.jpeg','.gif','mp4']`.

### Example

    {
     "dirs": [
       "/home/ryan/Pictures",
       "/media/ryan/ExtraDrive1/LG G6 Backup",
       "/media/ryan/ExtraDrive1/S10e SD Card Backup"
     ],
      "destination": "C:\\_DEV\\_IMAGES"
    }

