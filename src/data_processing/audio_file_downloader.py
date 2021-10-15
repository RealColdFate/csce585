import re
import urllib.request
from song import *
import os
import youtube_dl


def get_url_from_search_term(search_term: str) -> str:
    """
    Attains url from search query
    :param search_term: str
    :return: str url
    """
    search_input = search_term.replace(' ', '+')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_input)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return "https://www.youtube.com/watch?v=" + video_ids[0]


def download_from_url(url: str, output_file_name: str) -> None:
    """
    Downloads audio file in mp3 format from youtube url
    :param url: str
    :param output_file_name: str
    """
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=url, download=False
    )
    filename = f"{output_file_name}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))


def download_playlist(playlist: list, output_file_path: str) -> None:
    """
    Downloads a playlist of .mp3 audio files given list of search terms from youtube
    :param playlist: list of search terms
    :param output_file_path: str
    """
    # create parent dirs
    split = os.path.split(output_file_path)
    if not os.path.isdir(split[0]):
        os.mkdir(split[0])
        if not os.path.isdir(output_file_path):
            os.mkdir(output_file_path)

    # download songs into dir
    for i in range(len(playlist)):
        search_string = playlist[i].title
        output_file_name = os.path.join(output_file_path, f"song{i}")

        youtube_url = get_url_from_search_term(search_string)
        download_from_url(youtube_url, output_file_name)
        print(f"Downloaded {playlist[i].title}")


def get_json_str_form_file(file_path: str) -> str:
    """
    Returns the content of a text file as a valid json string
    :param file_path: str
    :return: str
    """
    with open(file_path, 'r') as file:
        return file.read().replace('\n', '')


def get_song_dict_form_json_dict(json_dict: dict) -> dict:
    """
    Takes a dictionary of json objects and returns a dictionary of Song objects mapped to their key from the json dict
    :param json_dict: dict
    :return: dict
    """
    for k, v in json_dict.items():
        json_dict[k] = load_song_form_json(v)

    return json_dict


def main() -> None:
    sample_dict_path = "sample_dicts/sample_dict_of_3_songs_0_.json"
    target_dir = '../../data/unmodified_song_lists/'

    song_list_name = os.path.split(sample_dict_path)[1].replace('.json', '')

    target_dir = os.path.join(target_dir, song_list_name)

    json_str = get_json_str_form_file(sample_dict_path)
    json_map = json.loads(json_str)
    song_map = get_song_dict_form_json_dict(json_map)
    song_list = list(song_map.values())

    '''
    if you uncomment this it may download a large amount of data to your pc
    '''
    # download_playlist(song_list, target_dir)


if __name__ == '__main__':
    main()
