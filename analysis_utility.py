import os
import numpy as np
import json
import matplotlib.pyplot as plt
import sys


def get_list_of_exp_ids(base_dir):
    exp_id_list = []
    for path in os.listdir(base_dir):
        if "S_S" in path:
            continue
        if (len(path) == 28):
            exp_id_list.append(path[-6:-4])
        else:
            exp_id_list.append(path[-7:-4])
    return exp_id_list


def get_video_id_list(name_file):
    f = open(name_file, )
    names = json.load(f)
    video_key = names['video_ids']
    return video_key


def get_duration_sorted(vid, json_file_loc):
    val_1_gt = open(json_file_loc, )
    data_gt = json.load(val_1_gt)

    duration = {}
    for key in vid:
        key = 'v_' + key
        duration[key] = str(data_gt[key]['duration'])

    duration = {k: v for k, v in sorted(duration.items(), key=lambda item: item[1])}
    sorted_duration_keys = list(duration.keys())
    return duration, sorted_duration_keys


def get_likert_categories_wrong_spelling():
    confidence = ['Not confident at all', 'A little confident', 'Moderately confident', 'Quite confident',
                  'Extremely confident']
    confusing = ['Not confusing at all', 'Somewhat confusing', 'Moderately confusing', 'Qiute confusing',
                 'Extremely confusing']
    match_info_aud = ['No match at all', 'A little bit matching', 'Moderately matching', 'Quite well matching',
                      'Extemetly well match', 'Not sure']
    match_info_vid = ['No match at all', 'A little bit matching', 'Moderately matching', 'Quite well matching',
                      'Extemetly well match']
    agree = ['Strongly Agree', 'Agree', 'Undecided', 'Disagree', 'Strongly disagree']
    yes_no = ['Yes', 'No']

    return confidence, confusing, match_info_aud, match_info_vid, agree, yes_no


def make_whole_data_dictionary(all_keys, exp_id_list, base_path):
    whole_data_dict = dict.fromkeys(all_keys, None)
    for exp_id in exp_id_list:
        full_path = base_path + str(exp_id) + '.txt'
        file1 = open(full_path, 'r')
        Lines = file1.readlines()
        last_line = len(Lines)
        for line_num in range(15, last_line):
            split1 = Lines[line_num].split(';')
            if "v_" in split1[0]:
                main_content = split1[3]
                questions = main_content.split('|')
                num_questions = len(questions)
                l = [exp_id]
                for q in questions:
                    q_split = q.split(':')
                    if len(q_split) == 2:
                        l.append(q_split[1].strip())
                # Logic to add text entered in the descriptive answers-> when it go to next line
                extra_text = ''
                flag = True
                counter = 1
                while (flag):
                    if line_num + counter >= last_line:
                        flag = False
                    elif "v_" in Lines[line_num + counter].split(';')[0]:
                        flag = False
                    else:
                        extra_text = extra_text + '.' + Lines[line_num + counter].split('|')[0].split(';')[0].strip()
                        counter = counter + 1
                l[-1] = l[-1] + extra_text
                # Append the responses on to appropriate
                if whole_data_dict[split1[0]] is None:
                    list_of_lists = [l]
                    whole_data_dict[split1[0]] = list_of_lists
                else:
                    whole_data_dict[split1[0]].append(l)
    return whole_data_dict


def make_demographics_dictionary(exp_id_list, base_path):
    demographics_dict = {}
    for exp_id in exp_id_list:
        full_path = base_path + str(exp_id) + '.txt'
        file1 = open(full_path, 'r')
        lines = file1.readlines()
        demo_g = lines[13].split('|')
        age = demo_g[0].split(':')[2]
        gender = demo_g[1].split(':')[1]
        primary_lan = demo_g[2].split(':')[1]
        exp_AD = demo_g[3].split(':')[1]
        demographics_dict[exp_id] = [age, gender, primary_lan, exp_AD]
    return demographics_dict


def simple_demographic_statistic(demographics_dict):
    ages = []
    genders = [0, 0]
    for key in demographics_dict:
        ages.append(int(demographics_dict[key][0]))
        if demographics_dict[key][1] == 'female':
            genders[0] = genders[0] + 1
        elif demographics_dict[key][1] == 'male':
            genders[1] = genders[1] + 1
    print('Average age', np.mean(ages))
    print('Number of Female Participants:', genders[0])
    print('Number of Male Participants:', genders[1])


