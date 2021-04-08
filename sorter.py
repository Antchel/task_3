#!/usr/bin/env python3

import os
import click
import eyed3


@click.command()
@click.option('-s', '--src-dir',
              type=click.Path(),
              help='Source directory.',
              default=os.getcwd())
@click.option('-d', '--dst-dir',
              type=click.Path(),
              help='Destination directory.',
              default=os.getcwd())
def main(src_dir: str, dst_dir: str) -> None:
    """[Author - Golovenko Anton] MP3 files sorter program. 2021 (c)"""

    eyed3.log.setLevel("ERROR")
    source_path_exists = os.path.exists(src_dir)
    if source_path_exists:
        files = os.listdir(src_dir)
        files_list = list(filter(lambda x: x.endswith('.mp3'), files))
        if files_list:
            # если файлы в списке есть, обрабатываем каждый из них
            for file_name in files_list:
                audio_file = eyed3.load(file_name)
                title = audio_file.tag.title.strip() if audio_file.tag.title else None
                singer = audio_file.tag.artist.strip() if audio_file.tag.artist else None
                album = audio_file.tag.album.strip() if audio_file.tag.album else None

                new_filename = generate_new_name(title, singer, album)
                if new_filename is None:
                    new_filename = file_name

                if singer and album:
                    new_path = os.path.join(singer, album)
                else:
                    continue

                new_file = os.path.join(dst_dir, new_path, new_filename)
                try:
                    os.renames(file_name, new_file)
                    print(f'{file_name} -> {new_file}')

                except Exception as e:
                    print(e)
        else:
            print('ERROR: There are no *.mp3 files on the specified path')
    else:
        print('ERROR: Source directory not exist')
    print('[INFO] Done.')


def file_has_permissions(filename):
    try:
        with open(filename, 'rb') as f:
            f.readline()
        return True

    except PermissionError:
        print(f'Has not file access permissions {filename}')
        return False


def generate_new_name(title, singer, album):
    if title:
        return f'{title} - {singer} - {album}.mp3'
    else:
        return None


if __name__ == '__main__':
    main()
