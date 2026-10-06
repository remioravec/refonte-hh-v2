#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remet l'article temoin dans son etat d'avant la refonte."""
import os, sys
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp_common as w      # noqa: E402

F = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
     "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/blog-avant/avant-7761.html")
av = open(F, encoding="utf-8").read()
if "faqData" not in av or len(av) < 150000:
    raise SystemExit("ARRET — sauvegarde suspecte (%d o)" % len(av))
print("restauration de %d ko" % (len(av) // 1024))
if "--poser" in sys.argv:
    w.update_content("posts", 7761, av, live=True)
    print("   fait")
else:
    print("(blanc)")
