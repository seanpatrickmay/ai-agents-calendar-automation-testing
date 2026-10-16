const $ = id => document.getElementById(id);
let events = [], selected = new Date().toISOString().slice(0,10), shown = new Date(selected+'T00:00:00Z'), editing = null;
const dayKey = date => date.toISOString().slice(0,10);
const fmt = (date, options) => new Intl.DateTimeFormat('en', {...options,timeZone:'UTC'}).format(date);
async function api(path='', method='GET', body) {
  const response = await fetch('/api/events'+path, {method,headers:body ? {'Content-Type':'application/json'} : {},body:body ? JSON.stringify(body) : undefined});
  const data = await response.json(); if (!response.ok) throw new Error(data.error); return data;
}
function onDay(event, date) { const start=Date.parse(date+'T00:00:00Z'); return Date.parse(event.start)<start+86400000 && Date.parse(event.end)>start; }
function render() {
  $('month').textContent = fmt(shown,{month:'long',year:'numeric'});
  const first = new Date(Date.UTC(shown.getUTCFullYear(),shown.getUTCMonth(),1));
  first.setUTCDate(first.getUTCDate()-(first.getUTCDay()+6)%7);
  $('calendar').replaceChildren();
  for(let i=0;i<42;i++) {
    const date = new Date(first); date.setUTCDate(first.getUTCDate()+i); const key=dayKey(date);
    const button = document.createElement('button'); button.className='day'+(date.getUTCMonth()!==shown.getUTCMonth()?' other':'')+(key===selected?' selected':'')+(key===dayKey(new Date())?' now':'');
    button.setAttribute('aria-label',fmt(date,{dateStyle:'full'})); button.setAttribute('aria-pressed',String(key===selected));
    const number=document.createElement('span');number.className='number';number.textContent=date.getUTCDate();button.append(number);
    const items=events.filter(event=>onDay(event,key));
    for(const event of items.slice(0,2)) {const chip=document.createElement('span');chip.className='chip';chip.textContent=event.title;button.append(chip);}
    if(items.length>2){const more=document.createElement('span');more.textContent=`+${items.length-2} more`;button.append(more);}
    button.onclick=()=>{selected=key;render();};$('calendar').append(button);
  }
  $('selected').textContent=fmt(new Date(selected+'T00:00:00Z'),{month:'long',day:'numeric',year:'numeric'});
  $('agenda').replaceChildren();const items=events.filter(event=>onDay(event,selected));
  if(!items.length){const empty=document.createElement('p');empty.textContent='No events. Add something fictional.';$('agenda').append(empty);}
  for(const event of items){const button=document.createElement('button');button.className='event';const title=document.createElement('strong');title.textContent=event.title;const detail=document.createElement('span');detail.textContent=`${fmt(new Date(event.start),{dateStyle:'medium',timeStyle:'short'})} – ${fmt(new Date(event.end),{dateStyle:'medium',timeStyle:'short'})} UTC`;button.append(title,detail);if(event.location){const location=document.createElement('span');location.textContent=event.location;button.append(location);}button.onclick=()=>openEditor(event);$('agenda').append(button);}
}
async function refresh(){try{events=await api();render();$('status').textContent=`${events.length} event${events.length===1?'':'s'} · Saved locally · UTC`;}catch(error){$('status').textContent=error.message;}}
function openEditor(event){editing=event?.id??null;$('form-title').textContent=editing?'Edit event':'Add event';$('title').value=event?.title??'';$('start').value=event?.start.slice(0,19)??selected+'T09:00:00';$('end').value=event?.end.slice(0,19)??selected+'T10:00:00';$('location').value=event?.location??'';$('notes').value=event?.notes??'';$('delete').hidden=!editing;$('form-error').textContent='';$('editor').showModal();$('title').focus();}
$('add').onclick=()=>openEditor();$('cancel').onclick=()=>$('editor').close();$('refresh').onclick=refresh;
for(const [id,delta] of [['prev',-1],['next',1]]) $(id).onclick=()=>{shown=new Date(Date.UTC(shown.getUTCFullYear(),shown.getUTCMonth()+delta,1));render();};
$('today').onclick=()=>{selected=dayKey(new Date());shown=new Date(selected+'T00:00:00Z');render();};
$('form').onsubmit=async e=>{e.preventDefault();$('save').disabled=true;try{const body={title:$('title').value,start:$('start').value+'Z',end:$('end').value+'Z',location:$('location').value,notes:$('notes').value};await api(editing?'/'+editing:'',editing?'PUT':'POST',body);selected=body.start.slice(0,10);shown=new Date(selected+'T00:00:00Z');$('editor').close();await refresh();}catch(error){$('form-error').textContent=error.message;}finally{$('save').disabled=false;}};
$('delete').onclick=async()=>{if(!confirm('Delete this fictional event?'))return;$('delete').disabled=true;try{await api('/'+editing,'DELETE');$('editor').close();await refresh();}catch(error){$('form-error').textContent=error.message;}finally{$('delete').disabled=false;}};
refresh();
