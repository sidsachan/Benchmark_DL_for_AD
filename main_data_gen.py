from extract_relevant_captions import save_captions
from download_videos_YT import downloadVidYT
from generate_audio import save_audio
from mmpeg_command_gen import make_bash_modified_video, extract_audio
from pathlib import Path
import os


name_file = './names.json'
base_dir_captions = './caption_json/'
save_file_extracted_captions = 'extracted_captions.json'
original_video_directory = './Original_Video'
tts_save_path = './TTS'
modified_video_directory = './Modified_Video'
modified_audio_directory = './Modified_Audio'
original_audio_directory = './Original_Audio'

# extract the relevant captions from the whole validation directories
save_captions(base_dir=base_dir_captions, name_file=name_file, save_file=save_file_extracted_captions)

# download and save the relevant videos from YouTube
downloadVidYT(name_file=name_file, rel_path=original_video_directory)

# convert the captions in to mp3 audio files, default language is English
save_audio(name_file=name_file, caption_file=base_dir_captions+save_file_extracted_captions,
           rel_save_path=tts_save_path)

# making bash file for adding audio to original video
make_bash_modified_video(name_file=name_file, caption_file=base_dir_captions + save_file_extracted_captions,
                         ori_videos_dir=original_video_directory, tts_dir=tts_save_path, modified_vid_dir=modified_video_directory)

# making bash file for extracting audio from original and modified videos
extract_audio(name_file=name_file, ori_videos_dir=original_video_directory, modified_vid_dir=modified_video_directory)

# making the additional directories
Path(modified_audio_directory).mkdir(parents=True, exist_ok=True)
Path(modified_video_directory).mkdir(parents=True, exist_ok=True)
Path(original_audio_directory).mkdir(parents=True, exist_ok=True)

# running the bash files from python
os.system('bash run_from_bash.sh')
os.system('bash extract_modified.sh')
os.system('bash extract_original.sh')