$(document).ready(function(){
    var acount = 0;
    var name_length = 0;
    var ordering = [];
    var organismFeatures = feature_counts.dimension(function(d){
        acount++;
        if (d.label.length > name_length){
            name_length = d.label.length;
        }
        ordering.push(d.label);
        return d.label;
    });
    var left_margin = name_length * 4 + 10;
    var bottom_margin = name_length * 4 + 10;
    var w = acount * 30 + left_margin + 60;
    console.log(feature_table_data);
    var organismFeaturesTable = $('#features-datatable').dataTable({
        "data": feature_table_data,
        "columns": feature_header,
        "colReorder" : {
            fixedColumnsLeft: 1
        },
        "search": {
            "caseInsensitive": true,
            "regex": true
        },
        "select" : true,
        "order" : []
    });
    var assemblyCounts = dc.barChart("#assemblyCounts-chart");
    var chromosomes = organismFeatures.group().reduceSum(function(d){
        return d.chrs;
    });
    var linkagegroups = organismFeatures.group().reduceSum(function(d){
        return d.lgs;
    });
    assemblyCounts
        .width(w)
        .height(600)
        .dimension(organismFeatures)
        .margins({top: 50, right: 50, bottom: bottom_margin, left: left_margin})
        .group(chromosomes, "Chromosomes")
        .x(d3.scale.ordinal().domain(ordering))
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Organism Identifier")
        .yAxisLabel("Chromosome Number and LGs")
        .stack(linkagegroups, "Linkage Groups")
        .transitionDuration(10)
        .legend((dc.legend().x(120).y(0).itemHeight(16).gap(4)))
        .on('renderlet', function(chart){
        chart.selectAll('rect').on('click.custom', function(d){
            var chartI = dc.chartRegistry.list('organismfeatures_group');
            var table = $('#features-datatable').DataTable();
            var rows = $("#features-datatable").dataTable()._('tr');
            for (var r = 0; r < rows.length; r++){
                if (rows[r][0] === d.x){
                    var indexes = table.rows().eq( 0 ).filter( function (rowIdx) {
                        return table.cell( rowIdx, 0 ).data() === d.x ? true : false;
                    });
                    if (table.rows(indexes).nodes().to$().hasClass('selected') === false){
                        table.rows(indexes)
                             .nodes()
                             .to$()
                             .addClass('selected');
                        console.log(rows[r], indexes);
                    } else {
                        table.rows(indexes)
                             .nodes()
                             .to$()
                             .removeClass('selected');
                    }
                }
            }
            for (var i = 0; i < chartI.length; i++) {
                if (chartI[i].chartName !== 'assemblycounts'){
                    chartI[i].filter(d.x);
                    console.log(chartI[i].chartName);
                }
            }
            dc.renderAll();
            console.log(d.x + "thing" + chartI);
        });	
    });
    assemblyCounts.chartName = 'assemblycounts';
    dc.chartRegistry.register(assemblyCounts, 'organismfeatures_group');
    console.log('this is counts' + assemblyCounts);

    var genomicCounts = dc.barChart("#genomicCounts-chart");
    var genes = organismFeatures.group().reduceSum(function(d){
        return d.genes;
    });
    var mrnas = organismFeatures.group().reduceSum(function(d){
        return d.mrnas;
    });
    var exons = organismFeatures.group().reduceSum(function(d){
        return d.exons;
    });
    var polypeptides = organismFeatures.group().reduceSum(function(d){
        return d.pps;
    });
    var polypeptide_domains = organismFeatures.group().reduceSum(function(d){
        return d.ppds;
    });
    genomicCounts
        .width(w)
        .height(600)
        .dimension(organismFeatures)
        .margins({top: 110, right: 50, bottom: bottom_margin, left: left_margin})
        .title(function(d){
            return d.key + ' ' + this.layer + ' ' + d.value;
        })
        .group(genes, 'Genes')
        .x(d3.scale.ordinal().domain(ordering))
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Organism Identifier")
        .yAxisLabel("Ontology Feature")
        .stack(mrnas, 'mRNAs')
        .stack(polypeptides, 'Polypeptides')
        .stack(polypeptide_domains, 'Polypeptide Domains')
        .stack(exons, 'Exons')
        .transitionDuration(10)
        .legend((dc.legend().x(120).y(0).itemHeight(16).gap(4)))
        .on('renderlet', function(chart){
        chart.selectAll('rect').on('click.custom', function(d){
            var chartI = dc.chartRegistry.list('organismfeatures_group');
            var table = $('#features-datatable').DataTable();
            var rows = $("#features-datatable").dataTable()._('tr');
            for (var r = 0; r < rows.length; r++){
                if (rows[r][0] === d.x){
                    var indexes = table.rows().eq( 0 ).filter( function (rowIdx) {
                        return table.cell( rowIdx, 0 ).data() === d.x ? true : false;
                    });
                    if (table.rows(indexes).nodes().to$().hasClass('selected') === false){
                        table.rows(indexes)
                             .nodes()
                             .to$()
                             .addClass('selected');
                        console.log(rows[r], indexes);
                    } else {
                        table.rows(indexes)
                             .nodes()
                             .to$()
                             .removeClass('selected');
                    }
                }
            }
            for (var i = 0; i < chartI.length; i++) {
                if (chartI[i].chartName !== 'genomiccounts'){
                    chartI[i].filter(d.x);
                    console.log(chartI[i].chartName);
                }
            }
            dc.renderAll();
            console.log(d.x + "thing" + chartI);
        });	
    });
    genomicCounts.chartName = 'genomiccounts';
    dc.chartRegistry.register(genomicCounts, 'organismfeatures_group');

    var markerCounts = dc.barChart("#markerCounts-chart");
    var markers = organismFeatures.group().reduceSum(function(d){
        return d.gms;
    });
    var primers = organismFeatures.group().reduceSum(function(d){
        return d.primers;
    });
    var qtls = organismFeatures.group().reduceSum(function(d){
        return d.qtls;
    });
    var syntenic_regions = organismFeatures.group().reduceSum(function(d){
        return d.syn_regs;
    });
    var consensus_regions = organismFeatures.group().reduceSum(function(d){
        return d.con_regs;
    });
    markerCounts
        .width(w)
        .height(700)
        .dimension(organismFeatures)
        .margins({top: 110, right: 50, bottom: bottom_margin, left: left_margin})
        .title(function(d){
            return d.key + ' ' + this.layer + ' ' + d.value;
        })
        .group(markers, 'Genetic Markers')
        .x(d3.scale.ordinal().domain(ordering))
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Organism Identifier")
        .yAxisLabel("Ontology Feature")
        .stack(primers, 'Primers')
        .stack(qtls, 'QTLs')
        .stack(syntenic_regions, 'Syntenic Regions')
        .stack(consensus_regions, 'Consensus Regions')
        .transitionDuration(10)
        .legend((dc.legend().x(120).y(0).itemHeight(16).gap(4)))
        .on('renderlet', function(chart){
        chart.selectAll('rect').on('click.custom', function(d){
            var chartI = dc.chartRegistry.list('organismfeatures_group');
            var table = $('#features-datatable').DataTable();
            var rows = $("#features-datatable").dataTable()._('tr');
            for (var r = 0; r < rows.length; r++){
                if (rows[r][0] === d.x){
                    var indexes = table.rows().eq( 0 ).filter( function (rowIdx) {
                        return table.cell( rowIdx, 0 ).data() === d.x ? true : false;
                    });
                    if (table.rows(indexes).nodes().to$().hasClass('selected') === false){
                        table.rows(indexes)
                             .nodes()
                             .to$()
                             .addClass('selected');
                        console.log(rows[r], indexes);
                    } else {
                        table.rows(indexes)
                             .nodes()
                             .to$()
                             .removeClass('selected');
                    }
                }
            }
            for (var i = 0; i < chartI.length; i++) {
                if (chartI[i].chartName !== 'markercounts'){
                    chartI[i].filter(d.x);
                    console.log(chartI[i].chartName);
                }
            }
            dc.renderAll();
            console.log(d.x + "thing" + chartI);
        });
    });
    markerCounts.chartName = 'markercounts';
    dc.chartRegistry.register(markerCounts, 'organismfeatures_group');
    dc.renderAll();

    var path = '';
    var dw = 800,
        dh = 800,
        x = d3.scale.linear().range([0, dw]),
        y = d3.scale.linear().range([0, dh]);	
    var vis = d3.select("#organism_partition").append("div")
      .attr("class", "chart")
      .attr("id", "organismPartition")
      .style("width", dw + "px")
      .style("height", dh + "px")
      .append("svg:svg")
      .attr("width", dw)
      .attr("height", dh);
    var partition = d3.layout.partition()
                      .value(function(d) { return d.count; });
    var colors = d3.scale.category20c();
    createchart(partition_data)

function createchart(root) {
    console.log(root);
    var g = vis.selectAll("g")
      .data(partition.nodes(root))
      .enter().append("svg:g")
      .attr("transform", function(d) { return "translate(" + x(d.y) + "," + y(d.x) + ")"; })
      .on("click", zoom);

    var kx = dw / root.dx,
        ky = dh / 1;

    g.append("svg:rect")
      .attr("width", root.dy * kx)
      .attr("height", function(d) { return d.dx * ky; })
      .attr("fill", function(d) {return colors(d.name)})
      .attr("class", function(d) { return d.children ? "parent" : "child"; });

    g.append("svg:text")
      .attr("transform", transform)
      .style("opacity", function(d) { return d.dx * ky < 12 ? 0 : 1 })
      .text(function(d) { if (d.parent){console.log(ancestors(d));};if(d.count){return d.name + ':' + d.count};if(d.name){return d.name; }})

    d3.select("#organism_partition")
      .on("click", function() { zoom(root); })

    function zoom(d) {
        console.log('clicked');
        if (!d.children){ reset_all(); return};
        kx = (d.y ? dw - 40 : dw) / (1 - d.y);
        var crums = d.name;
        if (d.parent){
            crums = ancestors(d);
            $('.counter').html(crums.join('/'));
        } else {
            $('.counter').html('At ROOT LEVEL Organisms');
        }
        console.log(crums);
        ky = dh / d.dx;
        x.domain([d.y, 1]).range([d.y ? 40 : 0, dw]);
        y.domain([d.x, d.x + d.dx]);
        var t = g.transition()
                 .duration(750)
                 .attr("transform", 
                  function(d) {
                      return "translate(" + x(d.y) + "," + y(d.x) + ")"; 
        });

        t.select("rect")
         .attr("width", d.dy * kx)
         .attr("height", function(d) { return d.dx * ky; });

        t.select("text")
         .attr("transform", transform)
         .style("opacity", function(d) { return d.dx * ky < 12 ? 0 : 1 });

        d3.event.stopPropagation();

        var searchstr = "";
        var s = [];
        var r = {};
        var table = $('#features-datatable').DataTable();
        var chartI = dc.chartRegistry.list('organismfeatures_group');
        if (d.depth === 0){
            reset_all();return
        }
        if (d.depth === 1){
            for (var i=0;i<d.children.length;i++){
                console.log(d.children[i])
                r[d.children[i].name] = 1;
                if (searchstr.length < 1){
                    searchstr = '(' + d.children[i].name + ')[^\\S+]';
                } else {
                    searchstr += '|(' + d.children[i].name + ')[^\\S+]';
                }
            }
        }
        if (d.depth === 2){
            searchstr = '(' + d.name + ')[^\\S+]';
            r[d.name] = 1;
        }
        table.search(searchstr, 1, true, false).draw();
        var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
        for (i=0;i<rows.length;i++){
            s.push(rows[i][0]);
        }
        var len = s.length;
        w = (len * 30) + left_margin + 60;
        console.log(len, w);
        for (var i = 0;i<chartI.length; i++){
            if (chartI[i].chartName === 'assemblycounts'){
                var chromosomes_filter = organismFeatures.group().reduceSum(function(d){
                     if (r[d.label] === 1){
                         return d.chrs;
                     }
                });
                var linkagegroups_filter = organismFeatures.group().reduceSum(function(d){
                     if (r[d.label] === 1){
                         return d.lgs;
                     }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(chromosomes_filter, "Chromosomes");
                chartI[i].stack(linkagegroups_filter, "Linkage Groups")
                chartI[i].filter(null);
            }
            else if (chartI[i].chartName === 'genomiccounts') {
                var genes_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.genes;
                    }
                });
                var mrnas_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.mrnas;
                    }
                });
                var exons_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.exons;
                    }
                });
                var polypeptides_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.pps;
                    }
                });
                var polypeptide_domains_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.ppds;
                    }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(genes_filter, "Genes");
                chartI[i].stack(mrnas_filter, 'mRNAs')
                chartI[i].stack(polypeptides_filter, 'Polypeptides')
                chartI[i].stack(polypeptide_domains_filter, 'Polypeptide Domains')
                chartI[i].stack(exons_filter, 'Exons')
                chartI[i].filter(null);
            }
            else if (chartI[i].chartName === 'markercounts') {
                var markers_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.gms;
                    }
                });
                var primers_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.primers;
                    }
                });
                var qtls_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.qtls;
                    }
                });
                var syntenic_regions_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.syn_regs;
                    }
                });
                var consensus_regions_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.con_regs;
                    }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(markers_filter, "Genetic Markers");
                chartI[i].stack(primers_filter, 'Primers')
                chartI[i].stack(qtls_filter, 'QTLs')
                chartI[i].stack(syntenic_regions_filter, 'Syntenic Regions')
                chartI[i].stack(consensus_regions_filter, 'Consensus Regions')
                chartI[i].filter(null);
            }
        }
        table.rows('.selected').deselect();
        dc.renderAll();
    }

	function transform(d) {
        return "translate(8," + d.dx * ky / 2 + ")";
    }
}

    $("#reset-features").click(reset_all);

    function reset_all(){
        var d = partition_data;
        console.log('resetting:', this);
        var g = vis.selectAll("g");
        if (!d.children){ reset_all(); return};
        kx = (d.y ? dw - 40 : dw) / (1 - d.y);
        var crums = d.name;
        if (d.parent){
            crums = ancestors(d);
            $('.counter').html(crums.join('/'));
        } else {
            $('.counter').html('At ROOT LEVEL Organisms');
        }
        console.log(crums);
        ky = dh / 1;
        x.domain([d.y, 1]).range([d.y ? 40 : 0, dw]);
        y.domain([d.x, d.x + d.dx]);
        var t = g.transition()
                 .duration(750)
                 .attr("transform",
                  function(d) {
                      return "translate(" + x(d.y) + "," + y(d.x) + ")";
        });

        t.select("rect")
         .attr("width", d.dy * kx)
         .attr("height", function(d) { return d.dx * ky; });

        t.select("text")
         .attr("transform", function(d) { return "translate(8," + d.dx * ky / 2 + ")"; })
         .style("opacity", function(d) { return d.dx * ky < 12 ? 0 : 1 });

        var table = $('#features-datatable').DataTable();
        var chartI = dc.chartRegistry.list('organismfeatures_group');
        table.rows('.selected').deselect();
        table.search("").draw();
        var len = $("#features-datatable").dataTable()._('tr').length;
        var w = len * 30 + left_margin + 60;
        for (var i = 0; i < chartI.length; i++) {
            if (chartI[i].chartName === 'assemblycounts'){
                var chromosomes = organismFeatures.group().reduceSum(function(d){
                     return d.chrs;
                });
                var linkagegroups = organismFeatures.group().reduceSum(function(d){
                     return d.lgs;
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(ordering));
                chartI[i].group(chromosomes, "Chromosomes");
                chartI[i].stack(linkagegroups, "Linkage Groups")
                chartI[i].filter(null);
            }
            else if (chartI[i].chartName === 'genomiccounts') {
                var genes = organismFeatures.group().reduceSum(function(d){
                    return d.genes;
                });
                var mrnas = organismFeatures.group().reduceSum(function(d){
                    return d.mrnas;
                });
                var exons = organismFeatures.group().reduceSum(function(d){
                    return d.exons;
                });
                var polypeptides = organismFeatures.group().reduceSum(function(d){
                    return d.pps;
                });
                var polypeptide_domains = organismFeatures.group().reduceSum(function(d){
                    return d.ppds;
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(ordering));
                chartI[i].group(genes, "Genes");
                chartI[i].stack(mrnas, 'mRNAs')
                chartI[i].stack(polypeptides, 'Polypeptides')
                chartI[i].stack(polypeptide_domains, 'Polypeptide Domains')
                chartI[i].stack(exons, 'Exons')
                chartI[i].filter(null);
            }
            else if (chartI[i].chartName === 'markercounts') {
                var markers = organismFeatures.group().reduceSum(function(d){
                    return d.gms;
                });
                var primers = organismFeatures.group().reduceSum(function(d){
                    return d.primers;
                });
                var qtls = organismFeatures.group().reduceSum(function(d){
                    return d.qtls;
                });
                var syntenic_regions = organismFeatures.group().reduceSum(function(d){
                    return d.syn_regs;
                });
                var consensus_regions = organismFeatures.group().reduceSum(function(d){
                    return d.con_regs;
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(ordering));
                chartI[i].group(markers, "Genetic Markers");
                chartI[i].stack(primers, 'Primers')
                chartI[i].stack(qtls, 'QTLs')
                chartI[i].stack(syntenic_regions, 'Syntenic Regions')
                chartI[i].stack(consensus_regions, 'Consensus Regions')
                chartI[i].filter(null);
            }
        }
        dc.redrawAll();
        table.clear();
        table.rows.add(feature_table_data).order([]).draw();
    }

    $('#features-datatable tbody').on('click', 'tr', function(){
        var chartI = dc.chartRegistry.list('organismfeatures_group');
        var rows = $('#features-datatable').DataTable().rows('.selected').data();
        console.log($(this)[0].getElementsByTagName('td')[0].innerText);
        var filtered_samples = organismFeatures.top(Infinity);
        console.log(filtered_samples);
        for (var j = 0;j<chartI.length; j++){
            chartI[j].filter(null)
            for (var i = 0;i<rows.length; i++){
                chartI[j].filter(rows[i][0]);
            }
        }
        dc.redrawAll();
    });

    $('#features-datatable thead').on('click', 'th', function(){
        var s = [];
        var chartI = dc.chartRegistry.list('organismfeatures_group');
        var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
        for (var i = 0;i<rows.length;i++){
            s.push(rows[i][0]);
        }
        for (var i = 0;i<chartI.length; i++){
            chartI[i].x(d3.scale.ordinal().domain(s));
        }
        dc.redrawAll();
    });

    $("#features-datatable_filter input").on('keyup', function(k){
        var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
        var chartI = dc.chartRegistry.list('organismfeatures_group');
        var s = [];
        var r = {};
        for (var i = 0;i<rows.length;i++){
            s.push(rows[i][0]);
            r[rows[i][0]] = 1;
        }
        var len = rows.length;
        w = (len * 30) + left_margin + 60;
        for (var i = 0;i<chartI.length; i++){
            if (chartI[i].chartName === 'assemblycounts'){
                var chromosomes_filter = organismFeatures.group().reduceSum(function(d){
                     if (r[d.label] === 1){
                         return d.chrs;
                     }
                });
                var linkagegroups_filter = organismFeatures.group().reduceSum(function(d){
                     if (r[d.label] === 1){
                         return d.lgs;
                     }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(chromosomes_filter, "Chromosomes");
                chartI[i].stack(linkagegroups_filter, "Linkage Groups")
            }
            else if (chartI[i].chartName === 'genomiccounts') {
                var genes_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.genes;
                    }
                });
                var mrnas_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.mrnas;
                    }
                });
                var exons_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.exons;
                    }
                });
                var polypeptides_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.pps;
                    }
                });
                var polypeptide_domains_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.ppds;
                    }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(genes_filter, "Genes");
                chartI[i].stack(mrnas_filter, 'mRNAs')
                chartI[i].stack(polypeptides_filter, 'Polypeptides')
                chartI[i].stack(polypeptide_domains_filter, 'Polypeptide Domains')
                chartI[i].stack(exons_filter, 'Exons')
            }
            else if (chartI[i].chartName === 'markercounts') {
                var markers_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.gms;
                    }
                });
                var primers_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.primers;
                    }
                });
                var qtls_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.qtls;
                    }
                });
                var syntenic_regions_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.syn_regs;
                    }
                });
                var consensus_regions_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.con_regs;
                    }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(markers_filter, "Genetic Markers");
                chartI[i].stack(primers_filter, 'Primers')
                chartI[i].stack(qtls_filter, 'QTLs')
                chartI[i].stack(syntenic_regions_filter, 'Syntenic Regions')
                chartI[i].stack(consensus_regions_filter, 'Consensus Regions')
            }
        }
        dc.renderAll();
    });

    $("#filter-features").click(function(d){
        var searchstr = "";
        var s = [];
        var r = {};
        var rows = $('#features-datatable').DataTable().rows('.selected').data();
        var table = $('#features-datatable').DataTable();
        var chartI = dc.chartRegistry.list('organismfeatures_group');
        if (rows.length === 0){
            return 0
        }
        for (var i=0;i<rows.length;i++){
            s.push(rows[i][0]);
            r[rows[i][0]] = 1;
            if (searchstr.length < 1){
                searchstr = '(' + rows[i][0] + ')[^\\S+]';
            } else {
                searchstr += '|(' + rows[i][0] + ')[^\\S+]';
            }
        }
        var len = rows.length;
        w = (len * 30) + left_margin + 60;
        table.search(searchstr, 1, true, false).draw();
        for (var i = 0;i<chartI.length; i++){
            if (chartI[i].chartName === 'assemblycounts'){
                var chromosomes_filter = organismFeatures.group().reduceSum(function(d){
                     if (r[d.label] === 1){
                         return d.chrs;
                     }
                });
                var linkagegroups_filter = organismFeatures.group().reduceSum(function(d){
                     if (r[d.label] === 1){
                         return d.lgs;
                     }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(chromosomes_filter, "Chromosomes");
                chartI[i].stack(linkagegroups_filter, "Linkage Groups")
                chartI[i].filter(null);
            }
            else if (chartI[i].chartName === 'genomiccounts') {
                var genes_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.genes;
                    }
                });
                var mrnas_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.mrnas;
                    }
                });
                var exons_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.exons;
                    }
                });
                var polypeptides_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.pps;
                    }
                });
                var polypeptide_domains_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.ppds;
                    }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(genes_filter, "Genes");
                chartI[i].stack(mrnas_filter, 'mRNAs')
                chartI[i].stack(polypeptides_filter, 'Polypeptides')
                chartI[i].stack(polypeptide_domains_filter, 'Polypeptide Domains')
                chartI[i].stack(exons_filter, 'Exons')
                chartI[i].filter(null);
            }
            else if (chartI[i].chartName === 'markercounts') {
                var markers_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.gms;
                    }
                });
                var primers_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.primers;
                    }
                });
                var qtls_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.qtls;
                    }
                });
                var syntenic_regions_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.syn_regs;
                    }
                });
                var consensus_regions_filter = organismFeatures.group().reduceSum(function(d){
                    if (r[d.label] === 1){
                        return d.con_regs;
                    }
                });
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                chartI[i].group(markers_filter, "Genetic Markers");
                chartI[i].stack(primers_filter, 'Primers')
                chartI[i].stack(qtls_filter, 'QTLs')
                chartI[i].stack(syntenic_regions_filter, 'Syntenic Regions')
                chartI[i].stack(consensus_regions_filter, 'Consensus Regions')
                chartI[i].filter(null);
            }
        }
        table.rows('.selected').deselect();
        dc.renderAll();
    });

    $('a.toggle-vis').on('click', function(e){
        e.preventDefault();
        var column = $("#features-datatable").DataTable().column(':contains(' + $(this).attr('data-column') + ')');
        column.visible(! column.visible());
        color_anchors($(this));
    });
});
