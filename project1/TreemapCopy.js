d3.json("PropertyTypeCopy.json").then(data => {
  // Transform each child (as before)
  data.children = data.children.map(d => ({
    name: d["Property Name"],
    usage: d["Property Usage"],
    // Convert GSF to numeric
    value: +String(d["GSF"]).replace(/,/g, "")
  }));

  // Build hierarchy
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);

  // Dimensions
  const headerHeight = 70;
  const width = window.innerWidth;
  const height = window.innerHeight - headerHeight;

  // Compute treemap layout
  d3.treemap()
    .size([width, height])
    .padding(2)(root);

  // -- COLOR LOGIC --
  // For "Education" => orange, otherwise => gray
  // (No color scale needed if you only want two colors)
  function getFillColor(d) {
    return d.data.usage === "Education" ? "#F47321" : "#828282";
  }

  // -- LABEL THRESHOLD LOGIC --
  // Option A: fixed threshold
  // const labelThreshold = 50000;

  // Option B: relative threshold (10% of max)
  const maxValue = d3.max(root.leaves(), d => d.value);
  const labelThreshold = 0.1 * maxValue;

  // Select container
  const container = d3.select("#treemap");

  // Create nodes
  const nodes = container.selectAll(".node")
    .data(root.leaves())
    .enter()
    .append("div")
      .attr("class", "node node--leaf")
      .style("left", d => d.x0 + "px")
      .style("top",  d => d.y0 + "px")
      .style("width",  d => (d.x1 - d.x0) + "px")
      .style("height", d => (d.y1 - d.y0) + "px")
      .style("background-color", d => getFillColor(d));

  // Append labels only for larger buildings
  nodes.append("div")
    .attr("class", "label")
    .text(d => d.value >= labelThreshold ? d.data.name : "");

  // Optional hover effect
  nodes
    .on("mouseover", function() {
      d3.select(this).style("opacity", 0.85);
    })
    .on("mouseout", function() {
      d3.select(this).style("opacity", 1);
    });
})
.catch(error => {
  console.error("Error loading JSON file:", error);
});
