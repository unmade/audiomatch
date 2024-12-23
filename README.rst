----

audiomatch

----

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
   :target: https://github.com/unmade/audiomatch/blob/master/LICENSE

A small command-line tool to find similar audio files

##############
 Installation
##############

First, install the Chromaprint_ fingerprinting library by Lukáš
Lalinský. (The library itself depends on an FFT library, but it's smart
enough to use an algorithm from software you probably already have
installed; see the Chromaprint page for details.)

Then you can install this library:

.. code:: bash

   pip install audiomatch

To perform tasks quickly, *audiomatch* requires a C compiler and Python
headers to be installed. You can skip the compilation by setting the
``AUDIOMATCH_NO_EXTENSIONS`` environment variable:

.. code:: bash

   AUDIOMATCH_NO_EXTENSIONS=1 pip install audiomatch

You can avoid installing all these libraries on your computer and run
everything in Docker:

.. code:: bash

   docker run --rm -v "$(pwd)":/tmp fdooch/audiomatch "/tmp/*"

############
 Quickstart
############

Suppose we have a directory with Nirvana songs:

.. code:: bash

   $ ls demo
   All Apologies (In Utero).m4a           Dumb (Unplugged in NYC).m4a
   All Apologies (Unplugged in NYC).m4a   Pennyroyal Tea (In Utero).m4a
   Dumb (In Utero).m4a                    Pennyroyal Tea (Solo Acoustic).mp3
   Dumb (Radio Appearance, 1991).mp3      Pennyroyal Tea (Unplugged in NYC).m4a

Let's find out which files sound similar:

.. code:: bash

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

*Note #1: Input audio files should be at least 10 seconds long.*

*Note #2: In some rare cases, false positives are possible.*

What's happening here is that *audiomatch* takes all audio files from
the directory and compares them with each other.

You can also compare a file with another file, a file and a directory,
or a directory with another directory. If you need to, you can provide
glob-style patterns, but don't forget to quote them, because otherwise
the shell will expand it for you. For example, let's compare all
``.mp3`` files with ``.m4a`` files:

.. code:: bash

   $ audiomatch "./demo/*.mp3" "./demo/*.m4a"
   These files sound similar:

   ../demo/Pennyroyal Tea (Solo Acoustic).mp3
   ../demo/Pennyroyal Tea (Unplugged in NYC).m4a

This time, *audiomatch* took all files with the ``.mp3`` extension and
compared them with all files with the ``.m4a`` extension.

Note how there is no In Utero version in the output. The reason it is
present in the previous output is because it is actually similar to the
Unplugged version, and then the transitive law applies: if ``a = b`` and
``b = c``, then ``a = c``.

**********
 --length
**********

The ``--length`` option specifies how many seconds to take for analysis
from the song. The default value is 120, and it is good enough to find
exactly the same song, but maybe in different quality. However, for more
complicated cases like the same song played in a different tempo, the
more input we have, the more accurate results are.

*************
 --extension
*************

By default, ``audiomatch`` looks for files with ``.m4a``, ``.mp3``,
``.caf`` extensions. In theory, audio formats supported by ffmpeg_ are
also supported by *audiomatch*. You can tell *audiomatch* to look for a
specific format by using the ``--extension`` flag:

.. code:: bash

   $ audiomatch -e .ogg -e .wav ./demo
   Not enough input files.

Indeed, we tried to compare files with ``.ogg`` and ``.wav`` extensions,
but there are no such files in the demo directory.

############
 Motivation
############

I play guitar and do recordings from time to time, mainly with Voice
Memos on iPhone. Over the years, I have hundreds of recordings like
that, and I thought it would be cool to find all the similar ones and
see how I have progressed over the years.

That's why I wrote this library.

############
 References
############

-  Chromaprint_ and pyacoustid_ libraries
-  `Example: How to compare fingerprints`_
-  `Example: How to compare shifted fingerprints`_ (note: the code is a
   little bit weird)
-  `Explanation: How to compare fingerprints`_
-  `Popcount in Python with benchmarks`_

.. _chromaprint: https://github.com/acoustid/chromaprint

.. _example: how to compare fingerprints: https://gist.github.com/lalinsky/1132166

.. _example: how to compare shifted fingerprints: https://medium.com/@shivama205/audio-signals-comparison-23e431ed2207

.. _explanation: how to compare fingerprints: https://groups.google.com/forum/#!msg/acoustid/Uq_ASjaq3bw/kLreyQgxKmgJ

.. _ffmpeg: http://ffmpeg.org

.. _popcount in python with benchmarks: http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html

.. _pyacoustid: https://github.com/beetbox/pyacoustid
