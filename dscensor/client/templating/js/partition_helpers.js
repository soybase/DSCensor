function linkoutCaller(target, done){
    var oReq = new XMLHttpRequest();
    console.log('my target ' + target);
    oReq.open('GET', 'https://legumeinfo.org/gene_links/' + target + '/json', true);
    oReq.onload = function(){
        done(null, JSON.parse(oReq.responseText));
    }
    oReq.onerror = function(){
        done(oReq.response);
    }
    oReq.send();
}

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
        var utr_3p_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['3p_utrs'];
                }
            } else {
                return d['3p_utrs'];
            }
        });
        var utr_5p_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['5p_utrs'];
                }
            } else {
                return d['5p_utrs'];
            }
        });
        var scaffolds_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['scaffolds'];
                }
            } else {
                return d['scaffolds'];
            }
        });
        var contigs_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['contigs'];
                }
            } else {
                return d['contigs'];
            }
        });
        var N50_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['N50'];
                }
            } else {
                return d['N50'];
            }
        });
        var allbases_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['allbases'];
                }
            } else {
                return d['allbases'];
            }
        });
        var gaps_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['gaps'];
                }
            } else {
                return d['gaps'];
            }
        });
        var records_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['records'];
                }
            } else {
                return d['records'];
            }
        });
        var gapbases_group = c.group().reduceSum(function(d){
            if (Object.keys(f).length > 0){
                if (f[d.label]){
                    return d['gapbases'];
                }
            } else {
                return d['gapbases'];
            }
        });

        var filters = {'genes' : genes_group,
                           'exons' : exons_group,
                           'mrnas' : mrnas_group,
                           'pps'   : pps_group,
                           'ppds'  : ppds_group,
                           'chrs'  : chrs_group,
                           'lgs'   : lgs_group,
                           'cds'   : cds_group,
                           '3p_utrs' : utr_3p_group,
                           '5p_utrs' : utr_5p_group,
                           'scaffolds' : scaffolds_group,
                           'contigs' : contigs_group,
                           'N50' : N50_group,
                           'allbases' : allbases_group,
                           'gaps' : gaps_group,
                           'records' : records_group,
                           'gapbases' : gapbases_group};
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

