var width = 900,
    height = 105,
    cellSize = 12; // cell size
    week_days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	
var ALL_TASKS = "all";
var csv_data, csv_data_all, csv_data_pomodoro, csv_data_weeks;
var task_name ; 
var project_pomodoro_count;
var nested_data;
var task_name_param = "task_name";
var rectWeeks;
var rect, svg;

var day = d3.time.format("%w"),
    week = d3.time.format("%U"),
    year = d3.time.format("%Y"),
    month_format = d3.time.format("%m"),
    percent = d3.format(".1%"),
    formatWeeks =  d3.time.format("%Y-%U"),
	format = d3.time.format("%Y-%m-%d");

	parseDate = d3.time.format("%Y%m%d").parse;
		
var color = d3.scale.quantize()
    .domain([0, 11])
    .range(d3.range(11)
.map(function(d) {
     return "q" + d + "-11"; 
   }));
    
    //  Tooltip Object
var tooltip = d3.select("body")
  .append("div").attr("id", "tooltip")
  .style("position", "absolute")
  .style("z-index", "10")
  .style("visibility", "hidden")
  .text("a simple tooltip");

function generateDailyCalendar() {
  svg = d3.select(".calender-map").selectAll("svg")
      .data(d3.range(2015, 2017))
    .enter().append("svg")
      .attr("width", '100%')
      .attr("data-height", '0.5678')
      .attr("viewBox",'0 0 900 105')
      .attr("class", "RdYlGn")
    .append("g")
      .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

  svg.append("text")
    .attr("transform", "translate(-38," + cellSize * 3.5 + ")rotate(-90)")
    .style("text-anchor", "middle")
    .text(function(d) { return d; });
 
  for (var i=0; i<7; i++)
  {    
    svg.append("text")
      .attr("transform", "translate(-5," + cellSize*(i+1) + ")")
      .style("text-anchor", "end")
      .attr("dy", "-.25em")
      .text(function(d) { return week_days[i]; }); 
   }

  // rect = svg.selectAll(".day")
  //     .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  //   .enter()
  // 	.append("rect")
  //     .attr("class", "day")
  //     .attr("width", cellSize)
  //     .attr("height", cellSize)
  //     .attr("x", function(d) { return week(d) * cellSize; })
  //     .attr("y", function(d) { return day(d) * cellSize; })
  //     .attr("fill",'#fff')
  //     .datum(format);

  var legend = svg.selectAll(".legend")
        .data(month)
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(" + (((i+1) * 50)+8) + ",0)"; });

  legend.append("text")
     .attr("class", function(d,i){ return month[i] })
     .style("text-anchor", "end")
     .attr("dy", "-.25em")
     .text(function(d,i){ return month[i] });
   
  svg.selectAll(".month")
      .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("path")
      .attr("class", "month")
      .attr("id", function(d,i){ return month[i] })
      .attr("d", monthPath);
}

