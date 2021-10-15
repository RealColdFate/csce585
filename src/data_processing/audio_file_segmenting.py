from pydub import AudioSegment
import time
import os

PROJECT_DATA_PATH = "../../data/"  # project data path do not change
TARGET_SONG_LIST = "sample_dict_of_20_songs_0_"  # target list change to target different list of songs

# only change if you have changed project structure elsewhere
SONG_DIR_PATH = f"../../data/unmodified_song_lists/{TARGET_SONG_LIST}"

# project song segment export path do not change
PROJECT_SONG_SEGMENT_EXPORT_PATH = os.path.join(PROJECT_DATA_PATH, "segmented_songs")
EXPORT_PATH_FOR_SEGMENTS_OF_TARGET_SONG_LIST = os.path.join(PROJECT_SONG_SEGMENT_EXPORT_PATH,
                                                            str(TARGET_SONG_LIST + 'segments'))

SONG_SEGMENT_LENGTH = 3  # this is the segmentation length in seconds change will require redefinition of model input


def segment_song(song_file_path: str, segment_export_path: str, segment_length_seconds: int) -> None:
    """
    Takes a path to an audio file splits it and exports it to some output path in .mp3 formatted segments
    :param song_file_path: str
    :param segment_export_path: str
    :param segment_length_seconds: int
    """
    # gathers song from file
    sound = AudioSegment.from_file(song_file_path)
    # song length in AudioSegment object is in milliseconds
    seconds = len(sound) // 1000
    sound_len = seconds * 1000
    step_size = segment_length_seconds * 1000

    # splitting audio and exporting
    for i in range(0, sound_len, step_size):
        next_step = step_size + i
        segment = sound[i:next_step]
        segment_name = str(os.path.basename(segment_export_path) + '-seg-' + str(segment_length_seconds) + '-' + str(
            i // step_size) + '.mp3')
        final_export_path = os.path.join(segment_export_path, segment_name)
        segment.export(final_export_path, format='mp3')


def gather_song_paths_list(dir_path: str) -> list:
    """
    Takes a directory and returns full paths to the files in that dir
    it is assumed that all files will be .mp3 files
    :param dir_path: str
    :return: list of full file paths
    """
    return [os.path.join(dir_path, p) for p in os.listdir(dir_path)]


def get_sub_dir_names_form_song_paths(song_paths: list) -> list:
    """
    This is formatting for the sub directories the song segments will be exported to
    so it will just parse the song names form the song file paths
    assumes that all paths to songs are .mp3 files
    :param song_paths: list of string paths to song files
    :return: list of song names form provided song paths
    """
    song_classes = []
    for p in song_paths:
        # this is just some nasty way to get the song name from the full file path
        s = os.path.basename(p)[:-4]
        song_classes.append(s)
    return song_classes


def create_segment_dirs(song_paths: list, export_dir: str) -> list:
    """
    Creates the directories needed to store the songs segment in the given export path
    assumes that all paths to songs are .mp3 files
    :param song_paths: list of string paths to song files
    :param export_dir: str
    :return list of paths to export directories for song segments
    """

    # create parent directories if they don't exist
    split_export_dir = os.path.split(export_dir)
    if not os.path.isdir(split_export_dir[0]):
        os.mkdir(split_export_dir[0])
    if not os.path.isdir(export_dir):
        os.mkdir(export_dir)

    # get the song names form paths
    song_names = get_sub_dir_names_form_song_paths(song_paths)

    segment_dir_paths = []
    # create individual sub directories for each song
    for s in song_names:
        full_export_dir_for_song_segments = os.path.join(export_dir, s)
        segment_dir_paths.append(full_export_dir_for_song_segments)
        if not os.path.isdir(full_export_dir_for_song_segments):
            os.mkdir(full_export_dir_for_song_segments)

    return segment_dir_paths


def segment_songs(song_paths: list, export_path_name_pairs: list, segment_length_seconds: int) -> None:
    """
    Segments songs from given lists and exports segments to given paths
    :param segment_length_seconds: int
    :param song_paths: list of strings to .mp3 files
    :param export_path_name_pairs: list of strings to dir
    """

    if len(song_paths) != len(export_path_name_pairs):
        raise ValueError

    for i in range(len(song_paths)):
        start_time = time.time()
        segment_song(song_paths[i], export_path_name_pairs[i], segment_length_seconds)
        end_time = time.time()
        print(f"Completed segmentation of {os.path.basename(song_paths[i])} in {end_time - start_time}s")
        print(f"Exported to \"{export_path_name_pairs[i]}\"")


def main() -> None:
    song_file_paths = gather_song_paths_list(SONG_DIR_PATH)
    segment_export_paths = create_segment_dirs(song_file_paths, EXPORT_PATH_FOR_SEGMENTS_OF_TARGET_SONG_LIST)

    segment_songs(song_file_paths, segment_export_paths, SONG_SEGMENT_LENGTH)


if __name__ == '__main__':
    main()
