Deletes tags from a docker trusted registry.

```
usage: tagdel.py [-h] [-n] [-k KEEP] [-b BASEURL] -r REPO -u USER -t TOKEN
                 [-i IGNORE]

Delete, and keep latest -k/--keep tags from a docker trusted registry using REST API.

optional arguments:
  -h, --help            show this help message and exit
  -n, --noop            Show a count of tags that are expected to be deleted
                        and kept, then exit
  -k KEEP, --keep KEEP  Number of newest tags to keep
  -b BASEURL, --baseurl BASEURL
                        Base url to the registry, including protocol. Default:
                        "https://dtr.nrk.no"
  -r REPO, --repo REPO  The repository you want to perform operations on - Ex:
                        origo/folkemusikk
  -u USER, --user USER  Username to authenticate as
  -t TOKEN, --token TOKEN
                        Authentication token. Must be created in the registry.
  -i IGNORE, --ignore IGNORE
                        Tag to ignore/keep. Can be specified multiple times.
```

Example:

```
./tagdel.py  -k 10 -u <username> -t <token> -r origo/folkemusikk
```

Will delete all but the latest 10 tags. 