function generateSvgForWeeksView(div_id) {
  var svgWeek = d3.select("." + div_id).selectAll("svg")
    .data(d3.range(2015, 2017))
  .enter().append("svg")
    .attr("width", '100%')
    .attr("data-height", '0.5678')
    .attr("viewBox",'0 0 900 50')
    .attr("class", "RdYlGn")
  .append("g")
    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

svgWeek.append("text")
    .attr("transform", "translate(-38," + cellSize  + ")rotate(-90)")
    .style("font-size","10px")   
    .style("text-anchor", "middle")
    .text(function(d) { return d; });
 

// var rect = svg.selectAll(".day")
//     .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
//   .enter()
//   .append("rect")
//     .attr("class", "day")
//     .attr("width", cellSize)
//     .attr("height", cellSize)
//     .attr("x", function(d) { return week(d) * cellSize; })
//     .attr("y", function(d) { return day(d) * cellSize; })
//     .attr("fill",'#fff')
//     .datum(format);

rectWeeks = svgWeek.selectAll(".day")
    .data(function(d) { return d3.time.weeks(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  .enter()
  .append("rect")
    .attr("class", "day")
    .attr("width", cellSize)
    .attr("height", cellSize * 2)
    .attr("x", function(d) { return week(d) * cellSize; })
    .attr("y", function(d) { return 0;})
    .attr("fill",'#fff')
    .datum(formatWeeks);
    // .datum(function(d) {
    //     return formatWeeks(d);
    // });

var legend = svgWeek.selectAll(".legend")
      .data(d3.range(0,52))
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(" + (((i+2 ) * cellSize) - 3) + ",0)"; });

legend.append("text")
   .style("text-anchor", "end")
   .style("font-size","7px")   
   .attr("dy", "-.1em")
   .text(function(d,i){ return i + 1 });
}

function numberWithCommas(x) {
    x = x.toString();
    var pattern = /(-?\d+)(\d{3})/;
    while (pattern.test(x))
        x = x.replace(pattern, "$1,$2");
    return x;
}

function monthPath(t0) {
  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
      d0 = +day(t0), w0 = +week(t0),
      d1 = +day(t1), w1 = +week(t1);
  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
      + "H" + w0 * cellSize + "V" + 7 * cellSize
      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
      + "H" + (w1 + 1) * cellSize + "V" + 0
      + "H" + (w0 + 1) * cellSize + "Z";
}

function getQueryVariable(variable)
{
   var query = window.location.search.substring(1);
   var vars = query.split("&");
   for (var i=0;i<vars.length;i++) {
           var pair = vars[i].split("=");
           if(pair[0] == variable){return decodeURIComponent(pair[1]);}
   }
   return(false);
}

function clear_yearly_data() {
  svg.selectAll(".day").remove();
}

function setCalendarForTask(task_data) {
  clear_yearly_data()
  rect = svg.selectAll(".day")
      .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter()
    .append("rect")
      .attr("class", "day")
      .attr("width", cellSize)
      .attr("height", cellSize)
      .attr("x", function(d) { return week(d) * cellSize; })
      .attr("y", function(d) { return day(d) * cellSize; })
      .attr("fill",'#fff')
      .datum(format);


  rect.filter(function(d) { return d in task_data; })
  .attr("class", function(d) { return "day " + color(task_data[d]); })
  .attr("data-title", function(d) { 
          return d + " pomodoro : " + task_data[d]}
  );   

}

function setCalendarForTaskWeeks(task_data) {
  rectWeeks
    .attr("class", "day")
    .attr("fill",'#fff');

  rectWeeks.filter(function(d) { return d in task_data;})
      .attr("class", function(d) { return "day " + color(task_data[d]); })
      .attr("data-title", function(d) { 
          tokens = d.split("-");
          return "Week " + tokens[1]  + " of year: " + tokens[0] +  ", pomodoro : " +
           task_data[d]}
          );   
  $("rect").tooltip({container: 'body', html: true, placement:'top'}); 
}



queue()
 .defer(d3.csv, "data/pomodoro_data_may_30.csv_out_.csv")
 .await(ready);
 

function load_csv_data(pomodoro_csv) {
  csv_data =  d3.nest()
    .key(function(d) {
      return (d.Project + "").toLowerCase(); 
   }).key(function(d) { 
      return d.Date; 
   })
   .rollup(function(leaves) { 
    return d3.sum(
      leaves, 
        function(d) {
          return parseFloat(d.Count);
        })})   
   .map(pomodoro_csv);

  csv_data_pomodoro =  d3.nest()
    .key(function(d) {return (d.Project + "").toLowerCase(); })
    .key(function(d) {return (d.Pomodoro + "").toLowerCase(); })
    .key(function(d) { return d.Date; })
   .rollup(function(leaves) { 
    return d3.sum(
      leaves, 
        function(d) {
          return parseFloat(d.Count);
        })})   
   .map(pomodoro_csv);

  csv_data_week = d3.nest()
    .key(function(d) {return (d.Project + "").toLowerCase();})
    .key(function(d) {var this_date = format.parse(d.Date); return year(this_date) + "-" + week(this_date);})
    .rollup(function(leaves) {return d3.sum(leaves, function(d) {return parseFloat(d.Count);})})   
    .map(pomodoro_csv); 

   return {
    "csv_data" : csv_data,
    "csv_data_pomodoro" : csv_data_pomodoro,
    "csv_data_week": csv_data_week
   }

}

function setTaskNameHeader(div_id_text, heading, task_name) {
d3.select(div_id_text).html("");

d3.select(div_id_text)
  .append("html")
    .attr("x", 0)             
    .attr("y", 0)
    .attr("text-anchor", "middle")  
    .style("font-size", "25px") 
    .style("text-anchor", "middle")
    .html("<h2>" + heading + " for task:</h2>" + "<h1 style=\"color:Green;\">" + task_name + "</h1>");
}


function load_csv_data_all(pomodoro_csv) {
  csv_data_all =  d3.nest()
    .key(function(d) {
      return (ALL_TASKS).toLowerCase(); 
   }).key(function(d) { 
      return d.Date; 
   })
   .rollup(function(leaves) { 
    return d3.sum(
      leaves, 
        function(d) {
          return parseFloat(d.Count);
        })})   
   .map(pomodoro_csv);

   all_count = d3.nest()
   .key(function(d) {
      return (ALL_TASKS).toLowerCase(); 
   })
   .rollup(function(leaves) { 
    return d3.sum(
      leaves, 
        function(d) {
          return parseFloat(d.Count);
        })})   
   .map(pomodoro_csv);

   return {
    "csv_data_all" : csv_data_all,
    "all_count" : all_count
   };

}

function load_csv_data_all_weeks(pomodoro_csv) {
  return d3.nest()
    .key(function(d) {
      return (ALL_TASKS).toLowerCase(); 
   }).key(function(d) { 
        var this_date = format.parse(d.Date);
        return year(this_date) + "-" + week(this_date); 
   })
   .rollup(function(leaves) { 
    return d3.sum(
      leaves, 
        function(d) {
          return parseFloat(d.Count);
        })})   
   .map(pomodoro_csv);
}

function refresh_ui_for_weeks(filter_data, task_name) {
  setCalendarForTaskWeeks(filter_data);
  setTaskNameHeader("#chart-text-weeks", "Weekly calendar", task_name);
}

function refresh_ui_for_days(filter_data, task_name) {
  setCalendarForTask(filter_data);
  setTaskNameHeader("#chart-text", "Daily calendar", task_name);
}

function load_drop_down(data, all_count) {
  nested_data = d3.nest()
    .key(function(d) { return d.Project; })
    .key(function(d) { return d.Pomodoro; })
    .rollup(function(leaves) {
        return {
          "length": leaves.length, 
          "Count":  d3.sum(leaves, function(d) {return parseFloat(d.Count);
        })} 
    })
    .entries(data);

  project_pomodoro_count = d3.nest()
    .key(function(d) { return d.Project; })
    .key(function(d) { return d.Pomodoro; })
    .rollup(function(leaves) {
        return {
          "length": leaves.length, 
          "Count":  d3.sum(leaves, function(d) {return parseFloat(d.Count);
        })} 
    })
    .map(data);

  var per_project_sum = d3.nest()
    .key(function(d) { return d.Project; })
    .rollup(function(leaves) {
        return {
          "length": leaves.length, 
          "Count":  d3.sum(leaves, function(d) {return parseFloat(d.Count);
        })}})
    .map(data);

    var all = {
      "key" : "all"
    }

    var all_sum = {
      "key" : "all",
      "Count" : all_count
    }
    per_project_sum["all"] = all_sum;
    nested_data.push(all);
    nested_data.map(function (d){
        d["Count"] = per_project_sum[d.key].Count;
    });

    nested_data.sort(function(a,b) {
      return parseFloat(b.Count) - parseFloat(a.Count); 
    } );
    
    generate_top_level_drop_down("#select-option", nested_data)
    return nested_data;    
}

function generate_top_level_drop_down(div_id, nested_data) {
  var select = d3.select(div_id)
    .append("select");

  select
    .on("change", function(d) {
        var value = d3.select(this).property("value");
        top_level_drop_selected(value)
    });

  select.selectAll("option")
      .data(nested_data)
      .enter()
      .append("option")
      .attr("value", function (d) { return d.key; })
      .text(function (d) { return  d.key + ", Pomodoro Count:" + d.Count; });
}

// project level drop down selected.
function top_level_drop_selected(project_text) {
  update_ui_with_project_name(project_text);
  generate_pomodoro_level_drop_down("#pomodoro-option", project_text.toLowerCase(), 
    csv_data_pomodoro[project_text.toLowerCase()]);
}  

// project level drop down selected.
function pomodoro_level_drop_selected(project_task, task_name_text) {
  update_ui_with_task_name(project_task, task_name_text);
}  

function generate_pomodoro_level_drop_down(div_id, project_text, nested_data) {
  d3.select(div_id).html("");
  var select = d3.select(div_id)
    .append("select");

  select
    .on("change", function(d) {
        var task_name = d3.select(this).property("value");
        pomodoro_level_drop_selected(project_text, task_name);
    });
    
    var tasks = d3.keys(nested_data);
    d3.keys(nested_data)
      .map(function (key) {
        nested_data[key].Count = 0;
        nested_data[key].Count = d3.sum(d3.values(nested_data[key]));
      })

    tasks.sort(function(a,b) {
      return parseFloat(nested_data[b].Count) - parseFloat(nested_data[a].Count); 
    } );

    select.selectAll("option")
      .data(tasks)
      .enter()
      .append("option")
      .attr("value", function (d) { 
          return d; 
      })
      .text(function (d) { 
          return  d + ", Pomodoro Count:" + nested_data[d].Count; 
      });
}


function ready(error, pomodoro_csv) {
  csv_data_dict = load_csv_data(pomodoro_csv);
  csv_data = csv_data_dict["csv_data"]
  csv_data_pomodoro = csv_data_dict["csv_data_pomodoro"]
  csv_data_weeks = csv_data_dict["csv_data_week"];
  csv_data_all_dict = load_csv_data_all(pomodoro_csv);
  csv_data_all_weeks = load_csv_data_all_weeks(pomodoro_csv);
  load_drop_down(pomodoro_csv, csv_data_all_dict["all_count"]["all"]);
  var url_params_string = window.location.search.substring(1);
  var task_name_text = getQueryVariable(task_name_param);
  generateDailyCalendar();
  generateSvgForWeeksView("calender-map-weeks");
  update_ui_with_project_name(task_name_text);
};

function update_ui_with_task_name (project_name, task_name_text) {
  var filter_data, filter_data_weeks ;
  if (task_name_text != false && task_name_text.toLowerCase() != ALL_TASKS) {
    task_name = task_name_text.toLowerCase();
    filter_data = csv_data_pomodoro[project_name][task_name];  
  }
  update_ui_with_selection(task_name, filter_data, filter_data_weeks)  
}

function update_ui_with_project_name (task_name_text) {
  var filter_data, filter_data_weeks ;
  if (task_name_text != false && task_name_text.toLowerCase() != ALL_TASKS) {
    task_name = task_name_text.toLowerCase();
    filter_data = csv_data[task_name];
    filter_data_weeks = csv_data_weeks[task_name];
  } else {
    task_name = ALL_TASKS;
    filter_data = csv_data_all_dict["csv_data_all"][task_name];
    filter_data_weeks = csv_data_all_weeks[task_name];
  }
  update_ui_with_selection(task_name, filter_data, filter_data_weeks)  
}

function update_ui_with_selection(task_name_text, filter_data, filter_data_weeks) {
  refresh_ui_for_days(filter_data, task_name);
  refresh_ui_for_weeks(filter_data_weeks, task_name);
}

