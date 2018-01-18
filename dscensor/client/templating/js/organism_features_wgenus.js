var histogramSelection = {'cds' : 'CDS', 'genes' : 'Genes', 'exons' : 'Exons', 'mrnas' : 'mRNAs', 'pps' : 'Polypeptides', 'ppds' : 'Polypeptide Domains', 'chrs' : 'Chromosomes', 'lgs' : 'Linkage Groups', 'gms' : 'Genetic Markers', 'primers' : 'Primers', 'qtls' : 'QTLs', 'con_regs' : 'Consensus Regions', 'syn_regs' : 'Syntenic Regions', '3p_utrs' : "3' UTR", '5p_utrs': "5' UTR", 'scaffolds' : 'Scaffolds', 'contigs' : 'Contigs', 'N50' : 'N50', 'allbases' : 'All Bases', 'gaps' : 'Gaps', 'gapbases' : 'Gap Bases', 'records' : 'Fasta Records'};
var global_domain_filter = {};
var sunburst_on = 1;
var features_filter = ['genes'];
var scatx = 'exons';
var scaty = 'genes';
if (page_type === 'fasta'){
    features_filter = ['scaffolds'];
    scatx = 'scaffolds';
    scaty = 'contigs';
}
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
    var scatw = 800;
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
    $("#feature_body").append(histogram_selector);
    $("#feature_body").append(scatter_selector);
    var customHistogram1 = dc.barChart("#customHistogram-1");
    customHistogram1
        .width(w)
        .height(600)
        .dimension(organismFeatures)
        .margins({top: 50, right: 50, bottom: bottom_margin, left: left_margin})
        .x(d3.scale.ordinal().domain(ordering))
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Organism Identifier")
        .yAxisLabel("Counts");
    var count = 0;
    var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
    for (var i = 0;i<histogramSelection.length;i++){
       var k_label = histogramSelection[i].label;
       var k_key = histogramSelection[i].key;
       var k_plot = histogramSelection[i].show;
       if(k_plot === true){
           if (count == 0){
               customHistogram1.group(histogram_filters[k_key], k_label);
           } else {
               customHistogram1.stack(histogram_filters[k_key], k_label);
           }
           count++;
        }
    }
    customHistogram1
        .group(histogram_filters[features_filter[0]], histogramSelection[features_filter[0]])
        .transitionDuration(10)
        .legend((dc.legend().x(40).y(0).itemHeight(16).gap(4)))
        .elasticY(true)
        .on('renderlet', function(chart){
        chart.selectAll('rect').on('click.custom', function(d){
            var chartI = dc.chartRegistry.list('histogramfeatures_group');
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
                if (chartI[i].chartName !== 'customHistogram1'){
                    chartI[i].filter(d.x);
                    console.log(chartI[i].chartName);
                }
            }
            dc.renderAll();
            console.log(d.x + "thing" + chartI);
        });
    });
    customHistogram1.chartName = 'customHistogram1';
    dc.chartRegistry.register(customHistogram1, 'histogramfeatures_group');
    var customScatter1 = dc.scatterPlot("#customScatter-1")
    var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
    customScatter1
        .width(scatw)
        .height(600)
        .dimension(scatter_filters['dimension'])
        .group(scatter_filters['group'])
        .margins({top: 50, right: 100, bottom: 75, left: left_margin - 40})
        .symbolSize(8)
        .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
        .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
        .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
        .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1))
        .colorAccessor(function(d){
            if (d){
                var scat_color = taxonChroma.get(d.key[3] + ' ' + d.key[4])
                return scat_color
            }
        })
        .colors(function(d){
            return d
        });
    customScatter1.chartName = 'customScatter1';
    dc.chartRegistry.register(customScatter1, 'scatterfeatures_group');
    dc.renderAll();
    create_sunburst();

