var lists = [];


function checkSwitch(value, btnNum) {
  data = {
    num: btnNum,
    state: value
  }
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/switch-change", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      console.log(xhr.responseText);
    }
  }
  xhr.send(JSON.stringify(data));
}

function getCurSwitch(id, btnNum) {
  const selectedSwitch = document.getElementById(id);
  checkSwitch(selectedSwitch.checked, btnNum);
}


function signup() {

}

const videoContainer = document.getElementById("videoFrame");
const videoContoller = document.getElementById("videoBtn");

function videoControl() {
  if (!videoContoller.checked) {
    videoContainer.style.display = "none";
  } else {
    videoContainer.style.display = "block";
  }
}

function customizing() {
  var module_name = $('#module_name').val();
  console.log("명령 값 : " + module_name);
  console.log(typeof module_name);
  var l_led = $('input[name=l_led]:checked').val();
  console.log("l_led 값 : " + l_led);
  console.log(typeof l_led);
  var m_led = $('input[name=m_led]:checked').val();
  console.log("m_led 값 : " + m_led);
  console.log(typeof l_led);
  var g_led = $('input[name=g_led]:checked').val();
  console.log("g_led 값 : " + g_led);
  console.log(typeof l_led);
  var window = $('input[name=window]:checked').val();
  console.log("창문 값 : " + window);
  console.log(typeof l_led);
  var g_window = $('input[name=g_window]:checked').val();
  console.log("차고 값 : " + g_window);
  console.log(typeof g_window);
  $.ajax({
      type: "POST",
      url: '/insert',
      data: {
          'name': module_name,
          'l_led': l_led,
          'm_led': m_led,
          'g_led': g_led,
          'window': window,
          'g_window': g_window
      },
      dataType: 'text',
      success: function (result) {
          $("#rst_check").text(result);
      },
      error: function (xhr, status, error) {
          error
      }
  })
};
function show() {
  $.ajax({
      type: "POST",
      url: '/show',
      dataType: 'text',
      success: function (result) {
          $("#test").html(result);
      },
      error: function (xhr, status, error) {
          error
      }
  })
};
function mike() {
  $.ajax({
      type: "POST",
      url: '/test',
      dataType: 'text',
      success: function (result) {
          $("#test").html(result);
      },
      error: function (xhr, status, error) {
          error
      }
  })
};
function streaming() {
  $.ajax({
      type: "POST",
      url: '/home/pi/SEONMO/transcribe_streaming_mic.py',
      dataType: 'text',
      data: null,
      success: function (result) {
          $("#test").html(result);
      },
      error: function (xhr, status, error) {
          error
      }
  })
}