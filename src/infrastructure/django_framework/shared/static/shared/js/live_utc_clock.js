var liveUtcClock = document.getElementById('live-utc-clock');

function updateLiveUtcClock() {
  var d = new Date();

  var h = d.getUTCHours();
  var m = d.getUTCMinutes();
  var s = d.getUTCSeconds();

  liveUtcClock.textContent = pad(h, 2) + ':' + pad(m, 2) + ':' + pad(s, 2);
}

updateLiveUtcClock();
setInterval(updateLiveUtcClock, 1000);