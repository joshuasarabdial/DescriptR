import * as d3 from "d3";
import * as SvgToPng from 'save-svg-as-png';

export function runTreeGraph(
  container,
  coursesData,
) {
  const containerRect = container.getBoundingClientRect();
  const h = containerRect.height;
  const w = containerRect.width;

  // Set the dimensions and margins of the diagram
  const margin = {top: 20, right: 90, bottom: 30, left: 100},
        width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

  var recursivePrerequisiteSearch = (c) => {
    var tree = {};
    if (Object.keys(c).length) {
      var course = null;

      try {
        course = JSON.parse(c.course);
      }
      catch {
        tree.name = c.course;
        return tree;
      }

      tree.name = course.fullname;
      if (c.prerequisites.length) {
        tree.children = [];
        c.prerequisites.forEach((d) => {
          tree.children.push(recursivePrerequisiteSearch(d));
        })
      }
      return tree;
    }
    else {
      return;
    }
  }

  var treeDataConverter = (c) => {
    var treeObj = {};
    if (Object.keys(c).length && c.courses) {
      treeObj = recursivePrerequisiteSearch(c.courses);
    };
    return treeObj;;
  }

  var data = treeDataConverter(coursesData);

  //Export graph as image on download click
  d3.select("#download-tree-graph").on('click', function() {
    // Get the d3js SVG element and save using saveSvgAsPng.js
    SvgToPng.saveSvgAsPng(document.getElementById("course-tree-graph"), "course-tree-graph.png", {backgroundColor: "#FFFFFF", left: 0, top: 0});
  });

  d3.select("#course-tree-graph").remove();
  var svg = d3.select(container).append("svg")
      .attr("viewBox", [-margin.left, -margin.top, width + margin.right + margin.left, height + margin.top + margin.bottom])
      .attr("id", "course-tree-graph");      

  const g = svg.append("g")
      .attr("class", "everything")
        
  var zoom_handler = d3.zoom()
      .on("zoom", function ({transform}) {
        g.attr("transform", transform);
      })
      .scaleExtent([1, 1])
        
  zoom_handler(svg)

  var i = 0,
      duration = 750,
      root;

  // declares a tree layout and assigns the size
  var treemap = d3.tree().size([height, width]);

  if (data && Object.keys(data).length) {
    // Assigns parent, children, height, depth
    root = d3.hierarchy(data, function(d) { return d.children; });
    root.x0 = height / 2;
    root.y0 = 0;

    // Collapse after the second level
    if (root.children) root.children.forEach(collapse);
    update(root);
  
    d3.select("#collapse-all").on('click', function() {
      collapseAll(root)
    });
    d3.select("#expand-all").on('click', function() {
      expandAll(root)
    });
  } 

  // Collapse the node and all it's children
  function collapse(d) {
    if(d.children) {
      d._children = d.children
      d._children.forEach(collapse)
      d.children = null
    }
  }

  function expand(d) {
    if (d._children) {
      d.children = d._children
      d.children.forEach(expand)
      d._children = null
    }
  }

  function collapseAll(d) {
    collapse(d)
    update(d)
  }

  function expandAll(d) {
    collapse(d)
    expand(d)
    update(d)
  }

  function update(source) {

    // Assigns the x and y position for the nodes
    var treeData = treemap(root);

    // Compute the new tree layout.
    var nodes = treeData.descendants(),
        links = treeData.descendants().slice(1);

    // Normalize for fixed-depth.
    nodes.forEach(function(d){ d.y = d.depth * 180});

    // ****************** Nodes section ***************************

    // Update the nodes...
    var node = g.selectAll('g.node')
        .data(nodes, function(d) {return d.id || (d.id = ++i); });

    // Enter any new modes at the parent's previous position.
    var nodeEnter = node.enter().append('g')
        .attr('class', 'node')
        .attr("transform", function(d) {
          return "translate(" + source.y0 + "," + source.x0 + ")";
      })
      .on('click', click);

    // Add Circle for the nodes
    nodeEnter.append('circle')
        .attr('class', 'node')
        .attr('r', 1e-6)
        .style("fill", function(d) {
            return d._children ? "lightsteelblue" : "darkgrey";
        });

    // Add labels for the nodes
    nodeEnter.append('text')
        .attr("dy", ".35em")
        .attr("x", function(d) {
            return d.children || d._children ? -13 : 13;
        })
        .attr("text-anchor", function(d) {
            return d.children || d._children ? "end" : "start";
        })
        .text(function(d) { return d.data.name; });

    // UPDATE
    var nodeUpdate = nodeEnter.merge(node);

    // Transition to the proper position for the node
    nodeUpdate.transition()
      .duration(duration)
      .attr("transform", function(d) { 
          return "translate(" + d.y + "," + d.x + ")";
      });

    // Update the node attributes and style
    nodeUpdate.select('circle.node')
      .attr('r', 10)
      .style("fill", function(d) {
          return d._children ? "lightsteelblue" : "darkgrey";
      })
      .attr('cursor', 'pointer');


    // Remove any exiting nodes
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + source.y + "," + source.x + ")";
        })
        .remove();

    // On exit reduce the node circles size to 0
    nodeExit.select('circle')
      .attr('r', 1e-6);

    // On exit reduce the opacity of text labels
    nodeExit.select('text')
      .style('fill-opacity', 1e-6);

    // ****************** links section ***************************

    // Update the links...
    var link = g.selectAll('path.link')
        .data(links, function(d) { return d.id; });

    // Enter any new links at the parent's previous position.
    var linkEnter = link.enter().insert('path', "g")
        .attr("class", "link")
        .attr('d', function(d){
          var o = {x: source.x0, y: source.y0}
          return diagonal(o, o)
        })
        .attr("fill", "none")
        .attr("stroke", "#CCC")
        .attr("stroke-width", "2px");

    // UPDATE
    var linkUpdate = linkEnter.merge(link);

    // Transition back to the parent element position
    linkUpdate.transition()
        .duration(duration)
        .attr('d', function(d){ return diagonal(d, d.parent) });

    // Remove any exiting links NOTE: do not remove
    var linkExit = link.exit().transition()
        .duration(duration)
        .attr('d', function(d) {
          var o = {x: source.x, y: source.y}
          return diagonal(o, o)
        })
        .remove();

    // Store the old positions for transition.
    nodes.forEach(function(d){
      d.x0 = d.x;
      d.y0 = d.y;
    });

    // Creates a curved (diagonal) path from parent to the child nodes
    function diagonal(s, d) {

      var path = `M ${s.y} ${s.x}
              C ${(s.y + d.y) / 2} ${s.x},
                ${(s.y + d.y) / 2} ${d.x},
                ${d.y} ${d.x}`

      return path
    }

    // Toggle children on click.
    function click(event, d) {
      if (d.children) {
          d._children = d.children;
          d.children = null;
        } else {
          d.children = d._children;
          d._children = null;
        }
      update(d);
    }
  }

  return {
    nodes: () => {
      return svg.node();
    }
  };
}