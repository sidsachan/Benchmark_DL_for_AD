from extract_relevant_captions import save_captions
from download_videos_YT import downloadVidYT

name_file = './names.json'
base_dir_captions = './caption_json/'
save_file_extracted_captions = 'extracted_captions.json'
original_video_directory = './Original_Videos'

# extract the relevant captions from the whole validation directories
save_captions(base_dir=base_dir_captions, name_file=name_file, save_file=save_file_extracted_captions)

# download and save the relevant videos from YouTube
downloadVidYT(name_file=name_file, rel_path=original_video_directory)