pwcheck
===========
This bitcoin fork has a small extension added to the original codebase in order to make rapidly attempting passwords against the cryptographic security measures locking a bitcoin wallet easier to do. The extension is kept in pwcheck.cpp, once you've inserted your wallets values build with `make -f makefile.["unix", "osx"] pwcheck`.

You will need from your wallet the following:

* Number of iterations  (wallet)
* Salt  (wallet)
* Crypted Key  (wallet)
* Public Key  (from a transaction)
* Crypted Secret  (from a transaction)

Values are currently hardcoded into pwcheck.cpp, so you'll need to extract the values from your wallet you're trying to unlock and replace them in pwcheck.cpp before compiling for your machine. The current values belong to a wallet what might yet be unlocked…

Any input can be piped into pwcheck. I've included an example C++ program which outputs all permutations (using the std library) of its only input, which can be piped into pwcheck in order to try all permutation of a passphrase, each attempt is output. This is stored in src as a program called `permute.cpp`. Simply compile it with 'g++ permute.cpp -o permute'. So for instance, the command `..\permute banana | .\pwcheck` generates the permutations of banana, and outputs:

* aaabnn
* aaanbn
* aaannb

and so on, trying each against the wallet's hash. The way this is done mimics the Unlock() method of the Wallet.cpp class of the original Bitcoin source.

If (& hopefully when!) a password hashes against the wallet correctly, the program reports success and terminates.


I wrote this piggybacking off of Bitcoin, although I stripped out every piece of the original Bitcoin source that was not absolutely necessary for pwcheck. This makes it an efficient program for rapidly attempting a large number of passwords against your wallet's cryptographic hash without needing to use bitcoind. ([parallel](http://savannah.gnu.org/projects/parallel) looks encouraging for its ability to, well, parallelize processing of your potentially large input. Unfortunately the use of SecureString precludes that possibility (eg, cat huge_dictionary | parallel --eta -j+0 ../pwcheck) for now.)



====================

What is Bitcoin?
----------------

Bitcoin is an experimental new digital currency that enables instant payments to
anyone, anywhere in the world. Bitcoin uses peer-to-peer technology to operate
with no central authority: managing transactions and issuing money are carried
out collectively by the network. Bitcoin Core is the name of open source
software which enables the use of this currency.

For more information, as well as an immediately useable, binary version of
the Bitcoin Core software, see https://www.bitcoin.org/en/download.

License
-------

Bitcoin Core is released under the terms of the MIT license. See [COPYING](COPYING) for more
information or see http://opensource.org/licenses/MIT.

Development process
-------------------

Developers work in their own trees, then submit pull requests when they think
their feature or bug fix is ready.

If it is a simple/trivial/non-controversial change, then one of the Bitcoin
development team members simply pulls it.

If it is a *more complicated or potentially controversial* change, then the patch
submitter will be asked to start a discussion (if they haven't already) on the
[mailing list](http://sourceforge.net/mailarchive/forum.php?forum_name=bitcoin-development).

The patch will be accepted if there is broad consensus that it is a good thing.
Developers should expect to rework and resubmit patches if the code doesn't
match the project's coding conventions (see [doc/coding.md](doc/coding.md)) or are
controversial.

The `master` branch is regularly built and tested, but is not guaranteed to be
completely stable. [Tags](https://github.com/bitcoin/bitcoin/tags) are created
regularly to indicate new official, stable release versions of Bitcoin.

Testing
-------

Testing and code review is the bottleneck for development; we get more pull
requests than we can review and test on short notice. Please be patient and help out by testing
other people's pull requests, and remember this is a security-critical project where any mistake might cost people
lots of money.

### Automated Testing

Developers are strongly encouraged to write unit tests for new code, and to
submit new unit tests for old code. Unit tests can be compiled and run (assuming they weren't disabled in configure) with: `make check`

Every pull request is built for both Windows and Linux on a dedicated server,
and unit and sanity tests are automatically run. The binaries produced may be
used for manual QA testing — a link to them will appear in a comment on the
pull request posted by [BitcoinPullTester](https://github.com/BitcoinPullTester). See https://github.com/TheBlueMatt/test-scripts
for the build/test scripts.

### Manual Quality Assurance (QA) Testing

Large changes should have a test plan, and should be tested by somebody other
than the developer who wrote the code.
See https://github.com/bitcoin/QA/ for how to create a test plan.

Translations
------------

Changes to translations as well as new translations can be submitted to
[Bitcoin Core's Transifex page](https://www.transifex.com/projects/p/bitcoin/).

Translations are periodically pulled from Transifex and merged into the git repository. See the
[translation process](doc/translation_process.md) for details on how this works.

**Important**: We do not accept translation changes as GitHub pull requests because the next
pull from Transifex would automatically overwrite them again.

Translators should also subscribe to the [mailing list](https://groups.google.com/forum/#!forum/bitcoin-translators).

Development tips and tricks
---------------------------

**compiling for debugging**

Run configure with the --enable-debug option, then make. Or run configure with
CXXFLAGS="-g -ggdb -O0" or whatever debug flags you need.

**debug.log**

If the code is behaving strangely, take a look in the debug.log file in the data directory;
error and debugging messages are written there.

The -debug=... command-line option controls debugging; running with just -debug will turn
on all categories (and give you a very large debug.log file).

The Qt code routes qDebug() output to debug.log under category "qt": run with -debug=qt
to see it.

**testnet and regtest modes**

Run with the -testnet option to run with "play bitcoins" on the test network, if you
are testing multi-machine code that needs to operate across the internet.

If you are testing something that can run on one machine, run with the -regtest option.
In regression test mode, blocks can be created on-demand; see qa/rpc-tests/ for tests
that run in -regtest mode.

**DEBUG_LOCKORDER**

Bitcoin Core is a multithreaded application, and deadlocks or other multithreading bugs
can be very difficult to track down. Compiling with -DDEBUG_LOCKORDER (configure
------------------------------------------
CXXFLAGS="-DDEBUG_LOCKORDER -g") inserts run-time checks to keep track of which locks
are held, and adds warnings to the debug.log file if inconsistencies are detected.
