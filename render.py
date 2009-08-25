#!/usr/bin/env python
# -*- coding: utf-8; mode: Python -*-

__version__ = '0.1'

import logging
import optparse
import sys, os

import ocitysmap

def main():
    usage = '%prog [options] <cityname> [lat1,long1 lat2,long2]'
    parser = optparse.OptionParser(usage=usage,
                                   version='%%prog %s' % __version__)
    parser.add_option('-o', '--output', dest='output', metavar='FILE',
                      default='citymap.svg',
                      help='Specify the output file name (defaults '
                           'to citymap.svg.')
    parser.add_option('-z', '--zoom', dest='zooms', action='append',
                      nargs=3, metavar='NAME BBOX',
                      help='Specify a zoomed section by its named '
                           'bounding box.')
    parser.add_option('-m', '--osm', dest='osm_map', metavar='PATH',
                      help='Path to the osm.xml file')

    (options, args) = parser.parse_args()
    if len(args) != 1 and len(args) != 3:
        parser.print_help()
        return 1

    if not options.osm_map:
        try:
            options.osm_map = os.environ['OSM_XML']
        except KeyError:
            parser.error("Invalid -m option and no OSM_XML env var")

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Parse bounding box arguments
    zooms = {}
    if options.zooms:
        for zoom in options.zooms:
            try:
                zooms[zoom[0]] = ocitysmap.BoundingBox.parse(zoom[1:])
            except ValueError:
                sys.stderr.write('ERROR: Invalid bounding box for zoom section %s!\n' % zoom[0])
                return 1

    boundingbox = None
    try:
        boundingbox = ocitysmap.BoundingBox.parse(args[1:])
    except ValueError:
        sys.stderr.write('ERROR: Invalid city bounding box!\n')
        return 1

    try:
        renderer = ocitysmap.OCitySMap(args[0], boundingbox, zooms)
    except ocitysmap.BaseOCitySMapError, e:
        sys.stderr.write('ERROR: %s\n' % e)
        return 1
    except KeyboardInterrupt:
        sys.stderr.write(' Aborting.\n')

    renderer.render_to_file(options.osm_map, options.output)
    return 0

if __name__ == '__main__':
    sys.exit(main())