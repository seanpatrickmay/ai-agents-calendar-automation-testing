/** Pi tool: stable event IDs per AGENTS.md §5, so no shell access is needed. */
import { createHash } from "node:crypto";
import { Type } from "@earendil-works/pi-ai";
import { defineTool, type ExtensionAPI } from "@earendil-works/pi-coding-agent";
export default function(pi:ExtensionAPI){
  pi.registerTool(defineTool({name:"stable_id",label:"Stable ID",description:"Compute the stable [cal-agent] id: first 10 hex chars of sha1(course + item_type + due_date + title), concatenated with no separators. Use the exact strings you will put in the event.",parameters:Type.Object({course:Type.String(),item_type:Type.String(),due_date:Type.String(),title:Type.String()},{additionalProperties:false}),async execute(_id,p){
    const id=createHash("sha1").update(p.course+p.item_type+p.due_date+p.title).digest("hex").slice(0,10);
    return {content:[{type:"text" as const,text:id}],details:{id}};
  }}));
}
