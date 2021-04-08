#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
import os
import eyed3

import shutil

@click.command()

@click.option('-s', '--src-dir',
              default='.',
              help='Source directory.',
              show_default=True)
@click.option('-d', '--dst-dir',
              default='.',
              help='Destination directory.',
              show_default=True)

def sort(src_dir, dst_dir):
    if os.path.isdir(src_dir):
        try:
            dir_list = os.scandir(src_dir)
        except PermissionError as e:
            print(str(e))
        else:
            with dir_list:
                for file_name in dir_list:
                    if file_name.name.lower().endswith('.mp3'):
                        try:
                            track = eyed3.load(file_name)
                            if not track.tag.title:
                                title = file_name.name
                            else:
                                title = track.tag.title.replace('/', '_')
                            if not track.tag.artist or not track.tag.album:
                                print(f'Not enough tags: {file_name.name}')
                                continue
                            else:
                                artist = track.tag.artist.replace('/', '_')
                                album = track.tag.album.replace('/', '_')
                            #track.tag.save()
                        except AttributeError as e:
                            print(f'Something wrong with file: {file_name.name}')
                        except PermissionError as e:
                            print(f'Have no permits to change file: {file_name.name}')
                            continue
                        else:
                            new_file_name = f'{title} - {artist} - {album}.mp3'
                            if os.path.exists(os.path.join(dst_dir, artist, album)):
                                shutil.move(os.path.join(src_dir, file_name.name),
                                            os.path.join(dst_dir, artist, album, new_file_name))
                            else:
                                try:
                                    os.makedirs(os.path.join(dst_dir, artist, album))
                                except PermissionError as e:
                                    print(str(e))
                                else:
                                    shutil.move(os.path.join(src_dir, file_name.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))
                            print(f'{os.path.join(src_dir, file_name.name)} '
                                  f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
        print ("[INFO] Done.")
    else:
        print('Source directory not found.')


sort()