/**
 * Proj4 Configuration for TWD97 Coordinate System
 * Registers Taiwan Datum 1997 (TWD97) projection
 */

import proj4 from 'proj4'
import { register } from 'ol/proj/proj4'

// Define TWD97 TM2 projection
// EPSG:3826 - TWD97 / TM2 zone 121
proj4.defs('EPSG:3826', '+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')

// Register with OpenLayers
register(proj4)

export default proj4
