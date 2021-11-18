from extract_relevant_captions import save_captions
from download_videos_YT import downloadVidYT
from generate_audio import save_audio
from mmpeg_command_gen import make_bash

name_file = './names.json'
base_dir_captions = './caption_json/'
save_file_extracted_captions = 'extracted_captions.json'
original_video_directory = './Original_Videos'
tts_save_path = './TTS'
modified_video_directory = './Modified_Video'

# extract the relevant captions from the whole validation directories
save_captions(base_dir=base_dir_captions, name_file=name_file, save_file=save_file_extracted_captions)

# download and save the relevant videos from YouTube
downloadVidYT(name_file=name_file, rel_path=original_video_directory)

# convert the captions in to mp3 audio files, default language is English
save_audio(name_file=name_file, caption_file=base_dir_captions+save_file_extracted_captions,
           rel_save_path=tts_save_path)

# making bash files
make_bash(name_file=name_file, caption_file=base_dir_captions+save_file_extracted_captions,
          ori_videos_dir=original_video_directory, tts_dir=tts_save_path, out_dir=modified_video_directory)