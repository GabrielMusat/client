import os


def maybe_create(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)