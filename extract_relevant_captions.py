import json


def save_captions(base_dir, name_file, save_file):
    # Opening JSON file
    f = open(name_file, )
    names = json.load(f)

    f_pred = open(base_dir + names['prediction'], )
    f_pred_gt = open(base_dir + names['prediction_gt'], )
    val_gt = open(base_dir + names['validation_gt'], )

    data_pred = json.load(f_pred)
    data_gt = json.load(val_gt)
    data_gt_proposals = json.load(f_pred_gt)['results']

    gen_4915 = data_pred['results']

    video_key = names['video_ids']
    new_d = {}
    for key in video_key:
        key = 'v_' + key
        pred_dict = {}
        l = len(gen_4915[key])
        list_time_stamps = []
        list_sentences = []
        for i in range(l):
            list_time_stamps.append(gen_4915[key][i]['timestamp'])
            list_sentences.append(gen_4915[key][i]['sentence'])
        pred_dict['timestamps'] = list_time_stamps
        pred_dict['sentences'] = list_sentences

        gt_dict = {}
        l = len(data_gt[key]['timestamps'])
        list_time_stamps = []
        list_sentences = []
        for i in range(l):
            list_time_stamps.append(data_gt[key]['timestamps'][i])
            list_sentences.append(data_gt[key]['sentences'][i])
        gt_dict['timestamps'] = list_time_stamps
        gt_dict['sentences'] = list_sentences

        pred_gt_proposal_dict = {}
        starting_point = []
        for i in range(l):
            starting_point.append((data_gt_proposals[key][i]['timestamp'][0]))

        sorted_starting_point_index = sorted(range(len(starting_point)), key=lambda k: starting_point[k])
        list_time_stamps = []
        list_sentences = []

        for i in sorted_starting_point_index:
            list_time_stamps.append(data_gt_proposals[key][i]['timestamp'])
            list_sentences.append(data_gt_proposals[key][i]['sentence'])
        pred_gt_proposal_dict['timestamps'] = list_time_stamps
        pred_gt_proposal_dict['sentences'] = list_sentences

        new_d[key] = [gt_dict, pred_dict, pred_gt_proposal_dict, data_gt[key]['duration']]

    with open(base_dir + save_file, 'w') as fp:
        json.dump(new_d, fp)

