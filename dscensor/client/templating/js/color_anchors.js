var color_anchors = function(t){
    if (t.hasClass('active')){
        t.removeClass('active');
        t.addClass('visited');
    } else {
        t.removeClass('visited');
        t.addClass('active');
    }
};
