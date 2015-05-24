!function(){
	var bP={};	
	var b=30, bb=150, height=1000, buffMargin=1, minHeight=14;
	var c1=[-170, 40], c2=[-50, 200], c3=[-10, 140]; //Column positions of labels.
	var colors =["#3366CC", "#DC3912",  "#FF9900","#109618", "#990099", "#0099C6", "#EB4747",
			"#F08A75","#F57A3D","#F5CCA3","#F7E06E","#A6F20D","#D6FCCF","#D1FAFA","#00FFFF","#00AAFF","#8CBFD9","#1430B8","#F20DCC",
			"#F0759E","#3333CC","#CCFF33","#66C285","#CCFF66","#0066FF","#666699",
			"#F57A3D","#F5CCA3","#F7E06E","#A6F20D","#3366CC", "#DC3912"
	];
	bP.partData = function(data,p){
		var sData={};
		
		sData.keys=[
			d3.set(
				data
					.map(function(d){ 
						return d[3].properties["REGIONID"];
					}))
					.values()
					.sort(function(a,b){ 
						return ( a<b? -1 : a>b ? 1 : 0);
					}),
			d3.set(
				data
					.map(function(d){ 
						return d[4]["REGIONID"];
					}))
					.values()
					.sort(function(a,b){ 
						return ( a<b? -1 : a>b ? 1 : 0)
					;})		
		];
		
		var leftMap = {};
		var rightMap = {};
		for(var i = 0 ; i < data.length; i++) {
			d = data[i];
			leftMap[d[3].properties["REGIONID"]] = d[3];	
			rightMap[d[4]["REGIONID"]] = d[4];	
		}
		sData.mapIdName=[leftMap, rightMap];

		sData.data = [	
			sData.keys[0].map(function(d){ 
				return sData.keys[1].map(function(v){ 
					return 0; 
				}); 
			}),
			sData.keys[1].map(function(d){
				return sData.keys[0].map(function(v){
					return 0; 
			}); 
		})];
		
		data.forEach(function(d){ 
			sData.data[0][
				sData.keys[0].indexOf("" + d[3].properties["REGIONID"])][sData.keys[1].indexOf(""+ d[4]["REGIONID"])] = d[p];
			sData.data[1][
			sData.keys[1].indexOf("" + d[4]["REGIONID"])][sData.keys[0].indexOf(""+ d[3].properties["REGIONID"])]= d[p]; 
		});
		
		return sData;
	}
	
	function visualize(data){
		var vis ={};
		function calculatePosition(a, s, e, b, m){
			var total=d3.sum(a);
			var sum=0, neededHeight=0, leftoverHeight= e-s-2*b*a.length;
			var ret =[];
			
			a.forEach(
				function(d){ 
					var v={};
					v.percent = (total == 0 ? 0 : d/total); 
					v.value=d;
					v.height=Math.max(v.percent*(e-s-2*b*a.length), m);
					(v.height==m ? leftoverHeight-=m : neededHeight+=v.height );
					ret.push(v);
				}
			);
			
			var scaleFact=leftoverHeight/Math.max(neededHeight,1), sum=0;
			
			ret.forEach(
				function(d){ 
					d.percent = scaleFact*d.percent; 
					d.height=(d.height==m? m : d.height*scaleFact);
					d.middle=sum+b+d.height/2;
					d.y=s + d.middle - d.percent*(e-s-2*b*a.length)/2;
					d.h= d.percent*(e-s-2*b*a.length);
					d.percent = (total == 0 ? 0 : d.value/total);
					sum+=2*b+d.height;
				}
			);
			return ret;
		}

		vis.mainBars = [ 
			calculatePosition( data.data[0].map(function(d){ return d3.sum(d);}), 0, height, buffMargin, minHeight),
			calculatePosition( data.data[1].map(function(d){ return d3.sum(d);}), 0, height, buffMargin, minHeight)
		];
		
		vis.subBars = [[],[]];
		vis.mainBars.forEach(function(pos,p){
			pos.forEach(function(bar, i){	
				calculatePosition(data.data[p][i], bar.y, bar.y+bar.h, 0, 0).forEach(function(sBar,j){ 
					sBar.key1=(p==0 ? i : j); 
					sBar.key2=(p==0 ? j : i); 
					vis.subBars[p].push(sBar); 
				});
			});
		});
		vis.subBars.forEach(function(sBar){
			sBar.sort(function(a,b){ 
				return (a.key1 < b.key1 ? -1 : a.key1 > b.key1 ? 
						1 : a.key2 < b.key2 ? -1 : a.key2 > b.key2 ? 1: 0 )});
		});
		
		vis.edges = vis.subBars[0].map(function(p,i){
			return {
				key1: p.key1,
				key2: p.key2,
				y1:p.y,
				y2:vis.subBars[1][i].y,
				h1:p.h,
				h2:vis.subBars[1][i].h
			};
		});
		vis.keys=data.keys;
		vis.mapIdName=data.mapIdName;
		return vis;
	}
	
	function arcTween(a) {
		var i = d3.interpolate(this._current, a);
		this._current = i(0);
		return function(t) {
			return edgePolygon(i(t));
		};
	}
	
	function getTipText(data, col, index) {
		if(!isAnySelected(prevDict)) {
			if (col == 0) {
				tipText = data.mapIdName[col][data.keys[col][index]].properties.NAME;
				count = getSimCount(data, col, index, false);
				return "Click to see top " + count + " similar neighborhoods of <span style='color:red'>" + tipText + ".</span>";				
			} else {
				tipText = data.mapIdName[col][data.keys[col][index]].name;
				count = getSimCount(data, col, index, false);
				return "Click to see all the " + count + " neighborhoods where <span style='color:red'>" + tipText + " </span> is in top 10.";				
			}
		}
		// something was selected. 
		if(isOnlyLeftSelected(prevDict)) {
			// is prev selection same as current, reset.
			if(isPrevLeftSameCurrent(prevDict, index, col)) {
				return "Click to deselect all.";				
			} else if (col == 0) {
				tipText = data.mapIdName[col][data.keys[col][index]].properties.NAME;
				count = getSimCount(data, col, index, false);
				return "Click to see top " + count + " similar neighborhoods of <span style='color:red'>" + tipText + ".</span>";				
			} else {
				// both left and right selected.
				var name1 = data.mapIdName[prevDict.prevLeftCol][data.keys[prevDict.prevLeftCol][prevDict.prevLeftIndex]].properties.NAME;
				var name2 = data.mapIdName[col][data.keys[col][index]].name;

				return "Click to select common menu items between <span style='color:red'>" + name1 + "</span> & "  +
					"<span style='color:green'>" + name2 + ".</span>"  ;				
			}
		} else if (isOnlyRightSelected(prevDict)) {
			// is prev selection same as current, reset.
			if(isPrevRightSameCurrent(prevDict, index, col)) {
				return "Click to deselect all.";				
			} else if(col == 1) {
				// another right selected, deselect prev, select new
				tipText = data.mapIdName[col][data.keys[col][index]].name;
				count = getSimCount(data, col, index, false);
				return "Click to see all the " + count + " neighborhoods where <span style='color:red'>" + tipText + " </span> is in top 10.";				
			} else {
				// both left and right selected.
				// both left and right selected.
				var name2 = data.mapIdName[col][data.keys[col][index]].properties.NAME;
				var name1 = data.mapIdName[prevDict.prevRightCol][data.keys[prevDict.prevRightCol][prevDict.prevRightIndex]].name;

				return "Click to select <span style='color:red'>" + name1 + "</span> & "  +
					"<span style='color:green'>" + name2 + ".</span>"  ;				
			}
		}
		return "Click to deselect all.";							
	}

	function getSimCount(data, col, index, isBothSelected) {
		return data.data[col][index]
			.filter(function(d, i) {
				if (isBothSelected) {
					return (prevIndex ==i && y == s ? d : 0);
				} else {
					return (d > 0 ? 1 : 0);
				}})
			.length;
	}

	function drawPart(data, bpData, id, p){
		var tip = d3.tip()
  			.attr('class', 'd3-tip')
  			.offset([-10, 0])
  			.html(function(d, i) {
  				return getTipText(bpData, p, i);
  		})
		d3.select("#"+id).append("g").attr("class","part"+p)
			.attr("transform","translate("+( p*(bb+b))+",0)");
		d3.select("#"+id).select(".part"+p).append("g").attr("class","subbars");
		d3.select("#"+id).select(".part"+p).append("g").attr("class","mainbars");
		
		var mainbar = d3.select("#"+id).select(".part"+p).select(".mainbars")
			.selectAll(".mainbar").data(data.mainBars[p])
			.enter().append("g").attr("class","mainbar");

		mainbar.call(tip);
		mainbar.append("rect").attr("class","mainrect")
			.attr("x", 0).attr("y",function(d){ return d.middle-d.height/2; })
			.attr("width",b).attr("height",function(d){ return d.height; })
			.style("shape-rendering","auto")
			.style("fill-opacity",0).style("stroke-width","0.5")
			.style("stroke","black").style("stroke-opacity",0);


		mainbar.append("text").attr("class","barlabel")
			.attr("x", c1[p]).attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ if (p == 0) return data.mapIdName[p][data.keys[p][i]].properties.NAME;
				else return data.mapIdName[1][data.keys[1][i]].name;})
 			.on('mouseover', tip.show)	
			.on('mouseout', tip.hide)	
			.attr("text-anchor","start" );
			
		mainbar.append("text").attr("class","barvalue")
			.attr("x", c2[p]).attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ return d.value.toFixed(2) ;})
			.attr("text-anchor","end");
			
		mainbar.append("text").attr("class","barpercent")
			.attr("x", c3[p]).attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ return "( "+Math.round(100*d.percent)+"%)" ;})
			.attr("text-anchor","end").style("fill","grey");
			
		d3.select("#"+id).select(".part"+p).select(".subbars")
			.selectAll(".subbar").data(data.subBars[p]).enter()
			.append("rect").attr("class","subbar")
			.attr("x", 0).attr("y",function(d){ return d.y})
			.attr("width",b).attr("height",function(d){ return d.h})
			.style("fill",function(d){ return colors[d.key1];});
	}
	
	function drawEdges(data, id){
		d3.select("#"+id).append("g").attr("class","edges").attr("transform","translate("+ b+",0)");

		d3.select("#"+id).select(".edges").selectAll(".edge")
			.data(data.edges).enter().append("polygon").attr("class","edge")
			.attr("points", edgePolygon).style("fill",function(d){ return colors[d.key1];})
			.style("opacity",0.5).each(function(d) { this._current = d; });	
	}	
	
	function drawHeader(header, id){
		d3.select("#"+id).append("g").attr("class","header").append("text").text(header[2])
			.style("font-size","20").attr("x",108).attr("y",-20).style("text-anchor","middle")
			.style("font-weight","bold");
		
		[0,1].forEach(function(d){
			var h = d3.select("#"+id).select(".part"+d).append("g").attr("class","header");
			
			h.append("text").text(header[d]).attr("x", (c1[d]-5))
				.attr("y", -5).style("fill","grey");
			
			h.append("text").text("similarity sum").attr("x", (c2[d]-10))
				.attr("y", -5).style("fill","grey");
			
			h.append("line").attr("x1",c1[d]-10).attr("y1", -2)
				.attr("x2",c3[d]+10).attr("y2", -2).style("stroke","black")
				.style("stroke-width","1").style("shape-rendering","crispEdges");
		});
	}
	
	function edgePolygon(d){
		return [0, d.y1, bb, d.y2, bb, d.y2+d.h2, 0, d.y1+d.h1].join(" ");
	}	
	
	function transitionPart(data, id, p){
		var mainbar = d3.select("#"+id).select(".part"+p).select(".mainbars")
			.selectAll(".mainbar").data(data.mainBars[p]);
		
		mainbar.select(".mainrect").transition().duration(500)
			.attr("y",function(d){ return d.middle-d.height/2;})
			.attr("height",function(d){ return d.height;});
			
		mainbar.select(".barlabel").transition().duration(500)
			.attr("y",function(d){ return d.middle+5;});
			
		mainbar.select(".barvalue").transition().duration(500)
			.attr("y",function(d){ return d.middle+5;}).text(function(d,i){ return d.value.toFixed(2) ;});
			
		mainbar.select(".barpercent").transition().duration(500)
			.attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ return "( "+Math.round(100*d.percent)+"%)" ;});
			
		d3.select("#"+id).select(".part"+p).select(".subbars")
			.selectAll(".subbar").data(data.subBars[p])
			.transition().duration(500)
			.attr("y",function(d){ return d.y}).attr("height",function(d){ return d.h});
	}
	
	function transitionEdges(data, id){
		d3.select("#"+id).append("g").attr("class","edges")
			.attr("transform","translate("+ b+",0)");

		d3.select("#"+id).select(".edges").selectAll(".edge").data(data.edges)
			.transition().duration(500)
			.attrTween("points", arcTween)
			.style("opacity",function(d){ return (d.h1 ==0 || d.h2 == 0 ? 0 : 0.5);});	
	}
	
	function transition(data, id){
		transitionPart(data, id, 0);
		transitionPart(data, id, 1);
		transitionEdges(data, id);
	}
	
	bP.draw = function(data, svg){
		data.forEach(function(biP,s){
			svg.append("g")
				.attr("id", biP.id)
				.attr("transform","translate("+ (550*s)+",0)");
				
			var visData = visualize(biP.data);
			drawPart(visData, biP.data, biP.id, 0);
			drawPart(visData, biP.data, biP.id, 1); 
			drawEdges(visData, biP.id);
			drawHeader(biP.header, biP.id);
			
			[0,1].forEach(function(p){			
				d3.select("#"+biP.id)
					.select(".part"+p)
					.select(".mainbars")
					.selectAll(".mainbar")
					.on("click",function(d, i){ return bP.mouseClick(data, p, i); })
					// .on("mouseover",function(d, i){ return bP.selectSegment(data, p, i); })
					// .on("mouseout",function(d, i){ return bP.deSelectSegment(data, p, i); });	
			});
		});	
	}

	var prevDict = {
		prevLeftCol : -1,
		prevLeftIndex : -1,
		prevRightCol : -1,
		prevRightIndex : -1
	}


	function isLeftSelected(prevDict) {
		return prevDict.prevLeftCol != -1 && prevDict.prevLeftIndex != -1 ;
	}

	function isRightSelected(prevDict) {
		return prevDict.prevRightCol != -1 && prevDict.prevRightIndex != -1 ;
	}

	function isOnlyLeftSelected(prevDict) {
		return isLeftSelected(prevDict) && !isRightSelected(prevDict);
	}

	function isOnlyRightSelected(prevDict) {
		return !isLeftSelected(prevDict) && isRightSelected(prevDict);
	}

	function isBothSelected(prevDict) {
		return isLeftSelected(prevDict) && isRightSelected(prevDict);
	}

	function isAnySelected(prevDict) {
		return isLeftSelected(prevDict) || isRightSelected(prevDict);
	}

	function setPrevLeft(prevDict, col, index) {
		prevDict.prevLeftCol = col;
		prevDict.prevLeftIndex = index;
	}

	function setPrevRight(prevDict, col, index) {
		prevDict.prevRightCol = col;
		prevDict.prevRightIndex = index;
	}

	function setPrevReset(prevDict) {
		setPrevLeft(prevDict, -1, -1);
		setPrevRight(prevDict, -1, -1);
	}

	function isPrevLeftSameCurrent(prevDict, index, col) {
		return prevDict.prevLeftIndex == index && prevDict.prevLeftCol == col;
	}

	function isPrevRightSameCurrent(prevDict, index, col) {
		return prevDict.prevRightIndex == index && prevDict.prevRightCol == col;
	}

	function setPrev(prevDict, col, index) {
		if (col == 0) {
			setPrevLeft(prevDict, col, index);
		} else {
			setPrevRight(prevDict, col, index);
		}
	}

	function deselectPrev(prevDict, data, col, index) {
		if (col == 0) {
			bP.deSelectSegment(data, col, prevDict.prevLeftIndex);			
		} else {
			bP.deSelectSegment(data, col, prevDict.prevRightIndex);						
		}
	}

	function selectSingle(data, col, index) {
		bP.selectSegment(data, col, index, prevDict, false);			
		if (col == 0) {
			hood = data[0].data.mapIdName[col][data[0].data.keys[col][index]];
			refreshUI(hood);
		}
	}

	function selectBoth(data, prevIndex, col, index) {
		bP.selectSegment(data, col, index, prevIndex, true);
		if (col == 1) {
			hood = data[0].data.mapIdName[col][data[0].data.keys[col][index]];
			refreshPairUI(hood);		
		}			
	}

	bP.mouseClick = function(data, col, index) {
		hood = data[0].data.mapIdName[col][data[0].data.keys[col][index]];

		// nothing was selected earlier, first time.
		if (!isAnySelected(prevDict)) {
			selectSingle(data, col, index);
			setPrev(prevDict, col, index);	
			return;
		}
		// something was selected. 
		if(isOnlyLeftSelected(prevDict)) {
			// is prev selection same as current, reset.
			if(isPrevLeftSameCurrent(prevDict, index, col)) {
				bP.deSelectSegment(data, col, index);
				setPrevReset(prevDict);
				return;			
			} else if (col == 0) {
				// another left selected, deselect prev, select new
				deselectPrev(prevDict, data, col, index);
				selectSingle(data, col, index);
			} else {
				// both left and right selected.
				selectBoth(data, prevDict.prevLeftIndex, col, index);
			}
		} else if (isOnlyRightSelected(prevDict)) {
			// is prev selection same as current, reset.
			if(isPrevRightSameCurrent(prevDict, index, col)) {
				bP.deSelectSegment(data, col, index);
				setPrevReset(prevDict);
				return;			
			} else if(col == 1) {
				// another right selected, deselect prev, select new
				deselectPrev(prevDict, data, col, index);
				selectSingle(data, col, index);
			} else {
				// both left and right selected.
				selectBoth(data, prevDict.prevRightIndex, col, index);
			}
		} else if(isBothSelected(prevDict)) {
			bP.deSelectSegment(data, prevDict.prevLeftCol, prevDict.prevLeftIndex);
			bP.deSelectSegment(data, prevDict.prevRightCol, prevDict.prevRightIndex);
			setPrevReset(prevDict);
			resetCloud();
			return ;
		}
		setPrev(prevDict, col, index);
	}
	
	bP.selectSegment = function(data, m, s, prevIndex, isBothSelected){
		data.forEach(function(k){
			var newdata =  {keys:[], data:[]};	
				
			newdata.keys = k.data.keys.map( function(d){ return d;});
			if (isBothSelected) {
				m = m == 0 ? 1 : 0;
			}
			newdata.data[m] = k.data.data[m].map( function(d){ return d;});
			
			newdata.data[1-m] = k.data.data[1-m]
				.map(function(v, y){ 
					return v.map(function(d, i){ 
							if (isBothSelected) {
								return (prevIndex ==i && y == s ? d : 0);
							} else {
								return (s==i ? d : 0);
							}
					});
				});
			
			transition(visualize(newdata), k.id);
			var selectedBar = d3.select("#"+k.id).select(".part"+m)
				.select(".mainbars")
				.selectAll(".mainbar")
				.filter(function(d,i){ 
					if (isBothSelected) {
						return i==prevIndex;
					} else {
						return i==s;						
					}
					;});
			selectedBar.select(".mainrect").style("stroke-opacity",1);			
			selectedBar.select(".barlabel").style('font-weight','bold');
			selectedBar.select(".barvalue").style('font-weight','bold');
			selectedBar.select(".barpercent").style('font-weight','bold');
				
	
			if (isBothSelected) {	
				m = m == 0 ? 1 : 0;
				var selectedBar = d3.select("#"+k.id).select(".part"+m)
					.select(".mainbars")
					.selectAll(".mainbar")
					.filter(function(d,i){ return (i==s);});				
				selectedBar.select(".mainrect").style("stroke-opacity",1);			
				selectedBar.select(".barlabel").style('font-weight','bold');
				selectedBar.select(".barvalue").style('font-weight','bold');
				selectedBar.select(".barpercent").style('font-weight','bold');
			}
		});
	}	
	
	bP.deSelectSegment = function(data, m, s){
		data.forEach(function(k){
			transition(visualize(k.data), k.id);
			
			var selectedBar = d3.select("#"+k.id).select(".part"+m).select(".mainbars")
				.selectAll(".mainbar").filter(function(d,i){ return (i==s);});
			
			selectedBar.select(".mainrect").style("stroke-opacity",0);			
			selectedBar.select(".barlabel").style('font-weight','normal');
			selectedBar.select(".barvalue").style('font-weight','normal');
			selectedBar.select(".barpercent").style('font-weight','normal');
		});		
	}
	
	this.bP = bP;
}();