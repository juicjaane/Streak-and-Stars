from PIL import Image
from PIL.TiffTags import TAGS_V2

def extract_metadata_from_tiff(tiff_file_path):
    try:
        # Open the TIFF file
        with Image.open(tiff_file_path) as img:
            # TIFF metadata is stored as tags
            metadata = img.tag_v2
            if metadata:
                for tag, value in metadata.items():
                    tag_name = TAGS_V2.get(tag, tag)
                    print(f"Tag: {tag_name}, Value: {value}")
            else:
                print("No metadata found.")
    except Exception as e:
        print(f"Error: {e}")

        
tiff_file_path = r"C:\Users\thooy\Downloads\Datasets_Assessment\Datasets\Raw_Images\Raw_Observation_025_Set3.tiff"
extract_metadata_from_tiff(tiff_file_path)
