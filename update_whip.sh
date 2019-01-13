#!/usr/bin/env bash
python3 scrapper.py update
python3 prepare.py
Rscript make_graph.R