var helpers = clientApp.helpers || {};

$.fn.repeat_gallery = function(result, index)  {
  if (result.visible) {
    var visible = eval(result.visible);
    if (!visible) return;
  }

  var blobListString = result.contents[0];
  var contentArray = result.contents[1];
  var repeatKey = result.repeat.split(".")[0];
  var repeatParam = result.repeat.split(".")[1];
  var repeatValues = JSON.parse(runData.get(repeatKey));
  var repeat = repeatValues[repeatParam];

  if (typeof(contentArray) == "string") {
    contentArray = [contentArray]
  }
  if (result.label) $(this).appendLabel(result.label);
  var gallerySelector = "gallery_" + index;
  $(this).append("<div class=" + gallerySelector + " ></div>");
  $("." + gallerySelector).addClass("gallery-container");

  var leftItems = "gallery-left-items-" + index;
  var rightItems = "gallery-right-items-" + index;
  renderRepeatBlobList(index, blobListString, gallerySelector, leftItems, 'left', repeat, contentArray);

  var blobsContainerSelector = "gallery-blobs-container-" + index;
  $("." + gallerySelector).append("<div class=" + blobsContainerSelector + "></div>");
  $("." + blobsContainerSelector).addClass("blobs-wrapper");
  renderRepeatBlobList(index, blobListString, gallerySelector, rightItems, 'right', repeat, contentArray);
  $("." + rightItems).addClass("gallery-item-list-right di-none");

  // Append both sides image containers
  var imgContainerLeft = "gallery-blob-container-left-" + index;
  var imgContainerRight = "gallery-blob-container-right-" + index;
  $("." + blobsContainerSelector).append("<div id=" +imgContainerLeft+ "></div>");
  $("." + blobsContainerSelector).append("<div id=" +imgContainerRight+ "></div>");
  $("#" + imgContainerLeft).addClass("gallery-blob-container");
  $("#" + imgContainerRight).addClass("gallery-blob-container di-none");

  let idx = 0;
  for (var i = 0; i < contentArray.length; i++) {
    $("#" + imgContainerLeft).append('<img src=' + work_url + eval(contentArray[i]) + ' class=gallery-img draggable=false></img>');
    $("#" + imgContainerRight).append('<img src=' + work_url + eval(contentArray[i]) + ' class=gallery-img draggable=false></img>');
    $("#" + imgContainerLeft + " > img").addClass('gallery-' +index+ '-blob-left di-inline');
    $("#" + imgContainerRight + " > img").addClass('gallery-' +index+ '-blob-right di-inline');
  }
}

function renderRepeatBlobList(galleryIndex, blobListString, gallerySelector, itemSelector, side, repeat, contentArray) {
  $("." + gallerySelector).append("<div class=" + itemSelector + "></div>");
  $("." + itemSelector).addClass("gallery-item-list");
  for (let idx = 0; idx < repeat; idx++) {
    // if (eval(contents[contentArray[i]].visible)) {
      $("." + itemSelector).append("<span id=gallery-" +galleryIndex+ "-item-" +side+ "-" +idx+ " class=gallery-item-selector>" + eval(blobListString) + "</span>");
      $("#gallery-" +galleryIndex+ "-item-" +side+ "-" +idx).addHoverRepeatFeature(galleryIndex, side, work_url, contentArray, idx);
    // }
  }
  $("." +itemSelector+ " span:first-child").addClass("gallery-item-selected");
}

$.fn.addHoverRepeatFeature = function(galleryIndex, side, work_url, contentArray, itemIndex) {
  var originalSrc = "";
  var imgSelector = '.gallery-' +galleryIndex+ '-blob-' + side;
  var selector = '.gallery-blob-container-' +side+ '-' + galleryIndex;
  var originalSrc = [];
  $(this).mouseover(function() {
    $(selector).addClass("flex-50");
    $(imgSelector).each(function(i) {
      let idx = itemIndex;
      $(this).attr("src", work_url + eval(contentArray[i]));
      $("#gallery-" +galleryIndex+ "-zoom > select").updateSize(galleryIndex);
    });
  });
  $(this).mouseout(function() {
    $(imgSelector).each(function(i){
      $(this).attr("src", originalSrc[i]);
      $("#gallery-" +galleryIndex+ "-zoom > select").updateSize(galleryIndex);
    });
  });
  $(this).on('click', function() {
    var listSelector = ".gallery-" +side+ "-items-" + galleryIndex;
    $(listSelector + " > .gallery-item-selected").toggleClass("gallery-item-selected");
    $(this).toggleClass("gallery-item-selected");
    originalSrc = [];
    $(imgSelector).each(function(){
      originalSrc.push($(this).attr("src"));
    });
  });
}
