#!/usr/bin/env bash
cd ~/whip
python3 scrapper.py update
python3 prepare.py
Rscript make_graph.R
git add *
git commit -m "Update graph"
git push -f