def modified_media_likert_questions(whole_data_dict, modified_media_dict, question_type_list):
    q1 = dict.fromkeys(modified_media_dict, None)
    q2 = dict.fromkeys(modified_media_dict, None)
    q3 = dict.fromkeys(modified_media_dict, None)
    q4 = dict.fromkeys(modified_media_dict, None)
    q1_tot = dict.fromkeys(modified_media_dict, None)
    q2_tot = dict.fromkeys(modified_media_dict, None)
    q3_tot = dict.fromkeys(modified_media_dict, None)
    q4_tot = dict.fromkeys(modified_media_dict, None)

    for key in modified_media_dict:
        l_q1 = [0] * len(question_type_list[0])
        l_q2 = [0] * len(question_type_list[1])
        l_q3 = [0] * len(question_type_list[2])
        l_q4 = [0] * len(question_type_list[3])
        for l in whole_data_dict[key]:
            l_q1[question_type_list[0].index(l[1])] += 1
            l_q2[question_type_list[1].index(l[2])] += 1
            l_q3[question_type_list[2].index(l[3])] += 1
            l_q4[question_type_list[3].index(l[4])] += 1
        q1[key] = l_q1
        q2[key] = l_q2
        q3[key] = l_q3
        q4[key] = l_q4
        q1_tot[key] = len(l_q1)
        q2_tot[key] = len(l_q2)
        q3_tot[key] = len(l_q3)
        q4_tot[key] = len(l_q4)

    q1_all_media_avg = np.zeros(len(question_type_list[0]))
    q2_all_media_avg = np.zeros(len(question_type_list[1]))
    q3_all_media_avg = np.zeros(len(question_type_list[2]))
    q4_all_media_avg = np.zeros(len(question_type_list[3]))

    for key in modified_media_dict:
        q1_all_media_avg += np.array(q1[key])
        q2_all_media_avg += np.array(q2[key])
        q3_all_media_avg += np.array(q3[key])
        q4_all_media_avg += np.array(q4[key])
    return [[q1, q2, q3, q4], [q1_tot, q2_tot, q3_tot, q4_tot], [q1_all_media_avg, q2_all_media_avg, q3_all_media_avg, q4_all_media_avg]]


def original_media_likert_questions(whole_data_dict, original_media_dict, question_type_list):
    q1 = dict.fromkeys(original_media_dict, None)
    q1_tot = dict.fromkeys(original_media_dict, None)

    for key in original_media_dict:
        l_q1 = [0] * len(question_type_list[0])
        for l in whole_data_dict[key]:
            l_q1[question_type_list[0].index(l[1])] += 1
        q1[key] = l_q1
        q1_tot[key] = len(l_q1)

    q1_all_media_avg = np.zeros(len(question_type_list[0]))
    for key in original_media_dict:
        q1_all_media_avg += np.array(q1[key])

    return [[q1], [q1_tot], [q1_all_media_avg]]


def normalized_responses(sorted_duration_keys, duration, question_type, q_dict, end_str):
    """
    Params
    sorted_duration_keys: list of vids sorted w.r.t. the duration (low to high)
    duration: duration is set as the key in the output instead of the vid used everywhere
    question_type: the list of questions options (the likert scale options), length needed
    q_dict: The dictionary which holds the responses to a particular question
    end_str: _pred.mp3, _pred.mp4 -> the additional part in the q_dict keys
    Returns
    media_wise_normalized_responses_dict : a dictionary with #vids keys and each key has a list of
    normalized number of responses. Also the dictionary is filled in increasing order, so as to get
    nice property when plotting (top-bottom follows low to high time)
    """
    media_wise_responses = np.zeros((len(sorted_duration_keys), len(question_type)))
    for i in range(len(sorted_duration_keys)):
        media_wise_responses[i, :] = q_dict[sorted_duration_keys[i] + end_str]

    media_wise_normalized_responses = 100 * (media_wise_responses / np.sum(media_wise_responses, axis=1, keepdims=True))

    media_wise_responses_dict = {}
    media_wise_normalized_responses_dict = {}
    i = 0
    for key in sorted_duration_keys:
        media_wise_responses_dict[str(duration[key])] = media_wise_responses[i, :]
        media_wise_normalized_responses_dict[str(duration[key])] = media_wise_normalized_responses[i, :]
        i += 1
    return media_wise_normalized_responses_dict


