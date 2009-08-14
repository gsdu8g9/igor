import sys
from os import path

sys.path.append(".")

from igor.tools import prepare_paths, find_files, posts, environment

def test_prepare_paths():
    paths = prepare_paths("./examples/basic", "/tmp/basic")

    assert(paths['source'], "source path was not properly constructed")
    assert(paths['destination'], "destination path was not properly constructed")
    assert(paths['posts'], "posts path was not properly constructed")
    assert(paths['templates'], "templates path was not properly constructed")
    assert(paths['media'], "media path was not properly constructed")

    for key, result_path in paths.iteritems():
        if (key != "destination"):
            assert(path.exists(result_path))

def test_find_files():
    extensions = [".txt", ".mkd"]
    files = list(find_files(path.abspath("./examples/basic/_posts"), extensions=extensions))
    assert(len(files) > 0, "No files returned")
    for file in files:
        ext, name = path.splitext(file)
        assert(path.exists(file), "File does not exist")
        assert(ext in extensions, "File was not of type found in extensions filter")

def test_posts():
    ps = list(posts("./examples/basic/_posts", extensions = [".txt", ".mkd"]))
    assert(len(ps) > 0, "No posts returned")

def test_environment():
    env = environment("./examples/basic/_templates")
    assert(env)
    env = environment("./examples/basic/_templates", global_context = {'a': 'b'})
    assert(env.globals['a'] == 'b')
