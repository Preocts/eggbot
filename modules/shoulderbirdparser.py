#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shoulder Bird is a bot plugin that pings a user when a defined keyword is read in chat

This was designed for Nayomii.

The processes contained in this script handle parsing chat messages to identify
keywords as defined on a guild/user basis. Keywords are searched by word bounded
regex expressions. When a keyword is found, the contents of the message containing
the keyword is send, via DM, to the user who setup the search.

Dependancies:
    shoulderbirdconfig.py
    shoulderbirdcli.py

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
