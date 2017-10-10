# Roadmap

The following list is a rough plan with the next big steps that should be done.

## Edit https://github.com/gammapy/gamma-cat/README.md

Add of a short paragraph as starting point for new contributors who have no idea about gamma-cat.

The main starting point is a reference to the documentation in https://gamma-cat.readthedocs.io

## Edit https://gamma-cat.readthedocs.io

- Add of detailed but easy description of the structure of the input yaml and ecsv files. Main goal is that unexperienced contributors can start adding data within a few minutes. 

- Add of a "Workflow" which should contain the fork-branch-pullrequest way of git and some formal things like running make.py checks before 
opening the pull request. 

- The documentation has to contain a reference to this file here, too!

- Description of how to access the data via gammapy.catalog.gammacat or reference to documentation of gammapy and there a detailed description

## Overview about all HESS sources

Create a .md file, e.g. in https://github.com/gammapy/gamma-cat/todo, which lists all(!) sources that have been seen by HESS, their references and the status of the corresponding yaml- and ecsv- input files. <br />
This point includes a cleanup of https://github.com/gammapy/gamma-cat/blob/master/todo/todo_hess_aux.md and of
https://github.com/gammapy/gamma-cat/blob/master/todo/todo_missing_hgps_sources.md which are currently not up to date with the input files! <br />
When this is finished one should release gamma-cat as version 0.1

## Overview about all MAGIC sources

Create a .md file, e.g. in https://github.com/gammapy/gamma-cat/todo, which lists all(!) sources that have been seen by MAGIC, their references and the status of the corresponding yaml- and ecsv- input files. <br />
This is highly connected to https://github.com/gammapy/gamma-cat/issues/157 which is not easy readable.
When this is finished one should release gamma-cat as version 0.2

## Overview about all VERITAS sources

Create a .md file, e.g. in https://github.com/gammapy/gamma-cat/todo, which lists all(!) sources that have been seen by VERITAS, their references and the status of the corresponding yaml- and ecsv- input files. <br />
When this is finished one should release gamma-cat as version 0.3