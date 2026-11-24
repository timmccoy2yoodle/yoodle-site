# yoodle.com
Static site. `python3 tools/build.py` writes `site/` (Netlify publish folder). `--preview` writes a flat review copy.
Content lives in `tools/data.py`. QA: `NODE_PATH=$(npm root -g) node qa/qa.cjs site qa/out` (must print 0 problems).
`TEST_BUILD = True` in build.py keeps the site noindex until launch.
