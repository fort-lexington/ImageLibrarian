fortlexington@gmail.com
Last Updated: October 13, 2024

# Image Librarian

Take a list of directories containing images, and sorts them into YEAR/MONTH folders using 
a file copy (original images are undisturbed).

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

1. Get the date taken from EXIF data embedded in JPG format (DateTimeOriginal)
2. Look for file names that start with a date stamp matching `YYYYMMDD`
3. Use the file created date

Run by configuring `images.json` and typing the following from the script directory:

```python main.py```

## images.json

**dirs** List of folders that are *recursively* searched.

**destination** Root directory where YYYY\MM folders will be created and files copied.

**format** (Optional) List of file extensions to find. Default is `['.png','.jpg','.gif','mp4']`

### Example

    {
     "dirs": [
       "C:\\Users\\rcmarti1\\OneDrive - Intel Corporation\\Pictures",
       "C:\Users\\rcmarti1\\Desktop\\Photos"
     ],
      "destination": "C:\\_DEV\\images"
    }

## TODO

Take a checksum (hash) of each image to ignore duplicates.
