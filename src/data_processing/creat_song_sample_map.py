import csv
import os
import random
from song import Song

SAMPLE_SIZE = 20


def count_song_map_total_duration(song_dict: dict) -> int:
    """
    counts total duration of a given dictionary of Song objects
    :param song_dict: dict
    :return: int
    """
    total_duration = 0
    for k, v in song_dict.items():
        total_duration += v.length
    return total_duration


def read_in_song_list(input_file_path: str) -> list:
    """
    Takes a the file path of a csv file containing song data and adds the rows to a list
    :param input_file_path: str
    :return: list
    """
    songs = []
    # read in song data form file
    with open(input_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            songs.append(row)

    # strip out labels from data (labels are at index 0 in csv file)
    songs = songs[1::]

    return songs


def create_song_map_sample(song_list: list, list_population: int) -> dict:
    """
    Samples songs from a given list of song data and turns it into a dict mapping the index of
    the song with its relevant data
    :param song_list: list
    :param list_population: int
    :return: dict
    """
    # int for indexing songs dict to store song index pairs
    i = 0
    song_dict = {}
    # take random sample of songs and put them into the dict
    for s in random.sample(song_list, list_population):
        index = i
        title = s[1]
        artist = s[2]
        genre = s[3]
        year = int(s[4])
        length = int(s[-4].replace(',', ''))
        song_dict[i] = Song(index, title, artist, genre, year, length)
        i += 1

    return song_dict


def parse_target_directory_for_next_available_file_name(target_dir: str, list_len: int) -> str:
    """
    Looks through target directory for the last created instance of a song dict
    and increments it's matching "key" and returns a new string of the file path for the song dict file
    :param target_dir: str
    :param list_len: int
    :return: str
    """

    # searches target directory for files
    valid_keys = []
    for f in os.listdir(target_dir):

        # splits files by delimiter '_' and parses info
        path_split = f.split('_')
        song_list_len = int(path_split[3])
        song_list_key = int(path_split[5])

        # check song dict file is the right length
        if song_list_len == list_len:
            valid_keys.append(song_list_key)

    # check there actually is a song dict of the given length
    if len(valid_keys) == 0:
        new_key = 0
    else:
        new_key = max(valid_keys) + 1

    out_put_file_name = f"sample_dict_of_{list_len}_songs_{new_key}_.py"

    return os.path.join(target_dir, out_put_file_name)


def write_song_map_sample_to_file(song_dict: dict):
    """
    Writes the given song dict into a working python file
    :param song_dict: dict
    """
    target_dir = 'sample_dicts'

    output_file_path = parse_target_directory_for_next_available_file_name(target_dir, len(song_dict))

    with open(output_file_path, 'w') as f:

        i = 1
        f.write("from ..song import Song\n\nSONG_MAP = {\n")
        for k, v in song_dict.items():
            if not i == SAMPLE_SIZE:
                item_str = ' ' * 4 + str(k) + ': ' + repr(v) + ',\n'
                f.write(item_str)
            else:
                item_str = ' ' * 4 + str(k) + ': ' + repr(v) + '\n'
                f.write(item_str)
            i += 1
        f.write('}')


def main():
    full_song_list_file_path = "../../data/Spotify-2000.csv"

    songs = read_in_song_list(full_song_list_file_path)

    song_map = create_song_map_sample(songs, SAMPLE_SIZE)

    total_song_dict_duration = count_song_map_total_duration(song_map)

    write_song_map_sample_to_file(song_map)

    print(f"Successfully created dict of {SAMPLE_SIZE} random songs.\nPlaylist duration: {total_song_dict_duration}")


if __name__ == '__main__':
    main()
