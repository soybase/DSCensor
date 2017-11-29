function ancestors(node) {
  var path = [];
  var current = node;
  while (current) {
    path.unshift(current['name']);
    current = current.parent;
  }
  return path;
}

function histogramFilters(c, f){
        var genes_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.genes;
                }
            } else {
                return d.genes;
            }
        });
        var exons_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.exons;
                }
            } else {
                return d.exons;
            }
        });
        var mrnas_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.mrnas;
                }
            } else {
                return d.mrnas;
            }
        });
        var pps_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.pps;
                }
            } else {
                return d.pps;
            }
        });
        var ppds_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.ppds;
                }
            } else {
                return d.ppds;
            }
        });
        var chrs_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.chrs;
                }
            } else {
                return d.chrs;
            }
        });
        var lgs_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.lgs;
                }
            } else {
                return d.lgs;
            }
        });
        var cds_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d.cds;
                }
            } else {
                return d.cds;
            }
        });
        var filters = {'genes' : genes_group,
                           'exons' : exons_group,
                           'mrnas' : mrnas_group,
                           'pps'   : pps_group,
                           'ppds'  : ppds_group,
                           'chrs'  : chrs_group,
                           'lgs'   : lgs_group,
                           'cds'   : cds_group};
        return filters;
}

function scatterFilters(c, f, x, y){
    var xmax = 0
    var ymax = 0
    var scatdomain = c.dimension(
        function(d){
           return [d[x], d[y], d.label, d.org_genus, d.org_species];
        });
    var scatgroup = scatdomain.group(function(d){
        if (Object.keys(f).length > 0){
            if (f[d[2]]){
                if (d[0] > xmax){
                    xmax = d[0]
                }
                if (d[1] > ymax){
                    ymax = d[1]
                }
                return [d[0], d[1], d[2], d[3], d[4]];
            }
        } else {
            if (d[0] > xmax){
                xmax = d[0]
            }
            if (d[1] > ymax){
                ymax = d[1]
            }
            return [d[0], d[1], d[2], d[3], d[4]];
        }
    });
    xmax = xmax + Math.floor(xmax/5);
    ymax = ymax + Math.floor(ymax/10);
    scatfilters = {'dimension' : scatdomain, 'group' : scatgroup, 'xmax' : xmax, 'ymax' : ymax};
    return scatfilters;
}

