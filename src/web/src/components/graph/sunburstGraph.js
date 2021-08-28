import React from "react";
import { runSunburstGraph } from "./sunburstGraphGenerator";
import styles from "./Graph.module.css";

export function SunburstGraph({ coursesData }) {
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    let destroyFn;

    if (containerRef.current) {
      const { destroy } = runSunburstGraph(containerRef.current, coursesData);
      destroyFn = destroy;
    }

    return destroyFn;
  });

  return <div ref={containerRef} className={styles.container} />;
}