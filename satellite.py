#!/usr/bin/env python2
import argparse
import datetime
import requests
import ephem
from math import degrees
from urllib import quote_plus


def process(lines):
    try:
        iss = ephem.readtle(str(lines[0]), str(lines[1]), str(lines[2]))
    except:
        return ""

    # Compute for now
    now = datetime.datetime.utcnow()
    iss.compute(now)
    name = lines[0].replace(" ", "").replace("'", "")
    lon = degrees(iss.sublong)
    lat = degrees(iss.sublat)
    elev = int(iss.elevation*1000)
    td = (now - datetime.datetime(1970, 1, 1))
    ts = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)
    return "{0}/{1}:{2}/{3} celestrak.stations{{name={4}}} T\n".format(
        ts, lat, lon, elev, quote_plus(name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", default="stations.metrics", help="Set the output file")

    args = parser.parse_args()

    lines = []
    res = requests.get("http://www.celestrak.com/NORAD/elements/stations.txt")
    file = open(args.output, "w")
    for line in res.iter_lines():
        lines.append(line)

        if len(lines) >= 3:
            file.write(process(lines))
            lines = []

    if len(lines) > 0:
        file.write(process(lines))

    file.close()


if __name__ == '__main__':
    main()
