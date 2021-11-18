import os
import numpy as np
from analysis_utility import *
from textwrap import wrap
import matplotlib.pyplot as plt
import json
from pathlib import Path

name_file = './names.json'
base_dir = './Response_Data'
base_dir_captions = './caption_json/'
base_path = './Response_Data/Siddharth_2021_s2_exp_'
gt_captions = base_dir_captions + json.load(open(name_file,))['validation_gt']
fig_dir = './figures'
Path(fig_dir).mkdir(parents=True, exist_ok=True)

vid = get_video_id_list(name_file=name_file)
exp_id_list = get_list_of_exp_ids(base_dir)

original_vid = ['v_' + ids + '.mp4' for ids in vid]
original_aud = ['v_' + ids + '.mp3' for ids in vid]
modified_vid = ['v_' + ids + '_pred.mp4' for ids in vid]
modified_aud = ['v_' + ids + '_pred.mp3' for ids in vid]

all_keys = [*original_vid, *original_aud, *modified_vid, *modified_aud]
# Extracted information where keys are still the likert scale options
whole_data_dict = make_whole_data_dictionary(all_keys, exp_id_list, base_path)
demographics_dict = make_demographics_dictionary(exp_id_list, base_path)

# The likert scale options for all the questions
confidence, confusing, match_info_aud, match_info_vid, agree, yes_no = get_likert_categories_wrong_spelling()
modified_aud_questions = [confusing, match_info_aud, agree, agree]
modified_vid_questions = [confusing, match_info_vid, agree, agree]
original_vid_questions = [yes_no]
original_aud_questions = [confidence]
simple_demographic_statistic(demographics_dict)

m_aud_q, m_aud_q_tot, m_aud_all_aud_avg = modified_media_likert_questions(whole_data_dict, modified_aud,
                                                                          modified_aud_questions)
m_vid_q, m_vid_q_tot, m_vid_all_vid_avg = modified_media_likert_questions(whole_data_dict, modified_vid,
                                                                          modified_vid_questions)
o_aud_q, o_aud_q_tot, o_aud_all_aud_avg = original_media_likert_questions(whole_data_dict, original_aud,
                                                                          original_aud_questions)
o_vid_q, o_vid_q_tot, o_vid_all_vid_avg = original_media_likert_questions(whole_data_dict, original_vid,
                                                                          original_vid_questions)

duration, sorted_duration_keys = get_duration_sorted(vid, gt_captions)

descriptive_response = extract_descriptive_answers(all_keys=all_keys, whole_data_dict=whole_data_dict)
write_descriptive_answers_to_file(vid, duration, descriptive_response)

x_l = 'Percentage of Responses'
y_l = 'Run Time of Videos (in seconds)'

plt.pie(m_vid_all_vid_avg[3], labels=modified_vid_questions[3], autopct='%1.1f%%', startangle=270)
plt.savefig('./figures/m_vid_q4.png', dpi=300)
plt.show()

i=3
m_aud_q1_all_normalized_dict = normalized_responses(sorted_duration_keys, duration, modified_aud_questions[i-1], m_aud_q[i-1], '_pred.mp3')
survey(m_aud_q1_all_normalized_dict, modified_aud_questions[i-1], 'RdYlGn', x_l, y_l, reversed=True)
plt.savefig('./figures/m_aud_q3_video-wise.png', dpi=300)
plt.show()
#
m_aud_q1_all_normalized_dict = normalized_responses(sorted_duration_keys, duration, modified_vid_questions[i-1], m_vid_q[i-1], '_pred.mp4')
survey(m_aud_q1_all_normalized_dict, modified_vid_questions[i-1], 'RdYlGn', x_l, y_l, reversed=True)
plt.savefig('./figures/m_vid_q3_video-wise.png', dpi=300)
plt.show()
#
m_aud_q1_all_normalized_dict = normalized_responses(sorted_duration_keys, duration, modified_vid_questions[0], m_vid_q[0], '_pred.mp4')
survey(m_aud_q1_all_normalized_dict, confusing, 'RdYlGn', x_l, y_l, reversed=True)
plt.show()
#
# o_aud_q1_m_aud_q4 = category_wise_connection(whole_data_dict, vid, confidence, agree)
# #
# plot_groped_plot(group_2d_data=o_aud_q1_m_aud_q4, cat1=confidence, cat2=agree, save_str='./figures/oa_ma_14.png')

plot_2_bar(m_aud_all_aud_avg[2], m_vid_all_vid_avg[2], modified_aud_questions[2],
           x_lab='Agreement with ""The descriptions are redundant or have grammar errors.""',
           save_str='./figures/m_q3_both.png')
plot_2_bar(m_aud_all_aud_avg[0], m_vid_all_vid_avg[0], modified_aud_questions[0], x_lab='Confusion in media content',
           save_str='./figures/m_q1_both.png')

l_modified = m_vid_all_vid_avg[1].tolist()
l_modified.append(0.0)
labels = [ '\n'.join(wrap(l, 10)) for l in modified_aud_questions[1]]
plot_2_bar(m_aud_all_aud_avg[1], np.array(l_modified), q_labels=labels,
           x_lab='Level of information matching with the original media.',
           save_str='./figures/m_q2_both.png')

m_vid_q1_m_vid_q2 = category_wise_connection(whole_data_dict, vid, modified_aud_questions[0], modified_aud_questions[2])
plot_groped_plot(group_2d_data=m_vid_q1_m_vid_q2, cat1=modified_aud_questions[0], cat2= modified_aud_questions[2],
                 x_lab= 'Confusion level after watching the modified audio', save_str='./figures/ma_ma_13.png')