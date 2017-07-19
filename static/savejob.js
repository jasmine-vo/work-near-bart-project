"use strict";


$(function () {
  function addToSavedJobs(results) {

    var id = results.id;
    var saved = results.status;

    if (saved === "saved") {
      $('#' + id).css('color', 'red');
      $('#' + id).removeClass('not-saved').addClass('saved');
    }

    else if (saved === "not-saved") {
      $('#' + id).css('color', 'grey');
      $('#' + id).removeClass('saved').addClass('not-saved');
    }
  }

  $('button[name=save-job]').on('click', function (evt) {
    var id = this.id;
    var saved = this.className;
    var data = {'id': id, 'saved': saved};
    console.log(data);

    $.post("/processfavorite.json", data, addToSavedJobs);
  });
});