def category_wise_connection(whole_data_dict, vid, cat1, cat2):
    size = (len(cat1), len(cat2))
    category_wise_res = np.zeros(size)

    for key in vid:
        o_key = 'v_' + key + '_pred.mp3'
        m_key = 'v_' + key + '_pred.mp3'
        o_list = whole_data_dict[o_key]
        m_list = whole_data_dict[m_key]
        num_reponses = len(o_list)
        for i in range(num_reponses):
            if i < len(m_list):
                category_wise_res[cat1.index(o_list[i][1])][cat2.index(m_list[i][3])] += 1

    return category_wise_res


def survey(results, category_names, colormap_str, x_l, y_l, reversed = False):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    if reversed:
        category_colors = plt.get_cmap(colormap_str).reversed()(
            np.linspace(0.15, 0.85, data.shape[1]))
    else:
        category_colors = plt.get_cmap(colormap_str)(
            np.linspace(0.15, 0.85, data.shape[1]))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(True)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
#         for y, (x, c) in enumerate(zip(xcenters, widths)):
#             ax.text(x, y, str(int(c)), ha='center', va='center',
#                     color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0.06, 1),
              loc='lower left', fontsize='small')

    ax.set_xticks([i for i in np.arange(0,110,10)], minor=False)
    ax.set_xlabel(x_l, fontsize=15)
    ax.set_ylabel(y_l, fontsize=15)
    return fig, ax


def plot_groped_plot(group_2d_data, cat1, cat2, x_lab, save_str):
    barWidth = 0.15
    plt.figure(figsize=(11, 6))

    # Set position of bar on X axis
    r1 = np.arange(len(group_2d_data[:, 0]))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]

    # Make the plot
    plt.bar(r1, group_2d_data[:, 0], color='k', width=barWidth, edgecolor='white', label=cat2[0])
    plt.bar(r2, group_2d_data[:, 1], color='g', width=barWidth, edgecolor='white', label=cat2[1])
    plt.bar(r3, group_2d_data[:, 2], color='r', width=barWidth, edgecolor='white', label=cat2[2])
    plt.bar(r4, group_2d_data[:, 3], color='b', width=barWidth, edgecolor='white', label=cat2[3])
    plt.bar(r5, group_2d_data[:, 4], color='y', width=barWidth, edgecolor='white', label=cat2[4])

    # Add xticks on the middle of the group bars
    plt.xlabel(x_lab, fontweight='bold')
    plt.ylabel('Number of responses', fontweight='bold')
    plt.xticks([r + 2 * barWidth for r in range(len(cat1))], cat1)

    # Create legend & Show graphic
    plt.legend(bbox_to_anchor=(0.95, 1.1), ncol=5)
    plt.savefig(save_str, dpi=300)
    plt.show()


def plot_2_bar(bar1, bar2, q_labels, x_lab, save_str):
    # set width of bars
    barWidth = 0.25
    plt.figure(figsize=(10, 7))
    bar1 = 100*bar1/np.sum(bar1)
    bar2 = 100*bar2/np.sum(bar2)
    # Set position of bar on X axis
    r1 = np.arange(len(bar1))
    r2 = [x + barWidth for x in r1]

    # Make the plot
    plt.bar(r1, bar1, color = 'r', width = barWidth, edgecolor = 'white', label = 'Modified Audio')
    plt.bar(r2, bar2, color = 'g', width = barWidth, edgecolor = 'white', label = 'Modified Video')

    # Add xticks on the middle of the group bars
    plt.xlabel(x_lab, fontweight='bold')
    plt.ylabel('Percentage of responses', fontweight='bold')
    plt.xticks([r+barWidth/2 for r in range(len(q_labels))], q_labels)

    # Create legend & Show graphic
    plt.legend(bbox_to_anchor=(0.7, 1.1), ncol=2)
    plt.savefig(save_str, dpi=300)
    plt.show()


def extract_descriptive_answers(all_keys, whole_data_dict):
    descriptive = dict.fromkeys(all_keys, None)

    for key in whole_data_dict.keys():
        l = whole_data_dict[key]
        l2 = []
        for res in l:
            l2.append(res[-1])
        descriptive[key] = l2
    return descriptive


def write_descriptive_answers_to_file(vid, duration, descriptive):
    sys.stdout = open("descriptive_responses.txt", "w")

    for ids in vid:
        dkey = 'v_' + ids
        key1 = dkey + '.mp3'
        key2 = dkey + '.mp4'
        key3 = dkey + '_pred.mp3'
        key4 = dkey + '_pred.mp4'
        print(dkey, ':-', duration[dkey])
        print(descriptive[key1], '\n')
        print(descriptive[key2], '\n')
        print(descriptive[key3], '\n')
        print(descriptive[key4], '\n', '\n')
    sys.stdout.close()
