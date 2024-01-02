document.addEventListener("DOMContentLoaded", function () {
  // Declare a global variable to store the chart instance
  var myChart;

  // Function to update the table with new data
  function updateTable(topEntries) {
    var tableBody = $('#data-table tbody');
    tableBody.empty(); // Clear existing content

    topEntries.forEach(function (entry) {
      var rowData = '<td class="multiline">' + entry.data + '</td>';
      var row = '<tr>' +
        '<td>' + entry.id + '</td>' +
        rowData +
        '<td>' + entry.date + '</td>' +
        '<td>' + entry.mac_adr+ '</td>' +
        '<td><button onclick="deleteData(' + entry.id + ')" class="btn btn-danger">Delete</button></td>' +
        '</tr>';
      tableBody.append(row);
    });
    console.log('Table updated successfully.'); // Log success message
  }

  // Function to draw the line chart
  function drawLineChart(labels, data) {
    var ctx = document.getElementById('myChart').getContext('2d');
    var xMin = Math.min(...labels);
    var xMax = Math.max(...labels);

    if (myChart) {
      myChart.data.labels = labels;
      myChart.data.datasets[0].data = data;
      myChart.options.scales.x.min = xMin;
      myChart.options.scales.x.max = xMax;
      myChart.update(); // Update the chart
    } else {
      myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Data Trends',
            data: data,
            borderColor: 'rgba(32, 135, 71, 1)',
            borderWidth: 1,
            fill: true,
            pointRadius: 2,
            pointBackgroundColor: 'rgba(32, 135, 71, 1)',
          }]
        },
        options: {
          scales: {
            x: {
              type: 'linear',
              min: xMin,
              max: xMax,
            },
            y: {
              min: 0,
              max: 4100,
            }
          }
        }
      });
    }
  }

  // Function to fetch chart data and populate the chart
  // function fetchChartAndPopulate() {
  //   var selectedDeviceId = document.getElementById('deviceIdSelect').value;

  //   $.ajax({
  //     url: '/esp?id=' + selectedDeviceId,
  function fetchChartAndPopulate() {
    var macAddress = document.getElementById('macSelect').value;

    $.ajax({
      url: '/esp?mac_adr=' + macAddress,
      method: 'GET',
      success: function (rawData) {
        rawData.sort((a, b) => b.id - a.id);
        var topChart = rawData.slice(0, 5);

        const parsedData = topChart.map(entry => {
          const items = entry.data.split('?').filter(Boolean);
          const data = items.map(item => {
            const [time, value] = item.split('&');
            return { time, value: parseInt(value) };
          });
          return data;
        });

        const flatData = parsedData.reduce((acc, val) => acc.concat(val), []);
        flatData.sort((a, b) => a.time - b.time);

        var labels = flatData.map(entry => entry.time);
        var values = flatData.map(entry => entry.value);

        drawLineChart(labels, values);
      },
      error: function (error) {
        console.error('Error fetching chart data:', error);
      }
    });
  }

  // Function to fetch table data and populate the table
  function fetchTableAndPopulate() {
    $.ajax({
      url: '/esp',
      method: 'GET',
      success: function (rawData) {
        rawData.sort((a, b) => b.id - a.id);
        var topTable = rawData.slice(0, 50);
        updateTable(topTable);
      },
      error: function (error) {
        console.error('Error fetching table data:', error);
      }
    });
  }

  // Event listener for the change event of the deviceIdSelect
  document.getElementById('macSelect').addEventListener('change', function () {
    fetchChartAndPopulate();
    fetchTableAndPopulate();
  });

  // Initial data fetch and population
  fetchChartAndPopulate();
  fetchTableAndPopulate();

  // Timer to update the data periodically
  setInterval(function () {
    fetchChartAndPopulate();
    fetchTableAndPopulate();
  }, 1000);
});


