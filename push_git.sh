#!/bin/bash
git checkout -b "$1"
git add .
git commit -m "Commit"
git push --set-upstream origin "$1"
