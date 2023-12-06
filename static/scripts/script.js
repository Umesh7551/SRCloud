/*  Js code for password input tag in login page starts here */
/* This code shows and hides password in login page */
function togglePassword() {
        var passwordInput = document.getElementById("password-input");
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    }


/*  JS code for change password */

$(document).ready(function(){
$('.pass_show').append('<span class="ptxt">Show</span>');
});


$(document).on('click','.pass_show .ptxt', function(){

$(this).text($(this).text() == "Show" ? "Hide" : "Show");

$(this).prev().attr('type', function(index, attr){return attr == 'password' ? 'text' : 'password'; });

});



/* JS code for tabs on index page  */
const triggerTabList = document.querySelectorAll('#myTab button')
triggerTabList.forEach(triggerEl => {
  const tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', event => {
    event.preventDefault()
    tabTrigger.show()
  })
})



function showTab(tabId) {
      // Hide all tab content blocks
      var tabContent = document.getElementsByClassName('tab-content');
      for (var i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
      }

      // Show the selected tab content block
      var selectedTabContent = document.getElementById(tabId);
      selectedTabContent.style.display = 'block';
    }

function showTab1(tabId) {
      // Hide all tab content blocks
      var tabContent = document.getElementsByClassName('tab-content1');
      for (var i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
      }

      // Show the selected tab content block
      var selectedTabContent = document.getElementById(tabId);
      selectedTabContent.style.display = 'block';
    }


/* JS Code for date pickers in data report tab*/
 $(function() {
    $("#fromDate").datepicker({
      dateFormat: "dd-mm-yy",
      onSelect: function(selectedDate) {
        $("#toDate").datepicker("option", "minDate", selectedDate);
      }
    });

    $("#toDate").datepicker({
      dateFormat: "dd-mm-yy",
      onSelect: function(selectedDate) {
        $("#fromDate").datepicker("option", "maxDate", selectedDate);
      }
    });

  });




/*  JS code for sending ajax request for reading and stopping rfid tag reading*/
//$(document).ready(function() {
//            // Function to send a request to start RFID reading
//            function startReading() {
//                $.ajax({
//                    type: 'GET',
//                    url: '/getreport',
//                    success: function(response) {
//                        console.log(response);
////
//                        // Parse the JSON response into an array of objects
//                        var data = JSON.parse(response);
////                        console.log(data)
//
//
//                        // Generate the table structure
//                        var table = '<table class="table table-bordered"><thead><tr><th>IP Address</th><th>Port</th><th>TagID</th><th>Time</th></tr></thead><tbody>';
//                        for (var i = 0; i < data.length; i++) {
//
//                            var key1 = Object.keys(data[i])[0]; // Extract the key
//                            var key2 = Object.keys(data[i])[1]; // Extract the key
//                            var key3 = Object.keys(data[i])[2]; // Extract the key
//                            var key4 = Object.keys(data[i])[3]; // Extract the key
////
//                            var value1 = data[i][key1]; // Extract the value
//                            var value2 = data[i][key2]; // Extract the value
//                            var value3 = data[i][key3]; // Extract the value
//                            var value4 = data[i][key4]; // Extract the value
//                            table += '<tr><td>' + value1 + '</td><td>' + value2 + '</td><td>' + value3 + '</td><td>' + value4 + '</td></tr>';
//                            }
//                        table += '</tbody></table>';
//
//                        // Display the table
//                        $('#response-content').html(table);
//                    },
//                    error: function(status, error) {
//                        console.log(error);
//
//
//                    }
//                });
//            }
//
//
//
//            // Event listener for the Start button click
//            $('#generateReport').click(function() {
//                startReading();
//            });
//
//
//        });


$(document).ready(function() {
    // Function to send a request to start RFID reading
    function startReading() {
        var fromdate = $('#fromDate').val(); // Get the from date from an input field
        var todate = $('#toDate').val(); // Get the to date from an input field

        $.ajax({
            type: 'GET',
            url: '/getreport',
            data: {
                fromdate: fromdate,
                todate: todate
            },
            success: function(response) {
                console.log(response);


                // Parse the JSON response into an array of objects
                var data = response;

                // Generate the table structure
                var table = '<table class="table table-bordered"><thead><tr><th>ID</th><th>Device ID</th><th>TagID</th><th>Time</th></tr></thead><tbody>';
                for (var i = 0; i < data.length; i++) {
                    for(var j = 0; j < i.length; j++){
                        var row = data[j];
                        var id = row[0]; // Assuming IP address is the first column
                        var device_id = row[1]; // Assuming port is the second column
                        var tagID = row[2]; // Assuming tag ID is the third column
                        var time = row[3]; // Assuming time is the fourth column



                    }


                    table += '<tr><td>' + id + '</td><td>' + device_id + '</td><td>' + tagID + '</td><td>' + time + '</td></tr>';
                }
                table += '</tbody></table>';

                // Display the table
                $('#response-content').html(table);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    }

    // Event listener for the Generate Report button click
    $('#generateReport').click(function() {
        startReading();
    });
});
