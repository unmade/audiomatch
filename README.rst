==========
audiomatch
==========

.. image:: https://github.com/unmade/audiomatch/workflows/lint%20and%20test/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/unmade/audiomatch/blob/master/.github/workflows/lint-and-test.yml

.. image:: https://codecov.io/gh/unmade/audiomatch/branch/master/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/gh/unmade/audiomatch

.. image:: https://img.shields.io/pypi/v/audiomatch.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/audiomatch

.. image:: https://img.shields.io/badge/License-MIT-purple.svg
    :alt: MIT License
    :target: https://github.com/unmade/apiwrappers/blob/master/LICENSE


A small command-line tool to find similar audio files

Installation
============

First, install the Chromaprint_ fingerprinting library by Lukáš Lalinský. (The library
itself depends on an FFT library, but it's smart enough to use an algorithm from
software you probably already have installed; see the Chromaprint page for details)

Then you can install this library:

.. code-block:: bash

    pip install audiomatch

To do things fast *audiomatch* requires C compiler and Python headers to be installed.
You can skip compilation by setting ``AUDIOMATCH_NO_EXTENSIONS`` environment variable:

.. code-block:: bash

    AUDIOMATCH_NO_EXTENSIONS=1 pip install audiomatch

You can avoid installing all this libraries on your computer and run everything in
docker:

.. code-block:: bash

    docker run --rm -v "$(pwd)":/tmp fdooch/audiomatch "/tmp/*"

Quickstart
==========

Suppose, we have a directory with Nirvana songs:

.. code-block:: bash

    $ ls demo
    All Apologies (In Utero).m4a           Dumb (Unplugged in NYC).m4a
    All Apologies (Unplugged in NYC).m4a   Pennyroyal Tea (In Utero).m4a
    Dumb (In Utero).m4a                    Pennyroyal Tea (Solo Acoustic).mp3
    Dumb (Radio Appearance, 1991).mp3      Pennyroyal Tea (Unplugged in NYC).m4a

Let's find out which files sound similar:

.. code-block:: bash

    $ audiomatch --length 300 ./demo
    These files sound similar:

    ./demo/All Apologies (In Utero).m4a
    ./demo/All Apologies (Unplugged in NYC).m4a

    ---

    ./demo/Dumb (In Utero).m4a
    ./demo/Dumb (Unplugged in NYC).m4a

    ---

    ./demo/Pennyroyal Tea (In Utero).m4a
    ./demo/Pennyroyal Tea (Solo Acoustic).mp3
    ./demo/Pennyroyal Tea (Unplugged in NYC).m4a

*Note #1: input audio files should be at least 10 seconds long*

*Note #2: in some rare cases false positives are possible*

What's happening here is that *audiomatch* takes all audio files from the directory and
compares them with each other.

You can also compare file with another file, file and directory, or directory to
directory. If you need to, you can provide glob-style patterns, but don't forget to
quote it, because otherwise shell expanded it for you. For example, let's compare all
``.mp3`` files with ``.m4a`` files:

.. code-block:: bash

    $ audiomatch  "./demo/*.mp3" "./demo/*.m4a"
    These files sound similar:

    ../demo/Pennyroyal Tea (Solo Acoustic).mp3
    ../demo/Pennyroyal Tea (Unplugged in NYC).m4a

This time, *audiomatch* took all files with ``.mp3`` extension and compare them with
all files with ``.m4a`` extension.

Note, how there is no In Utero version in the output. The reason it is present in the
previous output, because it actually similar with Unplugged version and then transitive
law applies: if ``a = b`` and ``b = c``, then ``a = c``.

--length
--------

The ``--length`` specifies how many seconds to take for analysis from the song. Default
value is 120 and it is good enough to find exactly the same song, but maybe in different
quality. However, for a more complicated cases like same song played in different tempo
the more input we have the more accurate results are.

--extension
-----------

By default, ``audiomatch`` looks for files with ``.m4a``, ``mp3``, ``.caf`` extensions.
In theory, audio formats supported by ffmpeg_ also supported by *audiomatch*. You can
tell to *audiomatch* to look for a specific format by using ``--extension`` flag:

.. code-block:: bash

    $ audiomatch -e .ogg -e .wav ./demo
    Not enough input files.

Indeed, we tried to compare files with ``.ogg`` and ``.wav`` extension, but there are
no such files in the demo directory.

Motivation
==========

I play guitar and do recordings from time to time mainly with Voice Memos on iPhone.
Over the years, I have hundreds of recordings like that and I though it would be cool
to find all the similar ones and see how I progress over the years.

That's why I wrote this library.

References
==========

- Chromaprint_ and pyacoustid_ libraries
- `Example: How to compare fingerprints`_
- `Example: How to compare shifted fingerprints`_ (note: the code is a little bit weird)
- `Explanation: How to compare fingerprints`_
- `Popcount in Python with benchmarks`_

.. _Chromaprint: https://github.com/acoustid/chromaprint
.. _`Example: How to compare fingerprints`: https://gist.github.com/lalinsky/1132166
.. _`Example: How to compare shifted fingerprints`: https://medium.com/@shivama205/audio-signals-comparison-23e431ed2207
.. _`Explanation: How to compare fingerprints`: https://groups.google.com/forum/#!msg/acoustid/Uq_ASjaq3bw/kLreyQgxKmgJ
.. _ffmpeg: http://ffmpeg.org
.. _`Popcount in Python with benchmarks`: http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
.. _`pyacoustid`: https://github.com/beetbox/pyacoustid
