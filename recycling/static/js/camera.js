const width = 320; // We will scale the photo width to this
let height = 0; // This will be computed based on the input stream

let streaming = false;

let video = null;
let canvas = null;
let photo = null;
let startbutton = null;
let scanbutton = null;
let restartbutton = null;

function showViewLiveResultButton() {
  if (window.self !== window.top) {
    document.querySelector(".contentarea").remove();
    const button = document.createElement("button");
    button.textContent = "View live result of the example code above";
    document.body.append(button);
    button.addEventListener("click", () => window.open(location.href));
    return true;
  }
  return false;
}

function startup() {
  if (showViewLiveResultButton()) {
    return;
  }
  
  video = document.getElementById("video");
  canvas = document.getElementById("canvas");
  photo = document.getElementById("photo");
  startbutton = document.getElementById("startbutton");
  scanbutton = document.getElementById("scanbutton");
  restartbutton = document.getElementById("restartbutton");

  let constraints = { video: true, audio: false };

  if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    constraints = {
      video: {
        facingMode: { exact: "environment" } // Request the rear camera
      },
      width: { ideal: 1280 },
      height: { ideal: 720 }
    };
  }

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      video.srcObject = stream;
      video.playsInline = true;
      video.play();
    })
    .catch((err) => {
      console.error(`An error occurred: ${err}`);
    });

  video.addEventListener(
    "canplay",
    (ev) => {
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width);

        if (isNaN(height)) {
          height = width / (4 / 3);
        }

        video.setAttribute("width", width);
        video.setAttribute("height", height);
        canvas.setAttribute("width", width);
        canvas.setAttribute("height", height);
        streaming = true;
      }
    },
    false,
  );

  clearphoto();
}

function clearphoto() {
  const context = canvas.getContext("2d");
  context.fillStyle = "#AAA";
  context.fillRect(0, 0, canvas.width, canvas.height);

  const data = canvas.toDataURL("image/png");
  photo.setAttribute("src", data);
}

function restartvideo() {
  video.style.display = "";
  startbutton.style.display = "";
  photo.style.display = "none";
  restartbutton.style.display = "none";
}

function takepicture() {
  let shuttersound = document.getElementById('shuttersound');
  shuttersound.play();
  const context = canvas.getContext("2d");
  if (photo.width && photo.height) {
    canvas.width = photo.width;
    canvas.height = photo.height;
    context.drawImage(video, 0, 0, photo.width, photo.height);
    video.style.display = "none";
    startbutton.style.display = "none";
    photo.style.display = "";
    scanbutton.style.display = "";
    restartbutton.style.display = "";

    const data = canvas.toDataURL("image/png");
    photo.setAttribute("src", data);
  } else {
    clearphoto();
  }
}

LABELS = {
  '-1': 'Incierto',
  '0': 'Empaque impreso',
  '1': 'Botella',
  '2': 'Papel',
  '3': 'Lata de aluminio',
  '4': 'Vaso de papel',
  '5': 'Otros',
  '6': 'Orgánico',
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function scanpicture(api_key, ip_server) {
  const csrftoken = getCookie('csrftoken');

  $('#scanspinner').removeClass('d-none');
  serverURL = ip_server
  photoTaken = document.getElementById("photo");
  mbin = document.getElementById("m-bin");
  mimg1 = document.getElementById("m-img1");
  mimg2 = document.getElementById("m-img2");
  mimg3 = document.getElementById("m-img3");
  imageData = photoTaken.getAttribute("src");
  apikey = api_key
  $.ajax({
    type: "POST",
    url:serverURL,
    data: JSON.stringify({'frame': imageData, 'user': 'online-guest'}),
    crossDomain: true,
    dataType: 'json',
    headers: {"x-api-key": apikey},
    success: function(response) {
      responseElement = document.getElementById("scanresponse");
      var label = LABELS.hasOwnProperty(response.prediction) ? LABELS[response.prediction] : LABELS[-1];
      if (response.prediction == '-1' || response.prediction == '5') {
        mbin.innerHTML = 'negra';
        mimg1.classList.add('d-none'); mimg3.classList.add('d-none'); mimg2.classList.remove('d-none');
      } else if (response.prediction == '6') {
        mbin.innerHTML = 'verde';
        mimg1.classList.add('d-none'); mimg2.classList.add('d-none'); mimg3.classList.remove('d-none');
      } else {
        mbin.innerHTML = 'blanca';
        mimg2.classList.add('d-none'); mimg3.classList.add('d-none'); mimg1.classList.remove('d-none');
      }
      responseElement.innerHTML = label;

      url_save_image = '/escaneo/guardar';

      $.ajax({
        type: "POST",
        url: url_save_image,
        data: JSON.stringify({'frame': imageData}),
        crossDomain: true,
        dataType: 'json',
        headers: {
          "X-CSRFToken": csrftoken
        },
        success: function(response) {
          console.log(response);
        },
        error: function(response) {
          alert('Error escaneando foto');
        },
      });

      $('#scanmodal').modal('show');
      $('#scanspinner').addClass('d-none');
    },
    error: function(response) {
      alert('Error escaneando foto');
    },
  });
}

function closemodal() {
  $('#scanmodal').modal('hide');
}

window.addEventListener("load", startup, false);