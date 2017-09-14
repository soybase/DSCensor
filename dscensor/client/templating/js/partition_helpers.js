function ancestors(node) {
  var path = [];
  var current = node;
  while (current) {
    path.unshift(current['name']);
    current = current.parent;
  }
  return path;
}

function generateFilters(c, f){
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
        var filters = {'genes' : genes_group,
                           'exons' : exons_group,
                           'mrnas' : mrnas_group,
                           'pps'   : pps_group,
                           'ppds'  : ppds_group,
                           'chrs'  : chrs_group,
                           'lgs'   : lgs_group};
        return filters;
}
