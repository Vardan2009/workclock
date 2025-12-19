import{y as e}from"./index-DMYWl0Kz.js";const s=`https://time-manager-app-backend.onrender.com

`;async function i(n,r={}){const a={"Content-Type":"application/json",...r.headers||{}};e.state.accessToken&&(a.Authorization=`Bearer ${e.state.accessToken}`);const o=await fetch(`${s}${n}`,{...r,headers:a}),t=await o.json();if(t.error)throw new Error(t.error);if(o.status===401)throw e.logout(),new Error("Unauthorized");return t}export{i as a};
