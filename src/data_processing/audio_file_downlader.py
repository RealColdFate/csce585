import re
import urllib.request
from song import Song
import os
import youtube_dl

# TODO fix this so the list/ dict can be loaded in (probably store song data as json)
SONG_MAP = {
    0: Song(index=0, title='Eternal Flame', artist='The Bangles', genre='album rock', year=2004, length=238),
    1: Song(index=1, title='Kingston Town', artist='UB40', genre='reggae fusion', year=1989, length=228),
    2: Song(index=2, title='Always On My Mind', artist='Willie Nelson', genre='classic country pop', year=1982,
            length=213),
    3: Song(index=3, title='The Way It Is', artist='Bruce Hornsby', genre='album rock', year=1986, length=298),
    4: Song(index=4, title='White Flag', artist='Dido', genre='dance pop', year=2003, length=241),
    5: Song(index=5, title='Walking in Memphis', artist='Marc Cohn', genre='folk', year=1991, length=253),
    6: Song(index=6, title='Fairytale of New York (feat. Kirsty MacColl)', artist='The Pogues', genre='celtic punk',
            year=1988, length=272),
    7: Song(index=7, title='The Boys Of Summer', artist='Don Henley', genre='album rock', year=1984, length=289),
    8: Song(index=8, title='Empire State of Mind (Part II) Broken Down', artist='Alicia Keys', genre='hip pop',
            year=2009, length=216),
    9: Song(index=9, title='She Will Be Loved', artist='Maroon 5', genre='pop', year=2002, length=257)
}


def get_url_from_search_term(search_term: str) -> str:
    search_input = search_term.replace(' ', '+')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_input)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return "https://www.youtube.com/watch?v=" + video_ids[0]


def download_from_url(url: str, output_file_name: str) -> None:
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


def main() -> None:
    song_list_name = "test_song_list_of_10_songs_0"  # TODO source this dynamically from song dict
    target_dir = '../../data/unmodified_song_lists/'
    target_dir = os.path.join(target_dir, song_list_name)

    song_list = list(SONG_MAP.values())

    '''
    if you uncomment this it may download a large amount of data to your pc
    '''
    download_playlist(song_list, target_dir)


if __name__ == '__main__':
    main()