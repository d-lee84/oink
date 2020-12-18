"use strict";

function getToggleLikeAPI(msgId) { return `/api/messages/${msgId}/toggle_like` }


async function toggleLike(evt) {
  let $icon = $(evt.target);
  console.log("$icon=", $icon)
  
  let msgId = $icon.data("msg-id");

  const API = getToggleLikeAPI(msgId);

  let resp = await axios.post(API)

  console.log("data msg=", resp.data.message)
  console.log("status=", resp.status)
  console.log("status type=", typeof resp.status)

  if (resp.data.message === "There is no message" || resp.status === 401) {
    return;
  }

  $icon.toggleClass("far");
  $icon.toggleClass("fas");

}


$("#messages").on("click", ".fa-heart", toggleLike);