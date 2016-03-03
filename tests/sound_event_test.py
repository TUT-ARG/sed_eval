#!/usr/bin/env python

import sed_eval

#file_list = [
#    {'reference_file': 'data/sound_event/office_snr0_med_v2.txt',  'estimated_file': 'data/sound_event/office_snr0_med_v2_detected.txt'},
#    {'reference_file': 'data/sound_event/office_snr0_high_v2.txt', 'estimated_file': 'data/sound_event/office_snr0_high_v2_detected.txt'},
#]

file_list = [
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr0_high_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr0_high_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr0_low_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr0_low_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr0_med_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr0_med_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr-6_high_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr-6_high_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr-6_low_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr-6_low_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr-6_med_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr-6_med_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr6_high_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr6_high_out.txt'
    }, 
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr6_low_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr6_low_out.txt'
    },
    {
     'reference_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr6_med_v2.txt',  
     'estimated_file': '/share/argdata/mesaros/DCASE2013_experiment/office_snr6_med_out.txt'
    },                             
]


data = []
all_data = sed_eval.util.event_list.EventList()
for file_pair in file_list:
    reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
    estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
    data.append({'reference_event_list': reference_event_list, 'estimated_event_list': estimated_event_list})
    all_data += reference_event_list
event_labels = all_data.unique_event_labels

segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels, time_resolution=1)
event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_label_list=event_labels, t_collar=0.250)
for file_pair in data:
    segment_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])
    event_based_metrics.evaluate(file_pair['reference_event_list'], file_pair['estimated_event_list'])

overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
print "Accuracy:", overall_segment_based_metrics['accuracy']['accuracy']

print segment_based_metrics
print event_based_metrics
