import React from "react";
import { runTreeGraph } from "./treeGraphGenerator";
import styles from "./Graph.module.css";

export function TreeGraph({ coursesData }) {
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    let destroyFn;

    if (containerRef.current) {
      const { destroy } = runTreeGraph(containerRef.current, coursesData);
      destroyFn = destroy;
    }

    return destroyFn;
  });

  return <div ref={containerRef} className={styles.container} />;
}