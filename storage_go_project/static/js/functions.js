
/*
Modal Functionalitiy
*/

function openCustomModal(url) {
  $('#custom-modal').load(url, function() {
    $(this).modal('show');
  });
  return false;
}

function closeCustomModal() {
  $('#custom-modal').modal('hide');
  return false;
}

/*
---------- JS Permissions ----------
*/

$('#id_type').on('change', function() {

  $("#id_model").empty();
  $("#id_object").empty();
  $("#id_attribute").empty();


  loadElements(function(data) {
    var opts = showElements(data);
    $("#id_model").append(opts);
  });
})

$('#id_model').on('change', function() {
  var type = $('#id_type').val();

  if (type != 'Modelo') {
    $("#id_object").empty();
    $("#id_attribute").empty();

    loadElements(function(data) {
      var opts = showElements(data);
      $("#id_object").append(opts);
    });
  }
})

$('#id_object').on('change', function() {
  var type = $('#id_type').val();

  if (type != 'Objeto') {
    $("#id_attribute").empty();

    loadElements(function(data) {
      var opts = showElements(data);
      $("#id_attribute").append(opts);
    });
  }
})

function loadElements(callback) {

  var type =  $("#id_type").val();
  var model = $("#id_model").val();
  var object = $("#id_object").val();

  console.log(type);
  console.log(model);
  console.log(object);

  $.ajax({
    method: "GET",
    url: '/panel/permissions/crear/cargar_elementos/',
    dataType: 'json',
    data: {
      type: type,
      model: model,
      object: object,
    },
    success: function(data, status) {
      callback(data);
    },
    error: function(response) {
      console.log("ERROR");
      callback(response);
    }
  });
}

function showElements(param) {
  /*
  var type = $('#id_type').val();
  var model = $('#id_model').val();
  var object = $('#id_object').val();

  console.log(type)
  console.log(model)
  console.log(object)

  console.log(param)
  */
  var opts = "";

  for (var i = 0; i < param.length; i++) {
    opts += "<option value='" + param[i][0] + "'>" + param[i][1] + "</option>";
  }
  return opts;
}




//
