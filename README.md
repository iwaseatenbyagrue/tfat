tfat
====

tfat is a tool for automating things.

tfat itself provides a library for helping to automate things.
tfat plugins then use that library to automate things.

Overview
--------

At its core, tfat uses a task pipeline to run tasks in parallel where possible.
It provides a number of common tasks, logging, and other general facilities.

It also provides a number of common parameters for CLI scripts.

Includes plugins
------------------

### password

A simple password generator.

It uses SecureRandom to provide entropy, and should be considered more
useful than secure.

#### generate

This maps integers from SystemRandom into bytes, and prints them.

The bytes are hex encoded by default, but base64 and raw encoding is available.

#### create

This creates a password from a set of content rules, e.g. 2 number, 2 upper.
Any character class specified in rules is used to generate the remainder
of the password up to a specified length.

### download

A set of tools to download stuff.

#### podcast

Downloads audio content given one or more RSS feeds.

Run periodically, and optionally with a configuration file, it can help
keep your local podcast collection up to date.
