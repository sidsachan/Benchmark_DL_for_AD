import json

def combine_adelay_strings(adelay_strings):
    out = ''
    combine_part = '[0]'
    for i in range(len(adelay_strings)):
        out = out + adelay_strings[i]
        combine_part = combine_part + '[' + 'aud' + str(i + 1) + ']'

    out = '\"' + out + combine_part + 'amix=' + str(len(adelay_strings) + 1) + '\"'
    return out


def combine_video_audio_input(v_dir, aud_dir_list):
    out = 'ffmpeg -i '
    out = out + v_dir
    for i in range(len(aud_dir_list)):
        out = out + ' -i ' + aud_dir_list[i]
    return out + ' '


def make_bash(name_file, caption_file, ori_videos_dir, tts_dir, out_dir):
    ori_videos_dir = ori_videos_dir + '/v_'
    tts_dir = tts_dir + '/v_'
    out_dir = out_dir + '/v_'
    all_captions = json.load(open(caption_file, ))
    f = open(name_file, )
    names = json.load(f)
    video_key = names['video_ids']
    tts_type = ['_gt', '_pred', '_pred_gt_proposals']
    index_type = 1
    filter_part = ' -filter_complex '
    bash_file = open('run_from_bash.sh', 'w')
    bash_file.write('#!/bin/bash\n')
    duration = 0
    for vid in video_key:
        vid_input = ori_videos_dir + vid + '.mp4'
        out_path = out_dir + vid + tts_type[index_type] + '.mp4'
        num_sentences = len(all_captions['v_' + vid][index_type]['timestamps'])
        duration = duration + all_captions['v_' + vid][3]
        aud_input = []
        start_time = []
        for i in range(num_sentences):
            start_time.append(all_captions['v_' + vid][index_type]['timestamps'][i][0] * 1000)
        adelay_strings = []
        for i in range(num_sentences):
            aud_input.append(tts_dir + vid + tts_type[index_type] + '_' + str(i) + '.mp3')
            adelay_string = '[' + str(i + 1) + ']adelay=' + str(start_time[i]) + '|' + str(
                start_time[i]) + '[' + 'aud' + str(i + 1) + '];'
            adelay_strings.append(adelay_string)
        s1 = combine_video_audio_input(vid_input, aud_input)
        s2 = combine_adelay_strings(adelay_strings)
        s3 = s1 + '-filter_complex ' + s2 + ' -c:v copy ' + out_path + '\n'
        bash_file.write(s3)

    bash_file.close()
    average_duration = duration / len(video_key)

    # Extract original video's audio
    bash_file = open('extract_original.sh', 'a')
    original_aud = './Original_Audio/v_'

    for vid in video_key:
        s = 'ffmpeg -i ' + ori_videos_dir + vid + '.mp4 -map 0:a -c copy '+ original_aud+vid+'.aac\n'
        bash_file.write(s)
    bash_file.close()

    # Extract modified video's audio
    modified_aud = './Modified_Audio/v_'
    bash_file = open('extract_modified.sh', 'a')

    for vid in video_key:
        s = 'ffmpeg -i ' + out_dir + vid + '_pred.mp4 -map 0:a -c copy '+ modified_aud+vid+'.aac\n'
        bash_file.write(s)
    bash_file.close()
