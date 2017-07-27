"use strict";


$(function () {
  function addToSavedJobs(results) {

    var id = results.id;
    var saved = results.status;

    if (saved === "saved") {
      $('#' + id).css('color', '#00A3D5');
      $('#' + id).removeClass('not-saved').addClass('saved');
      $('#' + id).html('<i class="material-icons md-18">thumb_up</i>');
    }

    else if (saved === "not-saved") {
      $('#' + id).css('color', 'grey');
      $('#' + id).removeClass('saved').addClass('not-saved');
      $('#' + id).html('<i class="material-icons md-18">thumb_up</i>')
    }
  }

  $('button[name=save-job]').on('click', function (evt) {
    var id = this.id;
    var saved = this.className;
    var data = {'id': id, 'saved': saved};
    console.log(data);

    $.post("/processsave.json", data, addToSavedJobs);
  });
});

$(function () {
  function removeSavedJobs(results) {

    var id = results.id;
    var unsaved = results.status;

    $('div').remove('#' + id);
  }

  $('button[name=unsave-job]').on('click', function (evt) {
    var id = this.id;
    var unsaved = this.className;
    var data = {'id': id, 'unsaved': unsaved};
    console.log(data);

    $.post("/processsave.json", data, removeSavedJobs);
  });
});


