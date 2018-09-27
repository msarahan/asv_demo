# asv_demo
Demo for dynamically defining benchmarks from test suites for Air Speed Velocity

This project demonstrates that you can write your tests and only your tests in
normal pytest-discoverable format, or as unittest stuff, and you can do some
voodoo to get ASV to run benchmarks using those tests, rather than writing your
own benchmark-specific tests.

To start, take a look at ``tests/test_functional.py``. This is where the normal test
suite would be defined. These tests are what we want to use for benchmarking,
too. Unfortunately, ASV wants us to define our own separate functions or classes
in the benchmarking folder
(https://asv.readthedocs.io/en/stable/writing_benchmarks.html). The way that ASV
detects benchmarks to run is a simple filename and function name heuristic. If
you can import and rename functions to match that heuristic, can you get ASV to
pick them up?

Yes. That's what this project does. It accomplishes it with lots of introspection. In
``benchmarks/peakmem_test.py``, you'll see a few things:

* the kind of test to run is detected from the filename
  (https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/benchmarks/peakmem_tests.py#L13-L15).
  We detect this dynamically, so that we need not duplicate code. Notice that
  ``time_test.py`` is only a symlink to ``peakmem_test.py``. This is sufficient to run
  two kinds of benchmarks: peakmem and time. You could create another symlink,
  ``mem_test.py``, to also run benchmarks on the size of return values.
* We import our module and place it in ``sys.modules``
  (https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/benchmarks/peakmem_tests.py#L16-L18).
  This ensures that when ASV later tries to import the module, it picks up our
  altered one, rather than getting a fresh thing to inspect
* We call functions defined in ``benchmarks/utils.py`` to detect test functions and
  methods that should have their names altered such that ASV sees them
  (https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/benchmarks/peakmem_tests.py#L25-L26).
  This is all that is required - you need not hard-code any function or class
  definitions in your benchmarks folder.
* Print statements are scattered here so you can see the process. You can run
  the ``peakmem_tests.py`` file directly to see these: ```python benchmarks/peakmem_tests.py```

## Introspection voodoo

Take a look at the benchmarks/utils.py file. This is where the introspection
magic happens. The two main functions, ``add_test_funcs_to_module`` and
``add_renamed_classes_to_module`` are both just globs that collect test files with a
simple pattern. With each of these test files, we do several kinds of
introspection (powered by several helpful Stack Overflow posts):

* Collect top-level functions defined in each file (using ``ast``)
* Detect decorators on each top-level function (using ``ast`` and ``inspect``)
* Filter out functions based on whether they have a specific decorator
* Collect classes that have methods beginning with "test_" and also with a
  specific decorator

From there, we just copy functions or subclass test suite classes, change
function or method names to match ASV's desired values, and add them to the
already-imported entry in ``sys.modules``. There's a couple of tricky bits in here,
though.

* we need to copy function objects so that we can rename them (change their
  ``__name__`` attr). We accomplish this thanks to a Stack Overflow post:
  https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/benchmarks/utils.py#L80-L88
* we need a way to dynamically create subclasses that have different (renamed)
  attributes. Here we can use the builtin, ``type``, which not only tells you
  the type of an object, but can also be used to dynamically create classes.
  Given the function renaming scheme at
  https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/benchmarks/utils.py#L129-L137,
  we create a new class at
  https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/benchmarks/utils.py#L152-153 and
  add it to the module.

## Other important details:

* This only supports python 3.4+. You could probably get it to work with py2.7,
  but sys.modules behaves differently there, and it also seems like lots of the
  introspection stuff works differently.
* the ``benchmark`` decorator comes from registering it with pytest in
  setup.cfg: https://github.com/msarahan/asv_demo/blob/cd346056c3b7fb2bb933b055a5467a25b54fe056/setup.cfg#L20
* The test code and benchmark code that run come from your source tree at the
  time that ASV runs, not from past commits. The actual code that gets installed
  for the benchmark runs comes from past commits. If your current test code
  imports things that aren't in past commits, the (current) tests won't run with
  those past commits. You can either try to restructure your imports in your
  tests to only have things that have been around a long time, or you're stuck
  with writing manual benchmarks that won't import things that aren't in older
  versions.
* I haven't tested this with pytest fixtures or parametrization.  YMMV.
