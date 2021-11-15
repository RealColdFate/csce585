from generate_segment_mfccs import *


def overlay_sounds(sound_path_one, sound_path_two, export_path) -> None:
    song_segment = AudioSegment.from_file(sound_path_one)
    sound = AudioSegment.from_file(sound_path_two)

    combined = sound.overlay(song_segment)

    combined.export(export_path, format='mp3')


def export_sound_overlay(segment_list_paths: list, export_dir_paths: list, sound_overlay_inputs: list) -> None:
    start_time_total = time.time()
    for i in range(len(segment_list_paths)):
        start_time = time.time()
        song_class_name = os.path.basename(export_dir_paths[i])
        for sp in segment_list_paths[i]:
            for j in range(len(sound_overlay_inputs)):
                segment_number = get_seg_name(sp)
                final_export_file_path = os.path.join(export_dir_paths[i],
                                                      f"{segment_number}-{os.path.basename(sound_overlay_inputs[j])[0:-4]}.mp3")
                overlay_sounds(sound_overlay_inputs[j], sp, final_export_file_path)
        end_time = time.time()
        print(f"Completed creation of overlays for {song_class_name} in {end_time - start_time}s")
    end_time_total = time.time()
    print(f"Total time elapsed {end_time_total - start_time_total}s")


def get_sound_overlay_paths(parent_path: str) -> list:
    return os.listdir(parent_path)


SEGMENT_OVERLAY_EXPORT_PATH = '../../data/song_seg_sound_overlays/'
OVERLAY_SOUNDS_PARENT_DIR = '../../data/sounds'


def main() -> None:
    parent_directories = gather_segment_dir_target_paths(TARGET_PATH_FOR_SEGMENT_MFCCS)
    print(parent_directories)
    song_segment_list = gather_segment_paths(parent_directories)
    overlay_export_dir = create_segment_mfcc_export_dirs(SEGMENT_OVERLAY_EXPORT_PATH, parent_directories)
    overlay_sounds_paths = [os.path.join(OVERLAY_SOUNDS_PARENT_DIR, p) for p in os.listdir(OVERLAY_SOUNDS_PARENT_DIR)]

    export_sound_overlay(song_segment_list, overlay_export_dir, overlay_sounds_paths)


if __name__ == "__main__":
    main()