function create_icicle(){
    var dw = 1000,
        dh = 1000,
        x = d3.scale.linear().range([0, dw]),
        y = d3.scale.linear().range([0, dh]);
    var vis = d3.select('#partition_display').append('svg')
                .attr("width", dw)
                .attr("height", dh);
    var partition = d3.layout.partition()
                      .value(function(d) { return d.count; });
    var colors = d3.scale.category20c();
    createchart(partition_data);

    function createchart(root) {
        var g = vis.selectAll("g")
          .data(partition.nodes(root))
          .enter().append("svg:g")
          .attr("transform", function(d) { return "translate(" + x(d.y) + "," + y(d.x) + ")"; })
          .on("click", zoom);

        var kx = dw / root.dx,
            ky = dh;

        g.append("svg:rect")
          .attr("width", root.dy * kx)
          .attr("height", function(d) { return d.dx * ky; })
          .attr("fill", function(d) {if (d.color){console.log(d.color + ' ' + taxonChroma.get(d.color));return taxonChroma.get(d.color)};return colors(d.name)})

        g.append("svg:text")
          .attr("transform", transform)
          .style("opacity", function(d) { return d.dx * ky < 15 ? 0 : 1 })
          .style("font-size", function(d) { console.log(d.dy, d.y, d.dx, d.x, d.dy * 100 / d.name.length + 'rem');return d.dx > 0.06 ? "1em" : "1rem";return "1em";})
          .text(function(d) { if (d.parent){console.log(ancestors(d));};if(d.count){return d.name + ':' + d.number};if(d.name){return d.name; }})

        d3.select("#partition_display")
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
                     .duration(500)
                     .attr("transform",
                      function(d) {
                          return "translate(" + x(d.y) + "," + y(d.x) + ")";
                      });
            t.select("rect")
             .attr("width", d.dy * kx)
             .attr("height", function(d) { return d.dx * ky; });

            t.select("text")
             .attr("transform", transform)
             .style("opacity", function(d) { return d.dx * ky < 15 ? 0 : 1 });

            d3.event.stopPropagation();
            var searchstr = "";
            var s = [];
            global_domain_filter = {};
            var table = $('#features-datatable').DataTable();
            var chartI = dc.chartRegistry.list('histogramfeatures_group');
            var chartJ = dc.chartRegistry.list('scatterfeatures_group');
            if (d.depth === 0){
                reset_all();return
            }
            if (d.depth === 1){
                for (var i=0;i<d.children.length;i++){
                    var cstep = d.children[i]
                    for (var j=0;j<cstep.children.length;j++){
                        global_domain_filter[cstep.children[j].name] = 1;
                        if (searchstr.length < 1){
                            searchstr = '(' + cstep.children[j].name + ')[^\\S+]';
                        } else {
                            searchstr += '|(' + cstep.children[j].name + ')[^\\S+]';
                        }
                    }
                }
            }
            if (d.depth === 2){
                for (var i=0;i<d.children.length;i++){
                    global_domain_filter[d.children[i].name] = 1;
                    if (searchstr.length < 1){
                        searchstr = '(' + d.children[i].name + ')[^\\S+]';
                    } else {
                        searchstr += '|(' + d.children[i].name + ')[^\\S+]';
                    }
                }
            }
            if (d.depth === 3){
                searchstr = '(' + d.name + ')[^\\S+]';
                global_domain_filter[d.name] = 1;
            }
            table.search(searchstr, 1, true, true).draw();
            var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
            for (i=0;i<rows.length;i++){
                s.push(rows[i][0]);
            }
            var len = s.length;
            w = (len * 30) + left_margin + 60;
            var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
            for (var i = 0;i<chartI.length; i++){
                var count = 0;
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                for (var j=0;j<features_filter.length;j++){
                    var key = features_filter[j];
                    if (count === 0){
                        chartI[i].group(histogram_filters[key], histogramSelection[key]);
                    } else {
                        chartI[i].stack(histogram_filters[key], histogramSelection[key]);
                    }
                    count++;
                }
                chartI[i].filter(null);
            }
            var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
            for (var i = 0;i<chartJ.length; i++){
                var count = 0;
                chartJ[i].group(scatter_filters['group'])
                    .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
                    .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
                    .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
                    .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1));
            }
            table.rows('.selected').deselect();
            dc.renderAll();
        }
        function transform(d) {
            return "translate(8," + d.dx * ky / 2 + ")";
        }
    }
}
function create_sunburst(){
    var width = 1000,
        height = 1000,
        pi = Math.PI,
        r = Math.min(width, height) / 2;

    var x = d3.scale.linear()
        .range([0, 2 * pi]);

    var y = d3.scale.linear()
        .range([0, r]);

    var svg = d3.select('#partition_display').append('svg')
        .attr("width", width)
        .attr("height", height)
        .append("g")
          .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + ")");

    var arc = d3.svg.arc()
        .startAngle(function(d) { return Math.max(0, Math.min(2 * pi, x(d.x))); })
        .endAngle(function(d) { return Math.max(0, Math.min(2 * pi, x(d.x + d.dx))); })
        .innerRadius(function(d) { return Math.max(0, y(d.y)); })
        .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });

    var partition = d3.layout.partition()
                             .value(function(d) { return d.count; });
    var colors = d3.scale.category20c();
    createchart(partition_data);

    function createchart(root) {
        var g = svg.selectAll("g")
          .data(partition.nodes(root))
          .enter().append("g");

        var path = g.append("path")
          .attr("d", arc)
          .style("fill", function(d) { if (d.color){return taxonChroma.get(d.color)};return colors(d.name);})
          .on("click", zoom);

        var text = g.append("text")
          .attr("x", function(d) { return y(d.y); })
          .attr("transform", function(d) { return "rotate(" + rotateText(d) + ")"; })
          .style("font-size", function(d) {return d.dx > 0.06 ? "1em" : "1rem";return "1em";})
          .text(function(d) { var name = d.name;var twidth = (d.dy*width/2)/7;if(d.name.length >= twidth){name = d.name.substring(0, Math.ceil(twidth)) + "...";};if(d.count){return name + ':' + d.number};if(d.name){return name; }});
    d3.select("#partition_display")
          .on("click", function() { zoom(root); });
    // Free code from Metmajer's Zoomable Sunburst Example MIT license
        function zoom(d) {
            text.attr("opacity", 0);
            if (!d.children){ reset_all(); return};
            path.transition()
              .duration(350)
              .attrTween("d", arcTween(d))
              .each("end", function(e, i) {
              // check if the animated element's data e lies within the visible angle span given in d
                  if (e.x >= d.x && e.x < (d.x + d.dx)) {
                      // get a selection of the associated text element
                      var arcText = d3.select(this.parentNode).select("text");
                      // fade in the text element and recalculate positions
                      arcText.transition().duration(350)
                          .attr("opacity", 1)
                          .attr("transform", function() { return "rotate(" + rotateText(e) + ")" })
                          .attr("x", function(d) { return y(d.y); })
                          .text(function(d) { var name = d.name;var twidth = (d.depth * 5) + (d.dy*width/2)/7;if(d.name.length >= twidth){name = d.name.substring(0, Math.ceil(twidth)) + "...";};if(d.count){return name + ':' + d.number};if(d.name){return name; }});
                  }
              });
            d3.event.stopPropagation();
            //Controlls for table and figures
            var searchstr = "";
            var s = [];
            global_domain_filter = {};
            var table = $('#features-datatable').DataTable();
            var chartI = dc.chartRegistry.list('histogramfeatures_group');
            var chartJ = dc.chartRegistry.list('scatterfeatures_group');
            if (d.depth === 0){
                reset_all();return
            }
            if (d.depth === 1){
                for (var i=0;i<d.children.length;i++){
                    var cstep = d.children[i]
                    for (var j=0;j<cstep.children.length;j++){
                        global_domain_filter[cstep.children[j].name] = 1;
                        if (searchstr.length < 1){
                            searchstr = '(' + cstep.children[j].name + ')[^\\S+]';
                        } else {
                            searchstr += '|(' + cstep.children[j].name + ')[^\\S+]';
                        }
                    }
                }
            }
            if (d.depth === 2){
                for (var i=0;i<d.children.length;i++){
                    global_domain_filter[d.children[i].name] = 1;
                    if (searchstr.length < 1){
                        searchstr = '(' + d.children[i].name + ')[^\\S+]';
                    } else {
                        searchstr += '|(' + d.children[i].name + ')[^\\S+]';
                    }
                }
            }
            if (d.depth === 3){
                searchstr = '(' + d.name + ')[^\\S+]';
                global_domain_filter[d.name] = 1;
            }
            table.search(searchstr, 1, true, true).draw();
            var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
            for (i=0;i<rows.length;i++){
                s.push(rows[i][0]);
            }
            var len = s.length;
            w = (len * 30) + left_margin + 60;
            var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
            for (var i = 0;i<chartI.length; i++){
                var count = 0;
                chartI[i].width(w);
                chartI[i].x(d3.scale.ordinal().domain(s));
                for (var j=0;j<features_filter.length;j++){
                    var key = features_filter[j];
                    if (count === 0){
                        chartI[i].group(histogram_filters[key], histogramSelection[key]);
                    } else {
                        chartI[i].stack(histogram_filters[key], histogramSelection[key]);
                    }
                    count++;
                }
                chartI[i].filter(null);
            }
            var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
            for (var i = 0;i<chartJ.length; i++){
                var count = 0;
                chartJ[i].group(scatter_filters['group'])
                    .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
                    .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
                    .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
                    .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1));
            }
            table.rows('.selected').deselect();
            dc.renderAll();
        }
    }
    d3.select("#partition_display").style("height", height + "px");

    function rotateText(d) {
        return (x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180;
    }
    // Free code from Metmajer's Zoomable Sunburst Example MIT license
    // Interpolate the scales!
    function arcTween(d) {
        var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
            yd = d3.interpolate(y.domain(), [d.y, 1]),
            yr = d3.interpolate(y.range(), [d.y ? 20 : 0, r]);
        return function(d, i) {
            return i
                ? function(t) { return arc(d); }
                : function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); return arc(d); };
        };
    }
}
    $("#reset-features").click(reset_all);

    function reset_all(){
        var d = partition_data;
        var svgs = d3.select('svg').remove();
        if (sunburst_on === 1){
            create_sunburst();
        } else {
            create_icicle();
        }
        var width = 1000,
            height = 1000,
            r = Math.min(width, height) / 2;

        var x = d3.scale.linear()
            .range([0, 2 * Math.PI]);

        var y = d3.scale.linear()
            .range([0, r]);

        var table = $('#features-datatable').DataTable();
        var chartI = dc.chartRegistry.list('histogramfeatures_group');
        var chartJ = dc.chartRegistry.list('scatterfeatures_group');
        table.rows('.selected').deselect();
        table.search("").draw();
        var len = $("#features-datatable").dataTable()._('tr').length;
        var w = len * 30 + left_margin + 60;
        global_domain_filter = {};
        var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
        for (var i = 0;i<chartI.length; i++){
            var count = 0;
            chartI[i].width(w);
            chartI[i].x(d3.scale.ordinal().domain(ordering));
            for (var j=0;j<features_filter.length;j++){
                var key = features_filter[j];
                if (count === 0){
                    chartI[i].group(histogram_filters[key], histogramSelection[key]);
                } else {
                    chartI[i].stack(histogram_filters[key], histogramSelection[key]);
                }
                count++;
            }
            chartI[i].filter(null);
        }
        var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
            for (var i = 0;i<chartJ.length; i++){
                var count = 0;
                chartJ[i].group(scatter_filters['group'])
                    .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
                    .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
                    .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
                    .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1));
                chartJ[i].filter(null);
            }
        dc.renderAll();
        dc.redrawAll();
        table.clear();
        table.rows.add(feature_table_data).order([]).draw();
    }

    $('#display_sunburst').on('click', function(){
        var svgs = d3.select('svg').remove();
        sunburst_on = 1;
//        create_sunburst();
        reset_all();
    });

    $('#display_icicle').on('click', function(){
        var svgs = d3.select('svg').remove();
        sunburst_on = 0;
//        create_icicle();
        reset_all();
    });

    $('#origin_genus').on('click', function(){
        partition_data = {'name' : 'Genus', 'children' : []};
        var tmp_data = {};
        for(var i=0;i<feature_table_data.length;i++){
           var tmp_vals = feature_table_data[i];
           var genus = tmp_vals[2];
           var origin = tmp_vals[1];
           var datum = {'color' : tmp_vals[2]+ ' ' +tmp_vals[3], 'name': tmp_vals[0], 'children' : []}
           var children = [];
           for(var j=7;j<feature_table_data[i].length;j++){
               console.log(feature_header[j]);
               children.push({'count' : 1, 'name' : feature_header[j]['title'], 'number' : tmp_vals[j]});
           }
           datum['children'] = children;
           if (genus in tmp_data){
               if (origin in tmp_data[genus]){
                   tmp_data[genus][origin].push(datum);
               } else{
                   tmp_data[genus][origin] = [datum];
               }
           } else {
               tmp_data[genus] = {};
               tmp_data[genus][origin] = [datum];
           }
        }
        for (var k in tmp_data){
            var g_ins = {'name' : k, 'children' : [], 'color' : k + ' 0'};
            for (var y in tmp_data[k]){
                var d_ins = {'name' : y, 'children' : tmp_data[k][y], 'color' : k + ' 1000'};
                g_ins['children'].push(d_ins);
            }
            partition_data['children'].push(g_ins);
        }
        var ptitle = d3.select('#partition_title');
        ptitle.text('Patition Display of Ontological Features by Genus')
        var svgs = d3.select('svg').remove();
        if(sunburst_on === 1){
            create_sunburst();
        } else {
            create_icicle();
        }
        reset_all();
    });
    
    $('#origin_db').on('click', function(){
        partition_data = {'name' : 'Origin', 'children' : []};
        var tmp_data = {};
        for(var i=0;i<feature_table_data.length;i++){
           var tmp_vals = feature_table_data[i];
           var genus = tmp_vals[2];
           var origin = tmp_vals[1];
           var datum = {'color' : tmp_vals[2]+ ' ' +tmp_vals[3], 'name': tmp_vals[0], 'children' : []}
           var children = [];
           for(var j=7;j<feature_table_data[i].length;j++){
               console.log(feature_header[j]);
               children.push({'count' : 1, 'name' : feature_header[j]['title'], 'number' : tmp_vals[j]});
           }
           datum['children'] = children;
           if (origin in tmp_data){
               if (genus in tmp_data[origin]){
                   tmp_data[origin][genus].push(datum);
               } else{
                   tmp_data[origin][genus] = [datum];
               }
           } else {
               tmp_data[origin] = {};
               tmp_data[origin][genus] = [datum];
           }
        }
        for (var k in tmp_data){
            var d_ins = {'name' : k, 'children' : []};
            for (var y in tmp_data[k]){
                var g_ins = {'name' : y, 'children' : tmp_data[k][y], 'color' : y + ' 0'};
                d_ins['children'].push(g_ins);
            }
            partition_data['children'].push(d_ins);
        }
        console.log('my datastructure ' + JSON.stringify(partition_data));
        var ptitle = d3.select('#partition_title');
        ptitle.text('Patition Display of Ontological Features by DB')
        var svgs = d3.select('svg').remove();
        if(sunburst_on === 1){
            create_sunburst();
        } else {
            create_icicle();
        }
        reset_all();
    });

    $('#features-datatable tbody').on('click', 'tr', function(){
        var chartI = dc.chartRegistry.list('histogramfeatures_group');
        var rows = $('#features-datatable').DataTable().rows('.selected').data();
        var filtered_samples = organismFeatures.top(Infinity);
        for (var j = 0;j<chartI.length; j++){
            chartI[j].filter(null);
            for (var i = 0;i<rows.length; i++){
                chartI[j].filter(rows[i][0]);
            }
        }
        dc.redrawAll();
    });

    $('#features-datatable thead').on('click', 'th', function(){
        var s = [];
        var chartI = dc.chartRegistry.list('histogramfeatures_group');
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
        var chartI = dc.chartRegistry.list('histogramfeatures_group');
        var chartJ = dc.chartRegistry.list('scatterfeatures_group');
        var s = [];
        global_domain_filter = {};
        for (var i = 0;i<rows.length;i++){
            s.push(rows[i][0]);
            global_domain_filter[rows[i][0]] = 1;
        }
        var len = rows.length;
        w = (len * 30) + left_margin + 60;
        var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
        for (var i = 0;i<chartI.length; i++){
            var count = 0;
            chartI[i].width(w);
            chartI[i].x(d3.scale.ordinal().domain(s));
            for (var j=0;j<features_filter.length;j++){
                var key = features_filter[j];
                if (count === 0){
                    chartI[i].group(histogram_filters[key], histogramSelection[key]);
                } else {
                    chartI[i].stack(histogram_filters[key], histogramSelection[key]);
                }
                count++;
            }
        }
        var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
        for (var i = 0;i<chartJ.length; i++){
            chartJ[i].group(scatter_filters['group'])
                .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
                .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
                .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
                .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1))
        }
        dc.renderAll();
    });

    $("#filter-features").on('click' , function(e){
        var rows = $('#features-datatable').DataTable().rows('.selected').data();
        var chartI = dc.chartRegistry.list('histogramfeatures_group');
        var chartJ = dc.chartRegistry.list('scatterfeatures_group');
        var table = $('#features-datatable').DataTable();
        var s = [];
        var r = {};
        var searchstr = "";
        var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
        global_domain_filter = {};
        var len = rows.length;
        w = (len * 30) + left_margin + 60;
        if (rows.length === 0){
            return 0;
        }
        for (var i=0;i<rows.length;i++){
            s.push(rows[i][0]);
            global_domain_filter[rows[i][0]] = 1;
            if (searchstr.length < 1){
                searchstr = '(' + rows[i][0] + ')[^\\S+]';
            } else {
                searchstr += '|(' + rows[i][0] + ')[^\\S+]';
            }
        }
        table.search(searchstr, 1, true, true).draw();
        var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
        for (var i = 0;i<chartI.length; i++){
            var count = 0;
            chartI[i].width(w);
            chartI[i].x(d3.scale.ordinal().domain(s));
            for (var j=0;j<features_filter.length;j++){
                var key = features_filter[j];
                if (count === 0){
                    chartI[i].group(histogram_filters[key], histogramSelection[key]);
                } else {
                    chartI[i].stack(histogram_filters[key], histogramSelection[key]);
                }
                count++;
            }
            chartI[i].filter(null);
        }
        var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
        for (var i = 0;i<chartJ.length; i++){
            chartJ[i].group(scatter_filters['group'])
                .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
                .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
                .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
                .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1))
        }
        table.rows('.selected').deselect();
        dc.renderAll();
    });

    $('button.customhistogram1').on('click', function(e){
        var element = 'input.customhistogram-' + $(this).attr('id').split('-')[1];
        var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
        var chartI = dc.chartRegistry.list('histogramfeatures_group');
        var s = [];
        global_domain_filter = {};
        for (var i = 0;i<rows.length;i++){
            s.push(rows[i][0]);
            global_domain_filter[rows[i][0]] = 1;
        }
        var len = rows.length;
        w = (len * 30) + left_margin + 60;
        var histogram_filters = histogramFilters(organismFeatures, global_domain_filter);
        for (var i = 0;i<chartI.length; i++){
            var count = 0;
            chartI[i].width(w);
            chartI[i].x(d3.scale.ordinal().domain(s));
            for (var j=0;j<features_filter.length;j++){
                var key = features_filter[j];
                if (count === 0){
                    chartI[i].group(histogram_filters[key], histogramSelection[key]);
                } else {
                    chartI[i].stack(histogram_filters[key], histogramSelection[key]);
                }
                count++;
            }
        }
       dc.renderAll();
    });

    $('button.customscatter1').on('click', function(e){
        var element = 'input.customhistogram-' + $(this).attr('id').split('-')[1];
        var rows = $("#features-datatable").dataTable()._('tr', {"filter": "applied"});
        var chartJ = dc.chartRegistry.list('scatterfeatures_group');
        var s = [];
        global_domain_filter = {};
        for (var i = 0;i<rows.length;i++){
            s.push(rows[i][0]);
            global_domain_filter[rows[i][0]] = 1;
        }
        var scatter_filters = scatterFilters(feature_counts, global_domain_filter, scatx, scaty);
        for (var i = 0;i<chartJ.length; i++){
            var count = 0;
            chartJ[i].group(scatter_filters['group'])
                .x(d3.scale.linear().domain([0, scatter_filters['xmax']]))
                .y(d3.scale.linear().domain([0, scatter_filters['ymax']]))
                .xAxisLabel(scatx.charAt(0).toUpperCase() + scatx.slice(1))
                .yAxisLabel(scaty.charAt(0).toUpperCase() + scaty.slice(1))
        }
        dc.renderAll();
    });

    $('input[type=checkbox]').change(function(){
        var datum = $(this).attr('value');
        var graph_class = $(this).attr('class').split('-')[0],
            graph_number = $(this).attr('class').split('-')[1];
        if (graph_class === 'customhistogram'){
            if (this.checked){
                var index = features_filter.indexOf(datum);
                if (index !== -1){
                    features_filter.splice(index, 1);
                }
                features_filter.push(datum);
            } else {
                var index = features_filter.indexOf(datum);
                if (index !== -1){
                    features_filter.splice(index, 1);
                }
            }
        } else {
            var graph_axis = graph_number.slice(-1);
            var group = "input:checkbox[class='" + $(this).attr('class') + "']";
            if (this.checked){
                $(group).prop('checked', false);
                $(this).prop('checked', true);
            } else {
                $(this).prop('checked', false);
            }
            if (graph_axis === 'x'){
                scatx = datum;
            } else {
                scaty = datum;
            }
            console.log(scatx, scaty);
        }
        console.log('my filter ' + features_filter);
    });

    $('a.toggle-vis').on('click', function(e){
        e.preventDefault();
        var column = $("#features-datatable").DataTable().column(':contains(' + $(this).attr('data-column') + ')');
        column.visible(! column.visible());
        color_anchors($(this));
    });

    $("#features-datatable").on('click', '.popupLinkout', function(){
        console.log('I clicked ' + this.innerHTML);
        var element = this.value;
        console.log(element);
        var popup = document.getElementById(element);
        console.log(popup, popup.classList);
        if (popup.classList.contains('show')){
            popup.classList.toggle('show');
            return;
        }
        var testtext = linkoutCaller(this.innerHTML, function(err, data){
            if (err){throw err;}
            if (! data){
                return;
            }
            console.log(data);
            console.log('Completed request');
            var popup = document.getElementById(element);
            popup.classList.toggle('show');
            console.log(popup, popup.innerHTML);
            var newhtml = '<a class="textright closepopup" value="' + element + '">X</a><ul>';
            var longest = 0;
            for (var i=0;i<data.length;i++){
                if (data[i].text.length > longest){
                    longest = data[i].text.length;
                }
                newhtml += '<li><a href=' + data[i].href + ' style="color:lightblue" target="_blank">' + data[i].text + '</a></li>\n';
            }
            popup.style.width = (longest *8 + 20) +"px";
            popup.innerHTML = newhtml;
        });
    });
    $("#features-datatable").on('click', '.closepopup', function(){
        var closeme = this.getAttribute('value');
        var popup = document.getElementById(closeme);
        popup.classList.toggle('show');
    });
});