function closeAlert(button) {
  // Tìm ra phần tử cha của nút đóng (button)
  var alertDiv = button.closest('.alert');

  // Ẩn phần tử cha (đó là thông báo)
  if (alertDiv) {
    alertDiv.style.display = 'none';
  }
}

function deleteData(dataId) {
  fetch("/delete-data", {
    method: "POST",
    body: JSON.stringify({ dataId: dataId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteAllData() {
  fetch("/delete-all", {
    method: "POST",
    body: "200",
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteDevice(device_id) {
  fetch("/delete-device", {
    method: "POST",
    body: JSON.stringify({ device_id: device_id }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function resetAllDevice() {
  fetch("/reset-all", {
    method: "POST",
    body: "200",
  }).then((_res) => {
    window.location.href = "/";
  });
}

function turnOnAllDevices() {
  fetch("/turn-on-all", {
    method: "POST",
    body: "200",
  }).then((_res) => {
    window.location.href = "/";
  });
}
function turnOffAllDevices() {
  fetch("/turn-off-all", {
    method: "POST",
    body: "200",
  }).then((_res) => {
    window.location.href = "/";
  });
}

function exportAllData() {
  // Assuming you want to send "200" as a query parameter
  const queryParams = new URLSearchParams({ data: "200" });

  fetch(`/export?${queryParams}`, {
    method: "GET",
  }).then((_res) => {
    // Redirect to the root ("/") after the request is complete
    window.location.href = "/";
  });
}


function toggleChange(device_id) {
  // Lấy tham chiếu đến phần tử checkbox và phần tử hiển thị trạng thái
  var deviceSw = document.getElementById('deviceSw' + device_id);
  // Thêm sự kiện thay đổi
  deviceSw.addEventListener("change", function () {
    if (deviceSw.checked) {
      statusChange(1, device_id);
    } else {
      statusChange(0, device_id);
    }
  });
}

// Function to handle status change
function statusChange(log, device_id) {
  $.ajax({
    url: '/status-change',
    method: 'POST',
    data: JSON.stringify({ log: log, device_id: device_id }),
    contentType: 'application/json',
    success: function () {
      console.log('Status changed successfully.');

      // Update the status element based on the new log value
      var statusElement = document.getElementById('status' + device_id);

      if (statusElement) {
        if (log) {
          statusElement.textContent = 'Status: ON';
        } else {
          statusElement.textContent = 'Status: OFF';
        }
      } else {
        console.error('Status element not found for device ID: ' + device_id);
      }
    },
    error: function (error) {
      console.error('Error changing status:', error);
    }
  });
}

// CAMERA FUNCTION
function deleteCamera(camera_id) {
  fetch("/delete-camera", {
    method: "POST",
    body: JSON.stringify({ camera_id: camera_id }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function cameraTurn(camera_id) {
  // Lấy tham chiếu đến phần tử checkbox và phần tử hiển thị trạng thái
  var cameraSw = document.getElementById('cameraSw' + camera_id);
  // Thêm sự kiện thay đổi
  cameraSw.addEventListener("change", function () {
    if (cameraSw.checked) {
      cameraTurnChange(1, camera_id);
    } else {
      cameraTurnChange(0, camera_id);
    }
  });
}

// Function to handle status change
function cameraTurnChange(log_2, camera_id) {
  $.ajax({
    url: '/camera-turn',
    method: 'POST',
    data: JSON.stringify({ log_2: log_2, camera_id: camera_id }),
    contentType: 'application/json',
    success: function () {
      console.log('Status changed successfully.');

      // Update the status element based on the new log value
      var statusElement = document.getElementById('camera' + camera_id);

      if (statusElement) {
        if (log_2) {
          statusElement.textContent = 'Status: ON';
        } else {
          statusElement.textContent = 'Status: OFF';
        }
      } else {
        console.error('Status element not found for camera ID: ' + camera_id);
      }
    },
    error: function (error) {
      console.error('Error changing status:', error);
    }
  });
}
