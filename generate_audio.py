from gtts import gTTS
import json
import os
from pathlib import Path


def save_tts_mp3(d, rel_path, v_key, caption_type, language):
    num_sentences = len(d['timestamps'])
    for i in range(num_sentences):
        text = d['sentences'][i]
        myobj = gTTS(text=text, lang=language, slow=False)
        save_path = os.path.join(rel_path, v_key + caption_type + str(i)+'.mp3')
        myobj.save(save_path)


def save_audio(name_file, caption_file, rel_save_path, language ='en'):
    # return if the audio files already present
    if os.path.isdir(rel_save_path):
        print("Audio files directory already here!!!")
        return
    f = open(name_file, )
    names = json.load(f)
    video_key = names['video_ids']
    f = open(caption_file,)
    all_captions = json.load(f)
    Path(rel_save_path).mkdir(parents=True, exist_ok=True)
    caption_type = ['_gt_', '_pred_', '_pred_gt_proposals_']
    for key in video_key:
        key = 'v_'+ key
        gt_d = all_captions[key][0]
        pred_d = all_captions[key][1]
        pred_gt_proposals_d = all_captions[key][2]
        save_tts_mp3(gt_d, rel_save_path, key, caption_type[0], language)
        save_tts_mp3(pred_d, rel_save_path, key, caption_type[1], language)
        save_tts_mp3(pred_gt_proposals_d, rel_save_path, key, caption_type[2], language)