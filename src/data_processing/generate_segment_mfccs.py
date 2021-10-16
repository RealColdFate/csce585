from audio_file_segmenting import *
import numpy as np
from numpy import ndarray
import json
import time
import warnings
import librosa

''' 
 This constant assumes that the song segments you want to get MFCCs for are in the export path
 for the list provided to "audio_file_segmenting.py"
'''
TARGET_PATH_FOR_SEGMENT_MFCCS = EXPORT_PATH_FOR_SEGMENTS_OF_TARGET_SONG_LIST
SEGMENT_MFCC_EXPORT_PATH = os.path.join(PROJECT_SONG_SEGMENT_EXPORT_PATH, TARGET_SONG_LIST + 'segment_mfccs')
NUMBER_OF_MFCC = 35


def gather_segment_dir_target_paths(target_dir_of_song_list: str) -> list:
    """
    Takes the path of the partent directory where the song segments are stored and returns a list of the paths to
    the sub directories for each songs segments
    :param target_dir_of_song_list: str
    :return: list
    """
    return [p for p in gather_song_paths_list(target_dir_of_song_list)]


def gather_segment_paths(segment_parent_dir_list: list) -> list:
    """
    Takes a list of parent directories for each song's segments and returns a 2d list of the paths for each of the
    song's segments corresponding to their song directory
    :param segment_parent_dir_list: list
    :return: list
    """
    return [[p for p in gather_song_paths_list(pd)] for pd in segment_parent_dir_list]


def create_segment_mfcc_export_dirs(export_path: str, segment_parent_dirs: list) -> list:
    """
    Creates export directories for mfccs for song segments and returns them as a list of file paths
    :param export_path: str
    :param segment_parent_dirs: list
    :return: list
    """
    if not os.path.isdir(export_path):
        os.mkdir(export_path)

    song_segment_mfcc_export_paths = []
    for i in segment_parent_dirs:
        full_seg_mfcc_export_dir = os.path.join(export_path, os.path.basename(i))
        if not os.path.isdir(full_seg_mfcc_export_dir):
            os.mkdir(full_seg_mfcc_export_dir)
        song_segment_mfcc_export_paths.append(full_seg_mfcc_export_dir)

    return song_segment_mfcc_export_paths


# disable warning display because librosa will display a warning while trying to open .mp3 files
warnings.filterwarnings(action='ignore', category=Warning, module='librosa')


def create_feature_vector_of_mean_mfcc_for_song(song_file_path: str) -> ndarray:
    """
    Takes in a file path to a song segment and returns a numpy array containing the mean mfcc values
    :param song_file_path: str
    :return: ndarray
    """
    song_segment, sample_rate = librosa.load(song_file_path)
    mfccs = librosa.feature.mfcc(y=song_segment, sr=sample_rate, n_mfcc=NUMBER_OF_MFCC)
    mfccs_processed = np.mean(mfccs.T, axis=0)

    return mfccs_processed


def get_seg_name(segment_path: str) -> str:
    return os.path.basename(segment_path)[:-4]


def create_mfcc_feature_vectors(segment_list_path_matrix: list, export_dir_paths: list) -> None:
    """
    Takes in a matrix with lists of segment paths corresponding to the read order of the song directories
    and a list of export directories for json files of labeled feature vectors to be sent to
    :param segment_list_path_matrix: list
    :param export_dir_paths: list
    """
    if len(segment_list_path_matrix) != len(export_dir_paths):
        raise ValueError

    start_time_total = time.time()
    for i in range(len(segment_list_path_matrix)):
        start_time = time.time()
        song_class_name = os.path.basename(export_dir_paths[i])
        for sp in segment_list_path_matrix[i]:
            segment_number = get_seg_name(sp)
            final_export_file_path = os.path.join(export_dir_paths[i], f"{segment_number}-mfccs.json")

            features = create_feature_vector_of_mean_mfcc_for_song(sp)
            data = [features.tolist(), song_class_name]
            save_features_to_json(data, final_export_file_path)

        end_time = time.time()
        print(f"Completed creation of mfcc vectors for {song_class_name} in {end_time - start_time}s")
    end_time_total = time.time()
    print(f"Total time elapsed {end_time_total - start_time_total}s")


def save_features_to_json(data: list, export_path: str) -> None:
    """
    Writes data given to json file with path provided
    this will not work if data object passed is not json serializable
    :param data: list
    :param export_path: str
    """
    with open(export_path, 'w') as f:
        json.dump(data, f)


def main() -> None:
    parent_directories = gather_segment_dir_target_paths(TARGET_PATH_FOR_SEGMENT_MFCCS)
    song_segment_matrix = gather_segment_paths(parent_directories)
    mfcc_export_dirs = create_segment_mfcc_export_dirs(SEGMENT_MFCC_EXPORT_PATH, parent_directories)

    create_mfcc_feature_vectors(song_segment_matrix, mfcc_export_dirs)


if __name__ == "__main__":
    main()
