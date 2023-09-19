# TVDB Scraper
Script used to extract the names of individual episodes from shows into a dictionary (using the TVDB site). Will automatically use said dictionary to replace file names.

Requires following file structure: /ShowName/Season x/EXX.filename (e.g. /House/Season 2/E03.mkv -> /House/Season 2/E03 Humpty Dumpty.mkv)

Plans:
* Adapt so it works for single season shows
* Add json or ini support in lieu of a settings file (to indicate range of seasons, format of episode number, etc)
