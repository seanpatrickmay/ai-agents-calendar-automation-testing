/** Pi adapter: fixed loopback CRUD only, no shell, filesystem or credential access. */
import { Type } from "@earendil-works/pi-ai";
import { defineTool, type ExtensionAPI } from "@earendil-works/pi-coding-agent";
const port = process.env.CALENDAR_PORT ?? "8765";
if (!/^\d+$/.test(port) || Number(port)<1024 || Number(port)>65535) throw new Error("Invalid calendar loopback port");
const event = Type.Object({title:Type.String(),start:Type.String({description:"ISO 8601 with explicit offset, e.g. 2030-04-08T09:00:00Z"}),end:Type.String(),location:Type.Optional(Type.String()),notes:Type.Optional(Type.String())},{additionalProperties:false});
async function call(method:string, id?:string, body?:unknown) {
  const response=await fetch(`http://127.0.0.1:${port}/api/events`+(id?"/"+encodeURIComponent(id):""),{method,headers:{"Content-Type":"application/json"},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(10000)});
  const data=await response.json(); if(!response.ok)throw new Error(data.error);
  return {content:[{type:"text" as const,text:JSON.stringify(data)}],details:data};
}
export default function(pi:ExtensionAPI){
  pi.registerTool(defineTool({name:"calendar_list",label:"List events",description:"List fictional local calendar events, ordered by UTC start.",parameters:Type.Object({}),async execute(){return call("GET");}}));
  pi.registerTool(defineTool({name:"calendar_get",label:"Get event",description:"Get one fictional event by stable ID.",parameters:Type.Object({id:Type.String()}),async execute(_id,p){return call("GET",p.id);}}));
  pi.registerTool(defineTool({name:"calendar_create",label:"Create event",description:"Create a fictional local event. Confirm human intent first.",parameters:Type.Object({event}),async execute(_id,p){return call("POST",undefined,p.event);}}));
  pi.registerTool(defineTool({name:"calendar_update",label:"Update event",description:"Replace event fields by stable ID. Get current data first; omitted location/notes become empty. Confirm human intent.",parameters:Type.Object({id:Type.String(),event}),async execute(_id,p){return call("PUT",p.id,p.event);}}));
  pi.registerTool(defineTool({name:"calendar_delete",label:"Delete event",description:"Delete a fictional event by exact ID after confirming human intent.",parameters:Type.Object({id:Type.String()}),async execute(_id,p){return call("DELETE",p.id);}}));
}
