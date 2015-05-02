label$ = new google.maps.InfoWindow({
    content: messages[$]
});

google.maps.event.addListener(marker$, "click", function (e) { 
    label$.open(map, this); });

