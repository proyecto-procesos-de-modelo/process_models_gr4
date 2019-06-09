
/*
*/

function getEntryProducts() {
  console.log("get entry products function");

  var statistics = JSON.parse(document.getElementById('statistics').textContent);

  var entry_products = [];

  for (var i in statistics['entry_products']) {
    var item = statistics['entry_products'][i];
    //console.log(item);
    //console.log(item['e_products']);
    entry_products.push(item['num_products']);
  }
  console.log(entry_products);

  return entry_products;
}

new Chart(document.getElementById("statistics_1"), {
    type: 'bar',
    data: {
      labels: ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"],
      datasets: [
        {
          label: "",
          backgroundColor: ["#53B8FE", "#53B8FE","#53B8FE","#53B8FE","#53B8FE", "#53B8FE", "#53B8FE"],
          data: getEntryProducts()
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Entrada de Productos'
      }
    }
});

new Chart(document.getElementById("statistics_6"), {
    type: 'bar',
    data: {
      labels: ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"],
      datasets: [
        {
          label: "",
          backgroundColor: ["#e8c3b9", "#e8c3b9", "#e8c3b9", "#e8c3b9", "#e8c3b9", "#e8c3b9", "#e8c3b9"],
          data: [0,0,0,0,0,0,0]
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Salida de Productos'
      }
    }
});

/*
*/

function getActiveUsersLabels() {
  //console.log("get active users labels function");

  var data = document.getElementById('statistics').textContent;
  var statistics = JSON.parse(data);

  var active_users_labels = [];
  for (var i in statistics['active_users']) {
    var item = statistics['active_users'][i];
    active_users_labels.push(item['group']);
  }
  //console.log(active_users_labels);

  return active_users_labels;
}

function getActiveUsersData() {
  //console.log("get active users data function");

  var data = document.getElementById('statistics').textContent;
  var statistics = JSON.parse(data);

  var active_users_data = [];
  for (var i in statistics['active_users']) {
    var item = statistics['active_users'][i];
    active_users_data.push(item['users']);
  }
  console.log(active_users_data);

  return active_users_data;
}

new Chart(document.getElementById("statistics_7"), {
    type: 'pie',
    data: {
      labels: getActiveUsersLabels(),
      datasets: [{
        label: "",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: getActiveUsersData()
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Usuarios Activos'
      }
    }
});

new Chart(document.getElementById("statistics_8"), {
    type: 'pie',
    data: {
      labels: ["Carretilla"],
      datasets: [{
        label: "",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: [125.00]
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Gastos Mantenimiento'
      }
    }
});

new Chart(document.getElementById("statistics_10"), {
    type: 'pie',
    data: {
      labels: ["Pendientes", "Completadas"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: [3,2]
      }]
    },
    options: {
      title: {
        display: true,
        text: '% Tareas'
      }
    }
});

/*
*/

new Chart(document.getElementById("statistics_2"), {
    type: 'doughnut',
    data: {
      labels: ["Producto 1", "Producto 2", "Producto 10"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: [2,1,2] //getOcupationRooms()
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Número de Contenedores'
      }
    }
});

new Chart(document.getElementById("statistics_4"), {
    type: 'doughnut',
    data: {
      labels: ["OK", "KO"],
      datasets: [
        {
          label: "",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: [86,14]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: '% SLA'
      }
    }
});

function getOcupationRooms() {
  console.log("get % ocupation rooms function");

  var statistics = JSON.parse(document.getElementById('statistics').textContent);

  var rooms_ocupation = [];
  for (var i in statistics['rooms_ocupation']) {
    var item = statistics['rooms_ocupation'][i];
    rooms_ocupation.push(item['name']);
  }
  console.log(rooms_ocupation);

  return rooms_ocupation;
}

new Chart(document.getElementById("statistics_11"), {
    type: 'bar',
    data: {
      labels: ["Sala 1", "Sala 2", "Sala A", "Sala B", "Sala C", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "M1", "M2", "M3", "M4", "Embarque"],
      datasets: [
        {
          label: "",
          backgroundColor: ["#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f", "#3cba9f"],
          data: [44.44,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] //getOcupationRooms()
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: '% Ocupación de Salas'
      }
    }
});




/**/
