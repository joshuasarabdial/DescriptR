import * as d3 from "d3";
import styles from "./Graph.module.css";
import * as SvgToPng from 'save-svg-as-png';

export function runForceGraph(
  courseModal,
  container,
  coursesData,
  prereqsData,
  nodeHoverTooltip
) {
  // Convert course data over to node and link data
  var nodesData = coursesData.map((c) =>{ return {"id": c.fullname, "subject": c.subject, "name": c.name} })
    var linksGetter = (c) => {
      var linkArr = [];
      c.forEach((d) => {
        if (d.prerequisites.simple?.length) {
          linkArr = linkArr.concat(d.prerequisites.simple.map((e)=> {
            if (!nodesData.find(element => element.id === e)) {
              let predata = prereqsData.find(ele => ele.fullname === e)
              if(predata) {
                nodesData = nodesData.concat({
                  "id": predata.fullname,
                  "subject": predata.subject,
                  "name": predata.name
                });
              } else {
                nodesData = nodesData.concat({"id": e, "subject": null});
              }
            }
            return { "source": d.fullname, "target": e, "value": 1};
          }))
        }
      })
      return linkArr;
    };
  const linksData = linksGetter(coursesData);

  const links = linksData.map((d) => Object.assign({}, d));
  const nodes = nodesData.map((d) => Object.assign({}, d));

  const width = window.innerWidth * 0.9;
  const height = width * 0.5;

  /* Functions */
  // Hover element creation and removal
  const addTooltip = (hoverTooltip, d, x, y) => {
    div
      .transition()
      .duration(200)
      .style("opacity", 0.9);
    div
      .html(hoverTooltip(d))
      .style("left", `${x}px`)
      .style("top", `${y - 28}px`);
  };

  const removeTooltip = () => {
    div
      .transition()
      .duration(200)
      .style("opacity", 0);
  };

  // Creates a 90 color scale for the subjects.
  const color = (d) => {
    const scale = d3.scaleOrdinal()
      .range(["#6668dd","#76e440","#5c37cd","#cfe848","#c53fe1","#5ada6d","#a354d9","#7ab737",
              "#522696","#e5cc3a","#2d1969","#bbe687","#db39b5","#6ee9ab","#943a9b","#458831",
              "#cf79db","#a8ac3b","#3d4997","#daa83c","#5b88e0","#ec4d1f","#40c3e1","#d13529",
              "#62e5da","#e0346e","#51b47a","#b33177","#b8e0b2","#301344","#e5d98b","#181837",
              "#dc7e21","#67b5eb","#a04216","#568fc7","#ea7251","#0d1724","#e49457","#332e5a",
              "#93a961","#6b286a","#646d24","#e064ac","#2c5623","#df4c58","#52a79b","#a83638",
              "#75bace","#793122","#add6da","#291429","#e2e7df","#32171a","#e6cdb6","#213146",
              "#d7af77","#8366af","#9d7a29","#b299e5","#203018","#e39bd3","#46855f","#d86686",
              "#1a3a3a","#e692a4","#397784","#bf7951","#536d9d","#795222","#abbbe9","#54211e",
              "#92a98c","#7d2351","#486657","#8f384b","#7d90a4","#55233c","#b9a28b","#584c7a",
              "#ce7e75","#3b566e","#daadaf","#473643","#c2a8cb","#4e4127","#a46590","#837754",
              "#76596b","#99716e"]);
    return d => {
      if (d.subject === null) {
        return "#666666";
      }
      else {
        return scale(d.subject);
      }
    }
  };

  // Updates the D3 drag module. Can probably leave as is
  const drag = (simulation) => {
    const dragstarted = (event,d) => {
      svg.style("cursor", "grabbing");
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    };

    const dragged = (event,d) => {
      svg.style("cursor", "grabbing");
      d.fx = event.x;
      d.fy = event.y;
    };

    const dragended = (event,d) => {
      svg.style("cursor", "pointer");
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    };

    return d3
      .drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  };

  // Add the tooltip element to the graph
  const tooltip = document.querySelector("#graph-tooltip");
  if (!tooltip) {
    const tooltipDiv = document.createElement("div");
    tooltipDiv.classList.add(styles.tooltip);
    tooltipDiv.style.opacity = "0";
    tooltipDiv.id = "graph-tooltip";
    document.body.appendChild(tooltipDiv);
  }
  const div = d3.select("#graph-tooltip");

  //Export graph as image on download click
  d3.select("#download-node-graph").on('click', function() {
      // Get the d3js SVG element and save using saveSvgAsPng.js
      SvgToPng.saveSvgAsPng(document.getElementById("courses-node-graph"), "courses-node-graph.png", {backgroundColor: "#FFFFFF", left: -width / 2, top: -height / 2});
  });

  // D3's built in tool to run force simulations
  const simulation = d3
    .forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id))
    .force("charge", d3.forceManyBody().strength(-700))    // Distance between nodes
    .force("collision", d3.forceCollide().radius(42))
    .force("x", d3.forceX())
    .force("y", d3.forceY())

  d3.select("svg").remove();
  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", [-width / 2, -height / 2, width, height])    // Viewbox defines the position of the graph
    .style("cursor","move")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("id", "courses-node-graph");

  svg.append("defs").selectAll("marker")
      .data(["suit", "licensing", "resolved"])
    .enter().append("marker")
      .attr("id", function(d) { return d; })
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 30)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto-start-reverse")
    .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .style("stroke", "#999")
      .style("opacity", "0.6");

  // Child element for svg for keeping nodes, links and labels in
  const g = svg.append("g")
    .attr("class", "everything");

  var zoom_handler = d3.zoom()
    .on("zoom", function ({transform}) {
      g.attr("transform", transform);
    })
    .scaleExtent([0.1, 8])

  zoom_handler(svg)

  const link = g
    .append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", d => Math.sqrt(d.value))    // Width of the edges
    .style("marker-start", "url(#suit)");
  const node = g
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 2)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 12)    // Defines the radius of the circle. Can be used later for course capacity
    .attr("fill", color(d => d))
    .attr("opacity", 0.6);
  if (nodesData.length <= 300) node.call(drag(simulation));

  const label = g.append("g")
    .attr("class", "labels")
    .selectAll("text")
    .data(nodes)
    .enter()
    .append("text")
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .text(d => d.id);    // Text of the label that appears
    if (nodesData.length <= 300) label.call(drag(simulation));

  // Mouse events
  // "dblclick" event available
  label.on("mouseover", (event,d) => {
    svg.style("cursor", "pointer");
    addTooltip(nodeHoverTooltip, d, event.pageX, event.pageY);
    highlightAdjacent(d);
  })
  .on("mouseout", (event, d) => {
    svg.style("cursor", "move");
    removeTooltip();
    highlightAdjacentOut(d);
  });

  node.on("mouseover", (event, d) => {
    highlightAdjacent(d);
  })
  .on("mouseout", (event, d) => {
    highlightAdjacentOut(d);
  })

  let linkedByIndex = {};
  links.forEach((d) => {
    linkedByIndex[`${d.source.index},${d.target.index}`] = true;
  });

  function highlightAdjacent(d) {
    node
      .transition(500)
      .attr('opacity', o => {
        if (isConnected(o, d)) {
          return 1.0;
        }
        return 0.2
      })
      .attr('fill', (o) => {
        let fillColor;
        if (isEqual(o, d)) {
          fillColor = 'hotpink';
        } else {
          fillColor = 'red';
        }
        return fillColor;
      });
  }

  function highlightAdjacentOut(d) {
    node
      .attr("fill", color(d => d))
      .transition(500)
      .attr('opacity', 0.6);
  }

  function isConnected(a, b) {
    function isConnectedAsSource(a, b) {
      return linkedByIndex[`${a.index},${b.index}`];
    }

    function isConnectedAsTarget(a, b) {
      return linkedByIndex[`${b.index},${a.index}`];
    }

    return isConnectedAsTarget(a, b) || isConnectedAsSource(a, b) || a.index === b.index;
  }

  function isEqual(a, b) {
    return a.index === b.index;
  }

  label.on("click", function() {
    let [code, number] = this.innerHTML.split("*");
    let course = coursesData.filter((el) => { return el.code===code && el.number===number })[0];
    if (!course) course = prereqsData.filter((el) => { return el.code===code && el.number===number })[0];
    if (course) courseModal.current.showCourse(course);
  });

  // Need to research more into how to make static image without animating. Worst case web worker. Second worst case render after table has rendered.
  if (nodesData.length > 300) {
    simulation.on("end", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
      label
        .attr("x", d => { return d.x; })
        .attr("y", d => { return d.y; })
    });
  }
  else simulation.on("tick", () => {
    //update link positions
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    // update node positions
    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);

    // update label positions
    label
      .attr("x", d => { return d.x; })
      .attr("y", d => { return d.y; })
  });

  return {
    destroy: () => {
      simulation.stop();
    },
    nodes: () => {
      return svg.node();
    }
  };
}
